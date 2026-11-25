// Browser test of the web page (docs/index.html); prints what it checks and fails if the page reports errors.
const {chromium}=require('playwright');require('./offline');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1400,height:1000}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+require('path').resolve(__dirname,'../docs/index.html'));await p.waitForTimeout(500);
await p.evaluate(()=>{st.pin='Lynott et al. (2020)';panel()});
console.log((await p.$eval('#panel',e=>e.innerText)).slice(0,700));
await p.click('.tabs button[data-t=contact]');console.log(await p.$eval('#tab-contact',e=>e.innerText));
await p.click('.tabs button[data-t=references]');console.log(await p.$eval('#tab-references .sub',e=>e.innerText));
await p.click('.tabs button[data-t=table]');await p.waitForTimeout(200);
console.log(await p.$$eval('#tbl tbody tr',r=>r.slice(0,2).map(x=>[...x.children].slice(8,11).map(c=>c.innerText).join(' | '))));
console.log(errs);await b.close();if(errs.length)process.exitCode=1})();
