# "Planning a study" tab: guided choices -> similar datasets (ranked by closeness), example instructions (ranked per category), documentation sheet
import json as _j2, re as _re2, sys as _sys
_sys.path.insert(0,ROOT+'/net'); from dims import dim as _dim
_R=[r for r in _j2.load(open(ROOT+'/work/records.json')) if not r.get('_excluded')]
_S=_j2.load(open(ROOT+'/work/scales/all2.json')); _C={(c['key'],c['scale']):c for c in _j2.load(open(ROOT+'/facets/coded2.json'))}
_ids={n['id'] for n in nodes}
_persp={r['_key']:r['_v3'].get('Perspective','') for r in _R}
def _clean(x,n):
    x=_re2.sub(r'\s+',' ',x or '').strip()
    for a,b in [('“','"'),('”','"'),('’',"'"),('‘',"'"),('–','-'),('—','-')]: x=x.replace(a,b)
    return x if len(x)<=n else x[:n-3].rsplit(' ',1)[0]+' ...'
# example pool: one entry per paper and wording; identical wordings of one paper are merged and list all their dimensions
_ex={}
for s in _S:
    w=(s.get('wording') or '').strip(); wt=s.get('wtype') or ''
    if not wt.startswith('verbatim') or len(w)<25: continue
    lab=s['key'].split('|')[0]
    if lab not in _ids: continue
    c=_C.get((s['key'],s['scale']),{})
    dd=[f"{k}|{_dim(k,s['scale'])}" for k in range(1,7) if c.get(f'cat{k}')=='core']
    if not dd: continue
    w2=_clean(w,280)
    if len(w2)>1 and w2[0]=='"' and w2[-1]=='"' and w2.count('"')==2: w2=w2[1:-1].strip()
    key=(lab,_re2.sub(r'[^a-z]','',w2.lower())[:200])
    e=_ex.setdefault(key,{'p':lab,'w':w2,'a':_clean(s.get('anchors'),140),'d':[],'s':[],'pp':_persp.get(s['key'],''),'tr':'translation' in wt})
    for d in dd:
        if d not in e['d']: e['d'].append(d)
    if s['scale'] not in e['s']: e['s'].append(s['scale'])
# keep one wording per paper and dimension (first one), so a paper with many near-identical wordings does not dominate
_seen=set();_pool=[]
for e in _ex.values():
    new=[d for d in e['d'] if (e['p'],d) not in _seen]
    if not new: continue
    for d in e['d']: _seen.add((e['p'],d))
    e['s']=', '.join(e['s'][:4])+(' ...' if len(e['s'])>4 else '')
    _pool.append(e)
