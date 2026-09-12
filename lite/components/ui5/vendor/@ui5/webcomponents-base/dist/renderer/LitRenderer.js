import{a as g,b as y,c as A,d as V}from"../../../../chunks/chunk-CRBGGRWR.js";import{a as w,b as D,c as $,d as T,e as L,f as H}from"../../../../chunks/chunk-UBNHMYT7.js";import{b as x}from"../../../../chunks/chunk-KIRTPI47.js";import"../../../../chunks/chunk-VC46IEJQ.js";var{I:U}=L;var E=()=>document.createComment(""),_=(t,e,i)=>{var r;let o=t._$AA.parentNode,s=e===void 0?t._$AB:e._$AA;if(i===void 0){let n=o.insertBefore(E(),s),u=o.insertBefore(E(),s);i=new U(n,u,t,t.options)}else{let n=i._$AB.nextSibling,u=i._$AM,p=u!==t;if(p){let c;(r=i._$AQ)===null||r===void 0||r.call(i,t),i._$AM=t,i._$AP!==void 0&&(c=t._$AU)!==u._$AU&&i._$AP(c)}if(n!==s||p){let c=i._$AA;for(;c!==n;){let h=c.nextSibling;o.insertBefore(c,s),c=h}}}return i},m=(t,e,i=t)=>(t._$AI(e,i),t),j={},R=(t,e=j)=>t._$AH=e,B=t=>t._$AH,b=t=>{var e;(e=t._$AP)===null||e===void 0||e.call(t,!1,!0);let i=t._$AA,r=t._$AB.nextSibling;for(;i!==r;){let o=i.nextSibling;i.remove(),i=o}};var I=(t,e,i)=>{let r=new Map;for(let o=e;o<=i;o++)r.set(t[o],o);return r},k=y(class extends A{constructor(t){if(super(t),t.type!==g.CHILD)throw Error("repeat() can only be used in text expressions")}ct(t,e,i){let r;i===void 0?i=e:e!==void 0&&(r=e);let o=[],s=[],n=0;for(let u of t)o[n]=r?r(u,n):n,s[n]=i(u,n),n++;return{values:s,keys:o}}render(t,e,i){return this.ct(t,e,i).values}update(t,[e,i,r]){var o;let s=B(t),{values:n,keys:u}=this.ct(e,i,r);if(!Array.isArray(s))return this.ut=u,n;let p=(o=this.ut)!==null&&o!==void 0?o:this.ut=[],c=[],h,P,l=0,f=s.length-1,a=0,d=n.length-1;for(;l<=f&&a<=d;)if(s[l]===null)l++;else if(s[f]===null)f--;else if(p[l]===u[a])c[a]=m(s[l],n[a]),l++,a++;else if(p[f]===u[d])c[d]=m(s[f],n[d]),f--,d--;else if(p[l]===u[d])c[d]=m(s[l],n[d]),_(t,c[d+1],s[l]),l++,d--;else if(p[f]===u[a])c[a]=m(s[f],n[a]),_(t,s[l],s[f]),f--,a++;else if(h===void 0&&(h=I(u,a,d),P=I(p,l,f)),h.has(p[l]))if(h.has(p[f])){let v=P.get(u[a]),C=v!==void 0?s[v]:null;if(C===null){let M=_(t,s[l]);m(M,n[a]),c[a]=M}else c[a]=m(C,n[a]),_(t,s[l],C),s[v]=null;a++}else b(s[f]),f--;else b(s[l]),l++;for(;a<=d;){let v=_(t,c[d+1]);m(v,n[a]),c[a++]=v}for(;l<=f;){let v=s[l++];v!==null&&b(v)}return this.ut=u,R(t,c),$}});var N=y(class extends A{constructor(t){var e;if(super(t),t.type!==g.ATTRIBUTE||t.name!=="class"||((e=t.strings)===null||e===void 0?void 0:e.length)>2)throw Error("`classMap()` can only be used in the `class` attribute and must be the only part in the attribute.")}render(t){return" "+Object.keys(t).filter((e=>t[e])).join(" ")+" "}update(t,[e]){var i,r;if(this.it===void 0){this.it=new Set,t.strings!==void 0&&(this.nt=new Set(t.strings.join(" ").split(/\s/).filter((s=>s!==""))));for(let s in e)e[s]&&!(!((i=this.nt)===null||i===void 0)&&i.has(s))&&this.it.add(s);return this.render(e)}let o=t.element.classList;this.it.forEach((s=>{s in e||(o.remove(s),this.it.delete(s))}));for(let s in e){let n=!!e[s];n===this.it.has(s)||!((r=this.nt)===null||r===void 0)&&r.has(s)||(n?(o.add(s),this.it.add(s)):(o.remove(s),this.it.delete(s)))}return $}});var O=t=>t??T;var S=class extends A{constructor(e){if(super(e),this.et=T,e.type!==g.CHILD)throw Error(this.constructor.directiveName+"() can only be used in child bindings")}render(e){if(e===T||e==null)return this.ft=void 0,this.et=e;if(e===$)return e;if(typeof e!="string")throw Error(this.constructor.directiveName+"() called with a non-string value");if(e===this.et)return this.ft;this.et=e;let i=[e];return i.raw=i,this.ft={_$litType$:this.constructor.resultType,strings:i,values:[]}}};S.directiveName="unsafeHTML",S.resultType=1;var F=y(S);var G=(t,...e)=>{let i=x("LitStatic");return(i?i.html:w)(t,...e)},ut=(t,...e)=>{let i=x("LitStatic");return(i?i.svg:D)(t,...e)},Q=(t,e)=>{let i=t.render(),r=x("OpenUI5Enablement");r&&(i=r.wrapTemplateResultInBusyMarkup(G,t,i)),H(i,e,{host:t})},ft=(t,e,i)=>{let r=x("LitStatic");if(r)return r.unsafeStatic((e||[]).includes(t)?`${t}-${i}`:t)};var dt=Q;export{N as classMap,dt as default,G as html,O as ifDefined,k as repeat,ft as scopeTag,V as styleMap,ut as svg,F as unsafeHTML};
/*! Bundled license information:

lit-html/directive-helpers.js:
  (**
   * @license
   * Copyright 2020 Google LLC
   * SPDX-License-Identifier: BSD-3-Clause
   *)

lit-html/directives/repeat.js:
lit-html/directives/unsafe-html.js:
  (**
   * @license
   * Copyright 2017 Google LLC
   * SPDX-License-Identifier: BSD-3-Clause
   *)

lit-html/directives/class-map.js:
lit-html/directives/if-defined.js:
  (**
   * @license
   * Copyright 2018 Google LLC
   * SPDX-License-Identifier: BSD-3-Clause
   *)
*/
