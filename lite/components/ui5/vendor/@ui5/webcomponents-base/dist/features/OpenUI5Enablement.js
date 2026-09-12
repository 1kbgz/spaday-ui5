import{a as c}from"../../../../chunks/chunk-GQD4P3ZM.js";import{I as n}from"../../../../chunks/chunk-BF3SMVAV.js";import{a}from"../../../../chunks/chunk-W6XL5UBJ.js";import"../../../../chunks/chunk-QJWNGS4J.js";import"../../../../chunks/chunk-WTRMJ7GF.js";import{a as o}from"../../../../chunks/chunk-KIRTPI47.js";import"../../../../chunks/chunk-VC46IEJQ.js";var d={properties:{__isBusy:{type:Boolean}}},r=class s{static wrapTemplateResultInBusyMarkup(t,i,e){return i.isOpenUI5Component&&i.__isBusy&&(e=t`
			<div class="busy-indicator-wrapper">
				<span tabindex="0" busy-indicator-before-span @focusin=${i.__suppressFocusIn}></span>
				${e}
				<div class="busy-indicator-overlay"></div>
				<div busy-indicator
					class="busy-indicator-busy-area"
					tabindex="0"
					role="progressbar"
					@keydown=${i.__suppressFocusBack}
					aria-valuemin="0"
					aria-valuemax="100"
					aria-valuetext="Busy">
					<div>
						<div class="busy-indicator-circle circle-animation-0"></div>
						<div class="busy-indicator-circle circle-animation-1"></div>
						<div class="busy-indicator-circle circle-animation-2"></div>
					</div>
				</div>
			</div>`),e}static enrichBusyIndicatorSettings(t){s.enrichBusyIndicatorMetadata(t),s.enrichBusyIndicatorMethods(t.prototype)}static enrichBusyIndicatorMetadata(t){t.metadata=a(t.metadata,d)}static enrichBusyIndicatorMethods(t){Object.defineProperties(t,{__redirectFocus:{value:!0,writable:!0},__suppressFocusBack:{get(){return{handleEvent:i=>{if(n(i)){let e=this.shadowRoot.querySelector("[busy-indicator-before-span]");this.__redirectFocus=!1,e.focus(),this.__redirectFocus=!0}},capture:!0,passive:!1}}},isOpenUI5Component:{get:()=>!0}}),t.__suppressFocusIn=function(){let e=this.shadowRoot?.querySelector("[busy-indicator]");e&&this.__redirectFocus&&e.focus()},t.getDomRef=function(){if(typeof this._getRealDomRef=="function")return this._getRealDomRef();if(!this.shadowRoot||this.shadowRoot.children.length===0)return;let e=[...this.shadowRoot.children].filter(u=>!["link","style"].includes(u.localName));return e.length!==1&&console.warn(`The shadow DOM for ${this.constructor.getMetadata().getTag()} does not have a top level element, the getDomRef() method might not work as expected`),this.__isBusy?e[0].querySelector(".busy-indicator-wrapper > :not([busy-indicator-before-span]):not(.busy-indicator-overlay):not(.busy-indicator-busy-area)"):e[0]}}static getBusyIndicatorStyles(){return c}};o("OpenUI5Enablement",r);var f=r;export{f as default};
