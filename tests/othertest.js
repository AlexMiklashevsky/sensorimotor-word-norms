// Browser test of the web page (docs/index.html); prints what it checks and fails if the page reports errors.
const {chromium}=require('playwright');require('./offline');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1400,height:1300}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+require('path').resolve(__dirname,'../docs/index.html')+'#planning');await p.waitForTimeout(400);
const vis=async id=>p.$eval('#'+id,e=>!e.hidden&&e.offsetParent!==null);
console.log('before',await vis('p_rg_other'),await vis('p_pos_other'),await vis('p_sc_other'),await vis('p_pp_other'),await vis('p_lang_other'));
await p.selectOption('#p_lang','__other');await p.fill('#p_lang_other','Basque');
await p.check('input[name=p_pp][value="other"]');await p.fill('#p_pp_other','an expert');
await p.check('input[name=p_rg][value="other"]');await p.fill('#p_rg_other','sign language users');
await p.check('input[name=p_pos][value="Other"]');await p.fill('#p_pos_other','adverbs');
await p.check('input[name=p_sc][value="other"]');await p.fill('#p_sc_other','1-10 slider');await p.waitForTimeout(150);
console.log('after',await vis('p_rg_other'),await vis('p_pos_other'),await vis('p_sc_other'),await vis('p_pp_other'),await vis('p_lang_other'));
console.log((await p.$eval('#p_sheet',e=>e.value)).split('\n').filter(l=>/Language|Parts of|Perspective|Rating scale|Rater group/.test(l)).join('\n'));
console.log(await p.$$eval('#tab-planning label',l=>l.map(x=>x.textContent.trim()).filter(t=>/other/i.test(t))));
await p.check('input[name=p_rg][value="children"]');await p.waitForTimeout(100);console.log('rg other hidden again',!(await vis('p_rg_other')));
await p.screenshot({path:'t_other.png',fullPage:true});console.log(errs);await b.close();if(errs.length)process.exitCode=1})();
