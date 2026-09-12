import{a as f}from"../../../../../../chunks/chunk-S7LV4H74.js";import"../../../../../../chunks/chunk-VC46IEJQ.js";var u=function(e,n){return n||(n=10),i(e,0,n)};function i(e,n,o){if(n>o)throw new TypeError("The structure depth of the source exceeds the maximum depth ("+o+")");return e==null?e:e instanceof Date?e.clone?e.clone():new Date(e.getTime()):Array.isArray(e)?l(e,n,o):typeof e=="object"?a(e,n,o):e}function l(e,n,o){for(var t=[],r=0;r<e.length;r++)t.push(i(e[r],n+1,o));return t}function a(e,n,o){if(!f(e))throw new TypeError("Cloning is only supported for plain objects");var t={};for(var r in e)r!=="__proto__"&&(t[r]=i(e[r],n+1,o));return t}var c=u;export{c as default};
/*! Bundled license information:

@ui5/webcomponents-localization/dist/sap/base/util/deepClone.js:
  (*!
   * OpenUI5
   * (c) Copyright 2026 SAP SE or an SAP affiliate company.
   * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
   *)
*/
