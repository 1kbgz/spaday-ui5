import { bundle } from "./tools/bundle.mjs";
import { bundle_css } from "./tools/css.mjs";
import { node_modules_external } from "./tools/externals.mjs";
import { vendor } from "./tools/vendor.mjs";

import fs from "fs";
import cpy from "cpy";

// The libraries served under their own bare specifiers (see tools/vendor.mjs): the components, the
// framework they run on -- whose configuration, theme and registries a library on the page has to
// share for setTheme() or an icon it registers to reach these elements -- and the icon, theming and
// localization packages that register into it.
const VENDORED = [
  "@ui5/webcomponents",
  "@ui5/webcomponents-base",
  "@ui5/webcomponents-icons",
  "@ui5/webcomponents-icons-business-suite",
  "@ui5/webcomponents-icons-tnt",
  "@ui5/webcomponents-localization",
  "@ui5/webcomponents-theming",
];

const VERSION = JSON.parse(
  fs.readFileSync("node_modules/@ui5/webcomponents/package.json", "utf8"),
).version;

// the elements this bundle serves: the define-guard warns about any that another copy registered first
const TAGS = JSON.parse(
  fs.readFileSync("../spaday_ui5/custom-elements.json", "utf8"),
)
  .modules.flatMap((mod) => mod.declarations.map((decl) => decl.tagName))
  .filter(Boolean);

// Every element's module -- each registers its element when it loads -- plus Assets.js, which
// registers the themes and translations beyond the built-in default, behind the define-guard. The
// guard is a module of its own, imported first: every import evaluates before the importing module's
// body, so an inlined guard would install too late. The specifiers stay imports, resolved by the
// page's import map.
const manifest = JSON.parse(
  fs.readFileSync("../spaday_ui5/custom-elements.json", "utf8"),
);
const elements = [
  ...new Set(
    manifest.modules.map((mod) =>
      mod.path.replace(/^@ui5\/webcomponents\//, ""),
    ),
  ),
]
  .map((file) => `import "@ui5/webcomponents/${file}";`)
  .join("\n");

// UI5 themes the whole document through setTheme(); follow spaday's page mode on the root. Only a
// change is applied, so a page that never uses wa-dark keeps whatever theme it configured.
const PAGE_MODE = `
const root = document.documentElement;
let dark = false;
const follow = () => {
  const next = root.classList.contains("wa-dark");
  if (next === dark) return;
  dark = next;
  setTheme(dark ? "sap_horizon_dark" : "sap_horizon");
};
new MutationObserver(follow).observe(root, { attributes: true, attributeFilter: ["class"] });
follow();
`;

const ENTRY = {
  contents: [
    'import { restoreDefine } from "./define-guard.js";',
    'import { setTheme } from "@ui5/webcomponents-base/dist/config/Theme.js";',
    'import "@ui5/webcomponents/dist/Assets.js";',
    elements,
    `restoreDefine(${JSON.stringify(`@ui5/webcomponents ${VERSION}`)}, ${JSON.stringify(TAGS)});`,
    PAGE_MODE,
    // the version actually served, so a page holding a second copy can compare and refuse rather
    // than half-work
    `Object.defineProperty(globalThis, "__spadayUi5", { value: Object.freeze({ version: ${JSON.stringify(VERSION)} }), configurable: true });`,
  ].join("\n"),
  resolveDir: "src/ts",
  loader: "js",
};

const keepImports = {
  name: "keep-imports",
  setup(build) {
    build.onResolve({ filter: /^(@ui5\/|\.\/define-guard\.js$)/ }, (args) => ({
      path: args.path,
      external: true,
    }));
  },
};

const BUNDLES = [
  {
    stdin: ENTRY,
    plugins: [node_modules_external()],
    outfile: "dist/esm/index.js",
  },
  {
    entryPoints: ["src/ts/define-guard.ts"],
    outfile: "dist/cdn/define-guard.js",
  },
  {
    stdin: ENTRY,
    plugins: [keepImports],
    outfile: "dist/cdn/index.js",
  },
];

async function build() {
  fs.rmSync("dist", { recursive: true, force: true });
  fs.rmSync("../spaday_ui5/extension", {
    recursive: true,
    force: true,
  });

  await bundle_css("src/css/ui5.css");

  await Promise.all(BUNDLES.map(bundle)).catch(() => process.exit(1));

  // the import map, relative to the served root: read by the Python package, and inlined into the
  // test page with URLs relative to it
  const imports = Object.fromEntries(
    Object.entries(await vendor(VENDORED, "dist/vendor")).map(
      ([specifier, file]) => [specifier, `vendor/${file}`],
    ),
  );
  fs.writeFileSync(
    "dist/vendor/imports.json",
    `${JSON.stringify(imports, null, 2)}\n`,
  );
  const map = JSON.stringify(
    {
      imports: Object.fromEntries(
        Object.entries(imports).map(([k, v]) => [k, `./${v}`]),
      ),
    },
    null,
    2,
  );
  const html = fs
    .readFileSync("src/html/index.html", "utf8")
    .replace(
      "<!-- importmap -->",
      `<script type="importmap">\n${map}\n    </script>`,
    );
  fs.writeFileSync("dist/index.html", html);

  // the exact version of every library this package serves, read by the Python package as its
  // ComponentPackage.provides, so spaday can reconcile it with the other packages on a page
  const { dependencies = {} } = JSON.parse(
    fs.readFileSync("package.json", "utf8"),
  );
  const served = Object.fromEntries(
    Object.keys(dependencies).map((name) => [
      name,
      JSON.parse(fs.readFileSync(`node_modules/${name}/package.json`, "utf8"))
        .version,
    ]),
  );
  fs.writeFileSync(
    "dist/versions.json",
    `${JSON.stringify(served, null, 2)}\n`,
  );

  // Copy servable assets to python extension (exclude esm/)
  fs.mkdirSync("../spaday_ui5/extension", { recursive: true });
  await cpy("dist/**/*", "../spaday_ui5/extension", {
    filter: (file) =>
      !file.relativePath.startsWith("esm/") &&
      !file.relativePath.startsWith("dist/esm/"),
  });
}

await build();
