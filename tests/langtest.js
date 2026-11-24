// Browser test of the web page (docs/index.html); prints what it checks and fails if the page reports errors.
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1300,height:1000}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+require('path').resolve(__dirname,'../docs/index.html'));await p.waitForTimeout(500);
const opts=await p.$$eval('#langSel option',o=>o.map(x=>x.textContent));
await p.selectOption('#langSel','Italian');await p.waitForTimeout(300);
const vis=await p.$$eval('svg#g g[role=button]',g=>g.filter(x=>x.style.display!=='none').length);
const rows=await p.$$eval('#tbl tbody tr',r=>r.length);
await p.screenshot({path:'lang.png'});console.log(errs,opts.join(' | '),vis,rows);await b.close();if(errs.length)process.exitCode=1})();
