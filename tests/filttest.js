// Browser test of the web page (docs/index.html); prints what it checks and fails if the page reports errors.
const {chromium}=require('playwright');require('./offline');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1300,height:1000}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+require('path').resolve(__dirname,'../docs/index.html'));await p.waitForTimeout(500);
const cnt=async()=>[await p.$$eval('svg#g g[role=button]',g=>g.filter(x=>x.style.display!=='none').length),await p.$$eval('#tbl tbody tr',r=>r.length),await p.$eval('#fcount',e=>e.textContent)];
console.log('init',await cnt());
for(const id of ['f_rg','f_pp','f_pos','f_nb']) console.log(id,(await p.$$eval('#'+id+' option',o=>o.map(x=>x.textContent))).join(' | '));
await p.selectOption('#f_rg','LLM');await p.waitForTimeout(200);console.log('LLM',await cnt());
await p.selectOption('#f_rg','');await p.selectOption('#f_nb','10,000+');await p.waitForTimeout(200);console.log('10k',await cnt());
await p.selectOption('#f_nb','');await p.selectOption('#f_pp','child');await p.waitForTimeout(200);console.log('child',await cnt());
await p.selectOption('#f_pp','');
await p.$eval('#y0',e=>{e.value=2015;e.dispatchEvent(new Event('input'))});await p.waitForTimeout(200);console.log('2015+',await cnt(),await p.$eval('#yrLab',e=>e.textContent));
await p.$eval('#y1',e=>{e.value=2010;e.dispatchEvent(new Event('input'))});await p.waitForTimeout(200);console.log('y1<y0',await cnt(),await p.$eval('#yrLab',e=>e.textContent));
await p.$eval('#y1',e=>{e.value=2020;e.dispatchEvent(new Event('input'))});await p.selectOption('#f_pos','Verbs');await p.waitForTimeout(200);console.log('2015-2020 verbs',await cnt());
await p.screenshot({path:'filt.png'});
await p.click('#fclear');await p.waitForTimeout(200);console.log('cleared',await cnt());
console.log(errs);await b.close();if(errs.length)process.exitCode=1})();
