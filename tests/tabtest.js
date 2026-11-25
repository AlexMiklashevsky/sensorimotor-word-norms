// Browser test of the web page (docs/index.html); prints what it checks and fails if the page reports errors.
const {chromium}=require('playwright');require('./offline');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1300,height:950}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto('file://'+require('path').resolve(__dirname,'../docs/index.html'));await p.waitForTimeout(600);
const vis=async()=>p.$$eval('.tabp',s=>s.filter(x=>!x.hidden).map(x=>x.id));
const nodes=async()=>p.$$eval('svg#g g[role=button]',g=>g.filter(x=>x.style.display!=='none').length);
const rows=async()=>p.$$eval('#tbl tbody tr',r=>r.length);
console.log('start',await vis(),await nodes(),await rows());
await p.screenshot({path:'t_net.png'});
// graph filter should not affect table
await p.selectOption('#f_rg','LLM');await p.waitForTimeout(200);console.log('graph LLM',await nodes(),await rows());
await p.click('.tabs button[data-t=table]');await p.waitForTimeout(200);console.log(await vis(),p.url().split('#')[1]);
await p.selectOption('#t_f_rg','children');await p.waitForTimeout(200);console.log('table children',await rows(),await p.$eval('#tcount',e=>e.textContent),'graph still',await nodes());
await p.fill('#tq','xu');await p.waitForTimeout(150);console.log('q xu',await rows());
await p.click('#tclear');await p.$eval('#ty0',e=>{e.value=2020;e.dispatchEvent(new Event('input'))});await p.selectOption('#t_lang','Chinese');await p.waitForTimeout(150);console.log('2020+ Chinese',await rows(),await p.$eval('#tcount',e=>e.textContent));
await p.screenshot({path:'t_table.png'});
await p.click('.tabs button[data-t=details]');await p.waitForTimeout(150);console.log(await vis(),await p.$$eval('#tab-details h3.fh',h=>h.map(x=>x.textContent)));
await p.screenshot({path:'t_details.png'});
await p.click('.tabs button[data-t=references]');await p.waitForTimeout(150);console.log('refs',await p.$$eval('.refs .ref',r=>r.length));
await p.screenshot({path:'t_refs.png'});
await p.click('.tabs button[data-t=contact]');await p.waitForTimeout(150);await p.screenshot({path:'t_contact.png'});
// direct hash load
const p2=await b.newPage({viewport:{width:1300,height:950}});p2.on('pageerror',e=>errs.push('p2 '+e.message));await p2.goto('file://'+require('path').resolve(__dirname,'../docs/index.html')+'#table');await p2.waitForTimeout(500);
console.log('hash load',await p2.$$eval('.tabp',s=>s.filter(x=>!x.hidden).map(x=>x.id)));
await p2.click('.tabs button[data-t=network]');await p2.waitForTimeout(400);console.log('labels shown after switch',await p2.$$eval('svg#g text',t=>t.filter(x=>x.style.display!=='none'&&x.textContent).length));
await p2.screenshot({path:'t_net2.png'});
console.log('errors',errs);await b.close();if(errs.length)process.exitCode=1})();
