"""Assemble the static Pyodide example from locally built and downloaded wheels."""

import json
import shutil
import sys
import zipfile
from pathlib import Path


def copy_wheel(wheel: Path, output: Path) -> str:
    target = output / "pypi" / wheel.name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(wheel, target)
    return f"pypi/{wheel.name}"


def extract_assets(wheel: Path, package: str, output: Path) -> None:
    prefix = f"{package}/extension/"
    with zipfile.ZipFile(wheel) as archive:
        assets = [name for name in archive.namelist() if name.startswith(prefix) and not name.endswith("/")]
        if not assets:
            raise RuntimeError(f"{wheel.name} contains no browser assets")
        for name in assets:
            target = output / name.removeprefix(prefix)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(name))


def one_wheel(directory: Path, distribution: str) -> Path:
    wheels = list(directory.glob(f"{distribution}-*.whl"))
    if len(wheels) != 1:
        raise RuntimeError(f"expected one {distribution} wheel in {directory}, found {len(wheels)}")
    return wheels[0]


def main(output: Path, ui5_wheel: Path, dependency_dir: Path) -> None:
    spaday_wheel = one_wheel(dependency_dir, "spaday")
    transports_wheel = one_wheel(dependency_dir, "transports")
    wheels = {
        "ui5": copy_wheel(ui5_wheel, output),
        "spaday": copy_wheel(spaday_wheel, output),
        "transports": copy_wheel(transports_wheel, output),
    }
    ui5_assets = output / "components" / "ui5"
    extract_assets(ui5_wheel, "spaday_ui5", ui5_assets)
    extract_assets(spaday_wheel, "spaday", output / "runtime" / "spaday")
    output.joinpath("wheels.json").write_text(json.dumps(wheels, indent=2) + "\n", encoding="utf-8")

    imports = json.loads(ui5_assets.joinpath("vendor/imports.json").read_text(encoding="utf-8"))
    import_map = {specifier: f"./components/ui5/{path}" for specifier, path in imports.items()}
    template = Path(__file__).with_name("pyodide.html").read_text(encoding="utf-8")
    html = template.replace("<!-- importmap -->", f'<script type="importmap">\n{json.dumps({"imports": import_map}, indent=2)}\n</script>')
    output.joinpath("index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main(*(Path(value) for value in sys.argv[1:]))
