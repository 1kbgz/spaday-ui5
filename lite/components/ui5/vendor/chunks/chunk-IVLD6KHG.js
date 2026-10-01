import{a as e}from"./chunk-N2XOWWJG.js";import{a as n}from"./chunk-ZB55AKTJ.js";import{a as r}from"./chunk-M3L46HP2.js";import{a}from"./chunk-QLT7FJ6S.js";var g=Object.create(null),i=e.extend("sap.ui.core.Locale",{constructor:function(t){e.apply(this),t instanceof n?(this.oLanguageTag=t,this.sLocaleId=this.oLanguageTag.toString()):(this.oLanguageTag=new n(t),this.sLocaleId=t),Object.assign(this,this.oLanguageTag),this.sLanguage=this.language},getLanguage:function(){return this.language},getScript:function(){return this.script},getRegion:function(){return this.region},getVariant:function(){return this.variant},getVariantSubtags:function(){return this.variantSubtags},getExtension:function(){return this.extension},getExtensionSubtags:function(){return this.extensionSubtags},getPrivateUse:function(){return this.privateUse},getPrivateUseSubtags:function(){return this.privateUseSubtags},hasPrivateUseSubtag:function(t){return r(t&&t.match(/^[0-9A-Z]{1,8}$/i),"subtag must be a valid BCP47 private use tag"),this.privateUseSubtags.indexOf(t)>=0},toString:function(){return this.oLanguageTag.toString()},getSAPLogonLanguage:function(){return a._getSAPLogonLanguage(this)}});i._getCoreLocale=function(t){return t instanceof n&&(t=g[t.toString()]||new i(t),g[t.toString()]=t),t};var c=i;export{c as a};
/*! Bundled license information:

@ui5/webcomponents-localization/dist/sap/ui/core/Locale.js:
  (*!
   * OpenUI5
   * (c) Copyright 2026 SAP SE or an SAP affiliate company.
   * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
   *)
*/
