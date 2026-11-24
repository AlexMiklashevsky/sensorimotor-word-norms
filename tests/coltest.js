// Browser test of the web page (docs/index.html); prints what it checks and fails if the page reports errors.
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1400,height:950}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+require('path').resolve(__dirname,'../docs/index.html')+'#table');await p.waitForTimeout(500);
console.log(await p.$$eval('#tbl thead th',h=>h.map(x=>x.textContent)));
await p.click('#tbl thead th[data-k=n_items]');await p.waitForTimeout(150);
console.log(await p.$$eval('#tbl tbody tr',r=>r.slice(0,3).map(x=>x.children[0].textContent+' | '+x.children[7].textContent)));
await p.click('#tbl thead th[data-k=f_pp]');await p.waitForTimeout(150);
console.log(await p.$$eval('#tbl tbody tr',r=>r.slice(0,2).map(x=>x.children[0].textContent+' | '+x.children[5].textContent)));
await p.screenshot({path:'t_table2.png'});
await p.click('.tabs button[data-t=network]');await p.waitForTimeout(400);
console.log(await p.$eval('#panel h3',e=>e.textContent));
console.log(errs);await b.close();if(errs.length)process.exitCode=1})();
