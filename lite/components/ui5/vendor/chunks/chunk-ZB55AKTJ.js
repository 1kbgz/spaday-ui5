var a=/^((?:[A-Z]{2,3}(?:-[A-Z]{3}){0,3})|[A-Z]{4}|[A-Z]{5,8})(?:-([A-Z]{4}))?(?:-([A-Z]{2}|[0-9]{3}))?((?:-[0-9A-Z]{5,8}|-[0-9][0-9A-Z]{3})*)((?:-[0-9A-WYZ](?:-[0-9A-Z]{2,8})+)*)(?:-(X(?:-[0-9A-Z]{1,8})+))?$/i,i=class{language;script;region;variant;variantSubtags;extension;extensionSubtags;privateUse;privateUseSubtags;#t;constructor(e){var t=a.exec(e.replace(/_/g,"-"));if(t===null)throw new TypeError("The given language tag '"+e+"' does not adhere to BCP-47.");this.language=t[1]||null,this.script=t[2]||null,this.region=t[3]||null,this.variant=t[4]&&t[4].slice(1)||null,this.variantSubtags=this.variant?this.variant.split("-"):[],this.extension=t[5]&&t[5].slice(1)||null,this.extensionSubtags=this.variant?this.variant.split("-"):[],this.privateUse=t[6]||null,this.privateUseSubtags=this.privateUse?this.privateUse.slice(2).split("-"):[],this.language&&(this.language=this.language.toLowerCase()),this.script&&(this.script=this.script.toLowerCase().replace(/^[a-z]/,function(s){return s.toUpperCase()})),this.region&&(this.region=this.region.toUpperCase()),this.#t=this.#i(this.language,this.script,this.region,this.variant,this.extension,this.privateUse),Object.freeze(this)}toString(){return this.#t}#i(){return Array.prototype.filter.call(arguments,Boolean).join("-")}},n=i;export{n as a};
/*! Bundled license information:

@ui5/webcomponents-localization/dist/sap/base/i18n/LanguageTag.js:
  (*!
   * OpenUI5
   * (c) Copyright 2026 SAP SE or an SAP affiliate company.
   * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
   *)
*/
