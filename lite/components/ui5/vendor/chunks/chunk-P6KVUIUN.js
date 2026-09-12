import{a as o}from"./chunk-AQHH3GZX.js";import{a as g}from"./chunk-5S7ZIXNA.js";var e=o.createClass("sap.ui.base.Object",{constructor:function(){if(!(this instanceof e))throw Error('Cannot instantiate object: "new" is missing!')}});e.prototype.destroy=function(){};e.prototype.getInterface=function(){var t=new e._Interface(this,this.getMetadata().getAllPublicMethods());return this.getInterface=function(){return t},t};e.defineClass=function(t,r,s){var a=new(s||o)(t,r),n=a.getClass();return n.getMetadata=n.prototype.getMetadata=function(){return a},a.isFinal()||(n.extend=function(i,u,f){return o.createClass(n,i,u,f||s)}),g.debug("defined class '"+t+"'"+(a.getParent()?" as subclass of "+a.getParent().getName():"")),a};e.prototype.isA=function(t){return this.getMetadata().isA(t)};e.isA=function(t,r){return t instanceof e&&t.isA(r)};e.isObjectA=function(t,r){return t instanceof e&&t.isA(r)};e._Interface=function(t,r,s){if(!t)return t;function a(f,p){return function(){var c=f[p].apply(f,arguments);return s?this:c instanceof e?c.getInterface():c}}if(!r)return{};for(var n,i=0,u=r.length;i<u;i++){n=r[i];(!t[n]||typeof t[n]=="function")&&(this[n]=a(t,n))}};var h=e;export{h as a};
/*! Bundled license information:

@ui5/webcomponents-localization/dist/sap/ui/base/Object.js:
  (*!
   * OpenUI5
   * (c) Copyright 2026 SAP SE or an SAP affiliate company.
   * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
   *)
  (*!oObject[sMethodName] for 'lazy' loading interface methods ;-) *)
*/
