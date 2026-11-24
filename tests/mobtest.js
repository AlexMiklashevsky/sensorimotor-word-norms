// Browser test of the web page (docs/index.html); prints what it checks and fails if the page reports errors.
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];
for(const t of ['network','details','table','planning','references','contact']){const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:1});p.on('pageerror',e=>errs.push(t+': '+e.message));p.on('console',m=>{if(m.type()==='error')errs.push(t+' console: '+m.text())});
 await p.goto('file://'+require('path').resolve(__dirname,'../docs/index.html')+'#'+t);await p.waitForTimeout(500);
 const ov=await p.evaluate(()=>document.documentElement.scrollWidth-window.innerWidth);
 console.log(t,'horizontal overflow px:',ov);await p.screenshot({path:`m_${t}.png`});await p.close()}
// keyboard: tab buttons focusable
const p=await b.newPage({viewport:{width:1300,height:900}});await p.goto('file://'+require('path').resolve(__dirname,'../docs/index.html'));await p.waitForTimeout(300);
const r=await p.$$eval('.tabs button',bs=>bs.map(x=>x.tabIndex));console.log('tab focusable',r);
// external links count & target
console.log('links',await p.$$eval('a[href]',a=>a.length), 'without rel noopener',await p.$$eval('a[target=_blank]:not([rel~=noopener])',a=>a.length));
console.log('errors',errs);await b.close();if(errs.length)process.exitCode=1})();
