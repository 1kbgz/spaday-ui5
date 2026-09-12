import{a as l}from"./chunk-5S7ZIXNA.js";var i=function(e,r,f,n,t){if(typeof f=="boolean"&&(n=f,f=void 0),t||(t=0),f||(f=10),t>f)return l.warning("deepEqual comparison exceeded maximum recursion depth of "+f+". Treating values as unequal"),!1;if(e===r||Number.isNaN(e)&&Number.isNaN(r))return!0;if(Array.isArray(e)&&Array.isArray(r)){if(!n&&e.length!==r.length||e.length>r.length)return!1;for(var u=0;u<e.length;u++)if(!i(e[u],r[u],f,n,t+1))return!1;return!0}if(typeof e=="object"&&typeof r=="object"){if(!e||!r||e.constructor!==r.constructor||!n&&Object.keys(e).length!==Object.keys(r).length)return!1;if(typeof Node<"u"&&e instanceof Node)return e.isEqualNode(r);if(e instanceof Date)return e.valueOf()===r.valueOf();for(var u in e)if(!i(e[u],r[u],f,n,t+1))return!1;return!0}return!1},s=i;export{s as a};
/*! Bundled license information:

@ui5/webcomponents-localization/dist/sap/base/util/deepEqual.js:
  (*!
   * OpenUI5
   * (c) Copyright 2026 SAP SE or an SAP affiliate company.
   * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
   *)
*/
