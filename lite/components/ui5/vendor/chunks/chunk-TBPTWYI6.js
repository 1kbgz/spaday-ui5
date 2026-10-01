var e=new Map,n={get:function(t){if(!e.has(t))throw new Error("Required calendar type: "+t+" not loaded.");return e.get(t)},set:function(t,r){e.set(t,r)}},o=n;export{o as a};
