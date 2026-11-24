// Browser test of the web page (docs/index.html); prints what it checks and fails if the page reports errors.
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1400,height:1100}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+require('path').resolve(__dirname,'../docs/index.html')+'#planning');await p.waitForTimeout(500);
const note=async()=>p.$eval('#p_note',e=>e.textContent);
console.log('init',await note(),await p.$eval('input[name=p_sc]:checked',e=>e.value),await p.$eval('#p_dk',e=>e.checked));
console.log('scales',await p.$$eval('#p_sc label',l=>l.map(x=>x.textContent.trim()).join(' | ')));
await p.check('#p_cats input[value="2"]');await p.check('#p_cats input[value="3"]');await p.waitForTimeout(100);
console.log('dims',(await p.$eval('#p_dims',e=>e.innerText)).replace(/\n/g,' / ').slice(0,600));
await p.check('#p_dims input[value="2|interoception"]');await p.selectOption('#p_lang','German');await p.check('input[name=p_pp][value="own"]');await p.waitForTimeout(150);
console.log(await note());
console.log((await p.$eval('#p_list',e=>e.innerText)).split('\n').slice(0,9).join('\n'));
console.log('EX:',(await p.$eval('#p_ex',e=>e.innerText)).split('\n').slice(0,14).join('\n'));
await p.check('input[name=p_pp][value="other"]');await p.fill('#p_pp_other','an expert');await p.check('input[name=p_sc][value="yes/no"]');await p.waitForTimeout(150);
console.log('yes/no top:',(await p.$eval('#p_list',e=>e.innerText)).split('\n').slice(0,4).join(' | '));
console.log((await p.$eval('#p_sheet',e=>e.value)).split('\n').filter(l=>/Dimensions|Perspective|Rating scale|know/.test(l)).join('\n'));
await p.screenshot({path:'t_plan2.png'});
console.log(errs);await b.close();if(errs.length)process.exitCode=1})();
