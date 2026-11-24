// Browser test of the web page (docs/index.html); prints what it checks and fails if the page reports errors.
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1300,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+require('path').resolve(__dirname,'../docs/index.html'));await p.waitForTimeout(500);
// zoom to max around a small multi-category node
const id=await p.evaluate(()=>{const n=N.filter(n=>n.pie&&n.pie.length>=3&&n.cited_by<=1)[0];return n.id});
for(let i=0;i<12;i++){await p.click('button:has-text("+")');await p.waitForTimeout(60)}
await p.evaluate(id=>{const n=N.find(x=>x.id===id);const [x,y]=P(n);VB.x=x-VB.w/2;VB.y=y-VB.h/2;setVB();render()},id);await p.waitForTimeout(300);
const g=await p.$$eval('svg#g g[role=button]',gs=>gs.length);
await p.screenshot({path:'zoompie.png',clip:{x:300,y:450,width:500,height:350}});console.log(id,'zoom',await p.evaluate(()=>ZZ()),errs);await b.close();if(errs.length)process.exitCode=1})();
