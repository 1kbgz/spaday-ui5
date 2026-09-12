import{a as o}from"./chunk-L4I2MXXE.js";var f=/('')|'([^']+(?:''[^']*)*)(?:'|$)|\{([0-9]+(?:\s*,[^{}]*)?)\}|[{}]/g,g=function(t,r){return t==null?"":(o(typeof t=="string"||t instanceof String,"pattern must be string"),(arguments.length>2||r!=null&&!Array.isArray(r))&&(r=Array.prototype.slice.call(arguments,1)),r=r||[],t.replace(f,function(a,i,e,n,s){if(i)return"'";if(e)return e.replace(/''/g,"'");if(n)return String(r[parseInt(n)]);throw new Error("formatMessage: pattern syntax error at pos. "+s)}))},l=g;export{l as a};
/*! Bundled license information:

@ui5/webcomponents-localization/dist/sap/base/strings/formatMessage.js:
  (*!
   * OpenUI5
   * (c) Copyright 2026 SAP SE or an SAP affiliate company.
   * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
   *)
*/