_plan={'ex':_pool}
_PLANHTML='''<section class="tabp" id="tab-planning" role="tabpanel" hidden>
<p class="sub">Click through the choices for a new rating study. The panel next to the steps (below them on small screens) shows existing datasets ranked by how close they are to your choices; step 8 shows how similar studies worded their instructions. At the end you get a documentation sheet with the fields used in our overview table; it is also what we need to add a finished dataset to the network (see Contact). Nothing you enter leaves your browser.</p>
<div class="plan">
<div class="psteps">
<div class="pstep"><h4>1 Language of the words</h4><select id="p_lang"></select> <input id="p_lang_other" type="text" placeholder="Please specify the language" hidden></div>
<div class="pstep"><h4>2 What should raters judge?</h4><div id="p_cats" class="pchecks"></div></div>
<div class="pstep" id="p_dims_box"><h4>3 Which dimensions?</h4><p class="muted pnote">Dimensions rated in existing datasets (number of papers).</p><div id="p_dims" class="pchecks"></div><input id="p_dims_other" type="text" placeholder="Other dimensions, e.g., hardness, sweetness"></div>
<div class="pstep"><h4>4 Perspective: whose experience?</h4><div id="p_pp" class="pchecks"></div><input id="p_pp_other" class="pother" type="text" placeholder="Please specify: whose experience? e.g., an expert" hidden></div>
<div class="pstep"><h4>5 Raters</h4><div id="p_rg" class="pchecks"></div><input id="p_rg_other" class="pother" type="text" placeholder="Please specify the rater group" hidden><div id="p_human"><label class="pinl psep">Rater population - further details (country, recruitment, age...) <input id="p_pop" type="text"></label><label class="pinl psep">Planned ratings per item <input id="p_rpi" type="number" min="1" step="1" placeholder="e.g., 20"></label></div><div id="p_llm" hidden><label class="pinl psep">Model(s) and version <input id="p_model" type="text" placeholder="e.g., GPT-4o (2024-08-06), Llama 3.1 70B"></label><label class="pinl psep">Settings <input id="p_set" type="text" placeholder="e.g., temperature 0, prompt language, date of generation"></label><label class="pinl psep">Runs per item <input id="p_runs" type="number" min="1" step="1" placeholder="e.g., 10"></label></div></div>
<div class="pstep"><h4>6 Items</h4><div id="p_pos" class="pchecks"></div><input id="p_pos_other" class="pother" type="text" placeholder="Please specify the parts of speech" hidden><label class="pinl psep">Number of items <input id="p_n" type="number" min="1" step="1" placeholder="e.g., 1000"></label> <span id="p_nbin" class="muted"></span><label class="pinl psep">Item type and selection <input id="p_itype" type="text" placeholder="e.g., concrete nouns from a frequency list"></label></div>
<div class="pstep"><h4>7 Rating scale</h4>
<div class="prec"><b>Our recommendation:</b> the Lancaster format (Lynott et al., 2020): a 0-5 scale with 0 = "not experienced at all" and 5 = "experienced greatly", plus a "Don't know the meaning of this word" box. In particular, we recommend
<ul><li>a 0 point meaning "not at all", so raters can say that a word has no link to the dimension rather than a weak one;</li><li>a "don't know the word" option, so unknown words are not rated by guessing and word knowledge can be reported.</li></ul>
<span class="muted">General good practice: label at least the endpoints of the scale.</span></div>
<div id="p_sc" class="pchecks"></div><input id="p_sc_other" class="pother" type="text" placeholder="Please specify the scale, e.g., 1-10 slider" hidden><label class="pinl psep">Anchors <input id="p_anch" type="text" placeholder="e.g., 0 = not experienced at all, 5 = experienced greatly"></label><label class="pinl psep" id="p_dk_lab"><input id="p_dk" type="checkbox" checked> Include a "don't know the word" option</label></div>
<div class="pstep"><h4>8 Instruction wording</h4><p class="muted pnote">How similar studies worded their instructions: up to 3 examples per category, closest to your choices first (verbatim where the paper prints it).</p><div id="p_ex" class="plist pexbox"></div><label class="pinl psep">Your planned instruction wording (per scale) <textarea id="p_instr" rows="4"></textarea></label></div>
<div class="pstep"><h4>9 Data</h4><p class="muted pnote">What data will be provided?</p><div id="p_dprov" class="pchecks"><label><input type="checkbox" value="trial-level data (each single rating)"> trial-level data (each single rating)</label><label><input type="checkbox" value="mean per item"> mean per item</label><label><input type="checkbox" value="SD per item"> SD per item</label><label><input type="checkbox" value="number of ratings per item"> number of ratings per item</label><label><input type="checkbox" value="proportion of &quot;don&#x27;t know&quot; responses per item"> proportion of "don't know" responses per item</label><label><input type="checkbox" value="other (please specify)"> other (please specify)</label></div><input id="p_dprov_other" class="pother" type="text" placeholder="Please specify the other data" hidden><label class="pinl psep">Other variables collected <input id="p_ovar" type="text" placeholder="e.g., imageability, concreteness, age of acquisition"></label></div>
<div class="pstep"><h4>10 Study details (optional)</h4><label class="pinl">Authors <input id="p_auth" type="text"></label><label class="pinl">Title or working title <input id="p_title" type="text"></label><label class="pinl">Year / status <input id="p_year" type="text" placeholder="e.g., 2027, in preparation"></label><label class="pinl">Paper or preprint link <input id="p_plink" type="text"></label><label class="pinl">Data link <input id="p_dlink" type="text"></label><label class="pinl">Comments <textarea id="p_comm" rows="3"></textarea></label></div>
</div>
<div class="pside">
<h4>Similar datasets</h4><p id="p_note" class="muted"></p><div id="p_list" class="plist"></div>
</div>
</div>
<h3 class="fh">Documentation sheet</h3>
<p class="muted">Generated from your choices; you can edit it here before downloading.</p>
<textarea id="p_sheet" rows="24" spellcheck="false"></textarea>
<p><button id="p_dl" class="fbtn">Download as text file</button> <button id="p_cp" class="fbtn">Copy</button> <span id="p_msg" class="muted"></span></p>
</section>'''
_a='<section class="tabp" id="tab-references"'
assert t.count(_a)==1; t=t.replace(_a,_PLANHTML+'\n'+_a,1)
_a='<button role="tab" data-t="references"'
t=t.replace(_a,'<button role="tab" data-t="planning" aria-selected="false">Planning a study</button>'+_a,1)
t=t.replace("const TABS=['network','details','table','references','contact'];","const TABS=['network','details','table','planning','references','contact'];")
t=t.replace('.lbl{','''.plan{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:18px;align-items:start}
@media (max-width:900px){.plan{grid-template-columns:1fr}}
.pstep{border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin:0 0 10px}
.pstep h4,.pside h4{margin:0 0 8px;font-size:14px}
.pside{position:sticky;top:8px;max-height:calc(100vh - 16px);overflow:auto;border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.pchecks label{display:inline-flex;gap:5px;align-items:center;margin:0 12px 6px 0;font-size:13px}
.pchecks .pdesc{color:var(--text-secondary);font-size:12px}
#p_cats label,#p_pp label{display:block;margin:0 0 6px}
#p_cats input,#p_pp input{vertical-align:-2px;margin:0 6px 0 0}
.pchecks .pgrp{font-size:12px;font-weight:600;margin:6px 0 2px;color:var(--text-secondary)}
.pnote{margin:0 0 6px;font-size:12px}
.prec{font-size:13px;background:var(--surface-2,rgba(0,0,0,.03));border-radius:8px;padding:8px 10px;margin:0 0 8px}
.prec ul{margin:4px 0 4px 18px;padding:0}
.pinl{display:block;font-size:13px;margin:6px 0 0}
.psep{border-top:1px solid var(--line);margin-top:12px;padding-top:10px;font-weight:600}
.pinl input[type=text],.pinl input[type=number],.pinl textarea,#p_pp_other,#p_dims_other{display:block;width:100%;box-sizing:border-box;font:inherit;font-size:13px;padding:4px 6px;margin-top:4px;border:1px solid var(--line);border-radius:6px;background:var(--surface-1);color:var(--text-primary)}
#p_lang,#p_lang_other{font:inherit;font-size:13px;padding:3px 6px}
.pother{display:block;width:100%;box-sizing:border-box;font:inherit;font-size:13px;padding:4px 6px;margin-top:4px;border:1px solid var(--line);border-radius:6px;background:var(--surface-1);color:var(--text-primary)}
.pother[hidden],#p_lang_other[hidden],#p_human[hidden],#p_llm[hidden],#p_dk_lab[hidden],#p_dprov label[hidden]{display:none}
.plist{font-size:13px;margin:0 0 12px}
.plist .pi{padding:5px 0;border-top:1px solid var(--line)}
.plist .pi:first-child{border-top:none}
.pexbox{max-height:420px;overflow:auto;margin-bottom:0}
.plist .pk{font-size:12px;font-weight:600;color:var(--text-secondary);margin:8px 0 2px}
.ptag{font-size:12px;color:var(--text-secondary)}
#p_sheet{width:100%;box-sizing:border-box;font:12px/1.4 ui-monospace,Menlo,Consolas,monospace;padding:8px;border:1px solid var(--line);border-radius:8px;background:var(--surface-1);color:var(--text-primary)}
.lbl{''',1)
_js=r'''// planning tab
const PLAN=__PLAN__;
(function(){
const $=id=>document.getElementById(id);
const NB_=Object.fromEntries(N.map(n=>[n.id,n]));
const CATN={1:'Global sensory experience',2:'Experience per sense',3:'Perceptual features',4:'Bodily involvement (no body part named)',5:'Specific body part / effector',6:'Body-object interaction'};
const CATD={1:'one overall rating of sensory experience (SER)',2:'a separate rating per sense',3:'specific features such as color, motion, loudness, weight',4:'how much the meaning involves the body or movement in general',5:'which body part an action involves',6:'how easily a body can physically interact with the referent (BOI)'};
const PPS=[['own','the rater\'s own experience'],['typical person','a generic person or body'],['child','a typical child'],['possible vs. actual','whether it can be experienced vs. how often the rater did'],['not specified','no experiencer named'],['other','']];
const RGS=['general adults','L2 bilinguals','older adults','children','clinical','LLM','other'];
const POSS=['Nouns','Verbs','Adjectives','Mixed','Other'];
const langs={};N.forEach(n=>n.language.split(' / ').forEach(l=>langs[l]=(langs[l]||0)+1));
$('p_lang').innerHTML='<option value="">Choose ...</option>'+Object.keys(langs).sort().map(l=>`<option value="${l}">${l} (${langs[l]} existing)</option>`).join('')+'<option value="__other">other (please specify)</option>';
const cnt=(f,v)=>N.filter(n=>(n[f]||[]).includes(v)).length;
const catCnt=k=>N.filter(n=>n.pie.some(p=>p[0]===k)).length;
$('p_cats').innerHTML=[1,2,3,4,5,6].map(k=>`<label><input type="checkbox" value="${k}"> ${k} ${CATN[k]} <span class="pdesc">(${catCnt(k)}; ${CATD[k]})</span></label>`).join('');
$('p_pp').innerHTML=PPS.map(([v,d])=>`<label><input type="radio" name="p_pp" value="${v}"> ${v==='other'?'other (please specify)':v+' <span class="pdesc">('+cnt('f_pp',v)+'; '+d+')</span>'}</label>`).join('');
$('p_rg').innerHTML=RGS.map(v=>`<label><input type="radio" name="p_rg" value="${v}"> ${v==='other'?'other (please specify)':(v==='LLM'?'LLM (model-generated ratings)':v)+' <span class="pdesc">('+cnt('f_rg',v)+')</span>'}</label>`).join('');
$('p_pos').innerHTML=POSS.map(v=>`<label><input type="radio" name="p_pos" value="${v}"> ${v==='Other'?'other (please specify)':v} <span class="pdesc">(${cnt('f_pos',v)})</span></label>`).join('');
const scc={};N.forEach(n=>(n.f_scale||[]).forEach(s=>scc[s]=(scc[s]||0)+1));
const grad=Object.keys(scc).filter(s=>/\d/.test(s)&&scc[s]>1).sort((a,b)=>scc[b]-scc[a]);
const catf=['yes/no','select all that apply'].filter(s=>scc[s]);
$('p_sc').innerHTML=[...grad,...catf].map(s=>`<label><input type="radio" name="p_sc" value="${s}"${s==='0-5'?' checked':''}> ${s} <span class="pdesc">(${scc[s]})</span></label>`).join('')+'<label><input type="radio" name="p_sc" value="other"> other (please specify)</label>';
// dimensions per category, from the data
const dimc={};N.forEach(n=>(n.f_dim||[]).forEach(d=>dimc[d]=(dimc[d]||0)+1));
const NB=[[30,99,'30-99'],[100,299,'100-299'],[300,999,'300-999'],[1000,2999,'1,000-2,999'],[3000,9999,'3,000-9,999'],[10000,1e12,'10,000+']];
const lab=d=>d.split('|')[1].replace(/^(visual|touch\/body|sound): /,'');
const g=n=>{const x=document.querySelector(`input[name=${n}]:checked`);return x?x.value:''};
const sel=()=>{const cats=[...document.querySelectorAll('#p_cats input:checked')].map(x=>+x.value);
 const dims=[...document.querySelectorAll('#p_dims input:checked')].map(x=>x.value);
 const lang=$('p_lang').value==='__other'?$('p_lang_other').value.trim():$('p_lang').value;
 const n=+$('p_n').value||0;const bin=n?(NB.find(b=>n>=b[0]&&n<=b[1])||[0,0,'fewer than 30'])[2]:'';
 return {lang,cats,dims,dimo:$('p_dims_other').value.trim(),pp:g('p_pp'),ppo:$('p_pp_other').value.trim(),rg:g('p_rg'),rgo:$('p_rg_other').value.trim(),pos:g('p_pos'),poso:$('p_pos_other').value.trim(),sc:g('p_sc'),sco:$('p_sc_other').value.trim(),n,bin,rpi:$('p_rpi').value,anch:$('p_anch').value.trim(),dk:$('p_dk').checked,model:$('p_model').value.trim(),set:$('p_set').value.trim(),runs:$('p_runs').value,
  auth:$('p_auth').value.trim(),title:$('p_title').value.trim(),pop:$('p_pop').value.trim(),instr:$('p_instr').value.trim(),plink:$('p_plink').value.trim(),dlink:$('p_dlink').value.trim(),itype:$('p_itype').value.trim(),year:$('p_year').value.trim(),dprov:[...document.querySelectorAll('#p_dprov input:checked')].map(x=>x.value),dprovo:$('p_dprov_other').value.trim(),ovar:$('p_ovar').value.trim(),comm:$('p_comm').value.trim()}};
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');
function dimsUI(s){const prev=new Set(s.dims);let h='';
 s.cats.forEach(k=>{const ds=Object.keys(dimc).filter(d=>d.startsWith(k+'|')&&!d.endsWith('|other')).sort((a,b)=>dimc[b]-dimc[a]||a.localeCompare(b));
  if(!ds.length)return;h+=`<div class="pgrp">${k} ${CATN[k]}</div>`;
  if(k===3){['visual','touch/body','sound'].forEach(gr=>{const gg=ds.filter(d=>d.split('|')[1].startsWith(gr+':'));if(gg.length)h+=`<div class="pdesc">${gr}</div>`+gg.map(d=>`<label><input type="checkbox" value="${d}"${prev.has(d)?' checked':''}> ${esc(lab(d))} <span class="pdesc">(${dimc[d]})</span></label>`).join('')})}
  else h+=ds.map(d=>`<label><input type="checkbox" value="${d}"${prev.has(d)?' checked':''}> ${esc(lab(d))} <span class="pdesc">(${dimc[d]})</span></label>`).join('')});
 $('p_dims').innerHTML=h||'<span class="muted">Choose one or more categories in step 2.</span>'}
// closeness of a dataset to the choices
function crit(s){const C=[];
 if(s.cats.length)C.push(['category',n=>n.pie.some(p=>s.cats.includes(p[0])),n=>'category '+n.pie.map(p=>p[0]).join(', ')]);
 if(s.dims.length)C.push(['dimension',n=>s.dims.some(d=>(n.f_dim||[]).includes(d)),n=>'other dimensions']);
 if(s.lang)C.push([s.lang,n=>n.language.split(' / ').includes(s.lang),n=>n.language]);
 if(s.pp&&s.pp!=='other')C.push([s.pp,n=>(n.f_pp||[]).includes(s.pp),n=>(n.f_pp||[]).join(', ')]);
 if(s.rg&&s.rg!=='other')C.push([s.rg,n=>(n.f_rg||[]).includes(s.rg),n=>(n.f_rg||[]).join(', ')]);
 if(s.pos)C.push([s.pos,n=>(n.f_pos||[]).includes(s.pos),n=>(n.f_pos||[]).join(', ')]);
 if(s.sc&&s.sc!=='other')C.push(['scale '+s.sc,n=>(n.f_scale||[]).includes(s.sc),n=>'scale '+((n.f_scale||[]).join(', ')||'not stated')]);
 return C}
function upd(){const s=sel();
 $('p_lang_other').hidden=$('p_lang').value!=='__other';$('p_pp_other').hidden=s.pp!=='other';$('p_rg_other').hidden=s.rg!=='other';const llm=s.rg==='LLM';$('p_human').hidden=llm;$('p_llm').hidden=!llm;$('p_dk_lab').hidden=llm;document.querySelectorAll('#p_dprov input').forEach(x=>{if(/don't know/.test(x.value))x.closest('label').hidden=llm});$('p_pos_other').hidden=s.pos!=='Other';$('p_sc_other').hidden=s.sc!=='other';$('p_dprov_other').hidden=!s.dprov.includes('other (please specify)');
 dimsUI(s);s.dims=[...document.querySelectorAll('#p_dims input:checked')].map(x=>x.value);
 $('p_nbin').textContent=s.bin?'Size group: '+s.bin+' ('+N.filter(n=>(n.f_nb||[]).includes(s.bin)).length+' existing papers)':'';
 const C=crit(s);
 const sc=N.map(n=>{const ok=C.map(c=>c[1](n));const dm=s.dims.filter(d=>(n.f_dim||[]).includes(d));return {n,ok,k:ok.filter(Boolean).length,dm}});
 sc.sort((a,b)=>b.k-a.k||b.dm.length-a.dm.length||b.n.cited_by-a.n.cited_by||b.n.year-a.n.year);
 const full=sc.filter(x=>x.k===C.length).length;
 $('p_note').textContent=!C.length?'Make a choice on the left; the list is then ranked by how many choices each dataset shares.':(full?full+' of '+N.length+' datasets match all your choices; the closest are listed first.':'No dataset matches all your choices; the closest are listed first.');
 $('p_list').innerHTML=sc.slice(0,15).map(x=>{const n=x.n;const m=C.filter((c,i)=>x.ok[i]&&c[0]!=='category'&&c[0]!=='dimension').map(c=>c[0]);const d=C.filter((c,i)=>!x.ok[i]&&c[0]!=='dimension').map(c=>c[2](n));
  return `<div class="pi"><b>${esc(n.id)}</b> - ${esc(n.language)}; ${n.n_items&&n.n_items.length?n.n_items.map(v=>v.toLocaleString('en-US')).join(', ')+' items':'items not stated'}${n.link?` - <a href="${n.link}" target="_blank" rel="noopener">paper</a>`:''}`+
  (x.dm.length?`<br><span class="ptag">covers: ${esc(x.dm.map(lab).join(', '))}</span>`:'')+(m.length?`<br><span class="ptag">matches: ${esc(m.join(', '))}</span>`:'')+(d.length?`<br><span class="ptag">differs (theirs): ${esc(d.join('; '))}</span>`:'')+'</div>'}).join('');
 // instruction examples: best 3 per ticked category
 const blocks=s.cats.length?s.cats:[0];let h='';
 blocks.forEach(k=>{let E=PLAN.ex.filter(e=>!k||e.d.some(d=>d.startsWith(k+'|')));
  const score=e=>{const n=NB_[e.p]||{};let v=0;
   if(s.dims.some(d=>e.d.includes(d)))v+=3;
   if(s.pp&&e.pp.split('; ').includes(s.pp))v+=1;if(s.lang&&(n.language||'').split(' / ').includes(s.lang))v+=1;
   if(s.rg&&(n.f_rg||[]).includes(s.rg))v+=1;if(s.pos&&(n.f_pos||[]).includes(s.pos))v+=1;if(s.sc&&(n.f_scale||[]).includes(s.sc))v+=1;return v};
  E=E.map(e=>[score(e),e]).sort((a,b)=>b[0]-a[0]||((NB_[b[1].p]||{}).cited_by||0)-((NB_[a[1].p]||{}).cited_by||0));
  const out=[],ps=new Set();for(const [v,e] of E){if(ps.has(e.p))continue;ps.add(e.p);out.push(e);if(out.length===3)break}
  if(k)h+=`<div class="pk">${k} ${CATN[k]}</div>`;
  h+=out.map(e=>`<div class="pi">${e.w.includes('"')?esc(e.w):'"'+esc(e.w)+'"'}${e.a?`<br><span class="muted">Scale: ${esc(e.a)}</span>`:''}<br><span class="muted">${esc(e.p)}; ${esc(e.d.filter(d=>!k||d.startsWith(k+'|')).map(lab).join(', '))}${e.tr?' (English translation printed in the paper)':''}</span></div>`).join('')||'<div class="pi muted">No verbatim instruction available for this category.</div>'});
 $('p_ex').innerHTML=h;
 sheet(s)}
let edited=false;
function sheet(s){if(edited)return;const L=[];const v=x=>x||'';
 const dims=s.cats.map(k=>{const ds=s.dims.filter(d=>d.startsWith(k+'|')).map(lab);return ds.length?k+' '+CATN[k]+': '+ds.join(', '):''}).filter(Boolean).concat(s.dimo?['other: '+s.dimo]:[]).join('; ');
 const now=new Date();
 L.push('SENSORIMOTOR WORD NORMS - DOCUMENTATION SHEET','Created with "Sensorimotor word norms: an overview" on '+now.toISOString().slice(0,10),'',
 'STUDY','Authors: '+v(s.auth),'Title / publication: '+v(s.title),'Year / status: '+v(s.year),'Paper or preprint link: '+v(s.plink),'Data link: '+v(s.dlink),'',
 'WORDS','Language: '+v(s.lang),'Number of items: '+(s.n||'')+(s.bin?' (size group '+s.bin+')':''),'Parts of speech: '+(s.pos==='Other'?'other: '+s.poso:v(s.pos)),'Item type and selection (e.g., concrete nouns from a frequency list): '+v(s.itype),'',
 'RATINGS','What raters judge (category): '+s.cats.map(k=>k+' '+CATN[k]).join('; '),'Dimensions / scales: '+dims,'Perspective (whose experience): '+(s.pp==='other'?'other: '+s.ppo:v(s.pp)),
 'Rating scale: '+(s.sc==='other'?'other: '+s.sco:(s.sc||''))+(s.anch?'; anchors: '+s.anch:''),...(s.rg==='LLM'?[]:['"Don\'t know the word" option: '+(s.dk?'yes':'no')]),'Exact instruction wording (per scale):',s.instr?s.instr:'','',
 'RATERS',...(s.rg==='LLM'?['Rater group: LLM (model-generated ratings)','Model(s) and version: '+v(s.model),'Settings (e.g., temperature, prompt language, date): '+v(s.set),'Runs per item: '+v(s.runs)]:['Rater group: '+(s.rg==='other'?'other: '+s.rgo:v(s.rg)),'Rater population (country, recruitment, age): '+v(s.pop),'Ratings per item: '+v(s.rpi)]),'',
 'DATA','Data provided: '+s.dprov.filter(x=>!(s.rg==='LLM'&&/don't know/.test(x))).map(x=>x==='other (please specify)'?'other: '+s.dprovo:x).join('; '),'Other variables collected: '+v(s.ovar),'Comments: '+v(s.comm));
 $('p_sheet').value=L.join('\n')}
const tp=$('tab-planning');tp.addEventListener('input',e=>{if(e.target.id!=='p_sheet')upd()});tp.addEventListener('change',e=>{if(e.target.id!=='p_sheet')upd()});
$('p_sheet').addEventListener('input',()=>{edited=true;$('p_msg').textContent='Edited by hand; further choices no longer update the sheet.'});
$('p_dl').onclick=()=>{const b=new Blob([$('p_sheet').value],{type:'text/plain'});const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='sensorimotor_norms_documentation_sheet.txt';document.body.appendChild(a);a.click();a.remove()};
$('p_cp').onclick=()=>{const t=$('p_sheet');t.select();let ok=false;try{ok=document.execCommand('copy')}catch(e){}if(!ok&&navigator.clipboard)navigator.clipboard.writeText(t.value);$('p_msg').textContent='Copied.'};
upd()})();
'''
_js=_js.replace('__PLAN__',_j2.dumps(_plan,ensure_ascii=False,separators=(',',':')))
_a='// tabs\nconst TABS='
assert t.count(_a)==1; t=t.replace(_a,_js+_a,1)
