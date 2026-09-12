import{a as f}from"../../../../../chunks/chunk-RWCIJGP6.js";import{a as s}from"../../../../../chunks/chunk-L4I2MXXE.js";import"../../../../../chunks/chunk-VC46IEJQ.js";var c=class{#t={};attachEvent(e,a,t){s(typeof e=="string"&&e,"Eventing.attachEvent: sType must be a non-empty string"),s(typeof a=="function","Eventing.attachEvent: fnFunction must be a function");let i=this.#t[e];Array.isArray(i)||(i=this.#t[e]=[]),i.push({fnFunction:a,oData:t})}attachEventOnce(e,a,t){let i=n=>{this.detachEvent(e,i),a.call(null,n)};i.oOriginal={fnFunction:a},this.attachEvent(e,i,t)}detachEvent(e,a){s(typeof e=="string"&&e,"Eventing.detachEvent: sType must be a non-empty string"),s(typeof a=="function","Eventing.detachEvent: fnFunction must be a function");let t=this.#t[e];if(!Array.isArray(t))return;let i;for(let n=0,r=t.length;n<r;n++)if(t[n].fnFunction===a){i=t[n],t.splice(n,1);break}if(!i)for(let n=0,r=t.length;n<r;n++){let o=t[n].fnFunction.oOriginal;if(o&&o.fnFunction===a){t.splice(n,1);break}}t.length==0&&delete this.#t[e]}fireEvent(e,a){let t,i,n,r,o;if(t=this.#t[e],Array.isArray(t))for(t=t.slice(),i=new f(e,a),n=0,r=t.length;n<r;n++)o=t[n],o.fnFunction.call(null,i)}},E=c;export{E as default};
/*! Bundled license information:

@ui5/webcomponents-localization/dist/sap/base/Eventing.js:
  (*!
   * OpenUI5
   * (c) Copyright 2026 SAP SE or an SAP affiliate company.
   * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
   *)
*/
