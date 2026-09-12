import"../../../../../../chunks/chunk-VC46IEJQ.js";var g=/^[0-9]+(?:\.([0-9]+)(?:\.([0-9]+))?)?(.*)$/;function i(t,n,u,r){if(t instanceof i)return t;if(!(this instanceof i))return new i(t,n,u,r);var e;typeof t=="string"?e=g.exec(t):Array.isArray(t)?e=t:e=arguments,e=e||[];function f(o){return o=parseInt(o),isNaN(o)?0:o}t=f(e[0]),n=f(e[1]),u=f(e[2]),r=String(e[3]||""),this.toString=function(){return t+"."+n+"."+u+r},this.getMajor=function(){return t},this.getMinor=function(){return n},this.getPatch=function(){return u},this.getSuffix=function(){return r},this.compareTo=function(o,c,h,p){var s=i.apply(null,arguments);return t-s.getMajor()||n-s.getMinor()||u-s.getPatch()||(r<s.getSuffix()?-1:r===s.getSuffix()?0:1)}}i.prototype.inRange=function(t,n){return this.compareTo(t)>=0&&this.compareTo(n)<0};var a=i;export{a as default};
/*! Bundled license information:

@ui5/webcomponents-localization/dist/sap/base/util/Version.js:
  (*!
   * OpenUI5
   * (c) Copyright 2026 SAP SE or an SAP affiliate company.
   * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
   *)
*/
