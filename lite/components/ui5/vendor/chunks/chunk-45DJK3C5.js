import{c as l}from"./chunk-UBNHMYT7.js";var p={ATTRIBUTE:1,CHILD:2,PROPERTY:3,BOOLEAN_ATTRIBUTE:4,EVENT:5,ELEMENT:6},d=o=>(...e)=>({_$litDirective$:o,values:e}),s=class{constructor(e){}get _$AU(){return this._$AM._$AU}_$AT(e,t,i){this._$Ct=e,this._$AM=t,this._$Ci=i}_$AS(e,t){return this.update(e,t)}update(e,t){return this.render(...t)}};var u=class extends s{constructor(e){var t;if(super(e),e.type!==p.ATTRIBUTE||e.name!=="style"||((t=e.strings)===null||t===void 0?void 0:t.length)>2)throw new Error("The `styleMap` directive must be used in the `style` attribute and must be the only part in the attribute.")}render(e){return""}update(e,[t]){let{style:i}=e.element;if(this._previousStyleProperties===void 0){this._previousStyleProperties=new Set;for(let r in t)this._previousStyleProperties.add(r)}this._previousStyleProperties.forEach(r=>{t[r]==null&&(this._previousStyleProperties.delete(r),r.includes("-")?i.removeProperty(r):i[r]="")});for(let r in t){let n=t[r];n!=null&&(this._previousStyleProperties.add(r),r.includes("-")?i.setProperty(r,n):i[r]=n)}return l}},v=d(u);export{p as a,d as b,s as c,v as d};
/*! Bundled license information:

lit-html/directive.js:
  (**
   * @license
   * Copyright 2017 Google LLC
   * SPDX-License-Identifier: BSD-3-Clause
   *)

@ui5/webcomponents-base/dist/renderer/directives/style-map.js:
  (**
   * @license
   * Copyright 2018 Google LLC
   * SPDX-License-Identifier: BSD-3-Clause
   *)
*/
