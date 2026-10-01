var o=new WeakMap,n=(e,s,t)=>{let r=new MutationObserver(s);o.set(e,r),r.observe(e,t)},b=e=>{let s=o.get(e);s&&(s.disconnect(),o.delete(e))};export{n as a,b};
