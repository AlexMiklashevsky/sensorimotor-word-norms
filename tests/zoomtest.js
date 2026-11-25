// Browser test of the web page (docs/index.html); prints what it checks and fails if the page reports errors.
const {chromium}=require('playwright');require('./offline');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1300,height:1000}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+require('path').resolve(__dirname,'../docs/index.html'));await p.waitForTimeout(500);
const box=await (await p.$('svg#g')).boundingBox();
await p.mouse.move(box.x+box.width*0.42,box.y+box.height*0.55);
for(let i=0;i<2;i++){await p.mouse.wheel(0,-250);await p.waitForTimeout(60)}
await p.waitForTimeout(300);await p.screenshot({path:'z1.png'});
await p.mouse.down();await p.mouse.move(box.x+box.width*0.42+150,box.y+box.height*0.55+60,{steps:8});await p.mouse.up();await p.waitForTimeout(200);
await p.screenshot({path:'z2.png'});
await p.click('svg#g g[aria-label="Lynott et al. (2020)"]').catch(e=>errs.push('click '+e.message));await p.waitForTimeout(200);
const pin=await p.textContent('#panel h3');await p.click('#zreset');await p.screenshot({path:'z3.png'});
console.log(errs,pin);await b.close();if(errs.length)process.exitCode=1})();
