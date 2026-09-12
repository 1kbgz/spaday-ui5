import{a as i}from"./chunk-L4I2MXXE.js";var o=function(t){i(Array.isArray(t),"uniqueSort: input parameter must be an Array");var n=t.length;if(n>1){t.sort();for(var f=0,e=1;e<n;e++)t.indexOf(t[e])===e&&(t[++f]=t[e]);++f<n&&t.splice(f,n-f)}return t},r=o;export{r as a};
/*! Bundled license information:

@ui5/webcomponents-localization/dist/sap/base/util/array/uniqueSort.js:
  (*!
   * OpenUI5
   * (c) Copyright 2026 SAP SE or an SAP affiliate company.
   * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
   *)
*/
