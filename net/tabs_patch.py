# v18: five tabs (Interactive network, Details, Table, References, Contact); table has its own filters
import json as _j, datetime as _dt
_REF=_j.load(open(ROOT+'/refs/references.json'))
_refs_html=''.join(f'<p class="ref">{_REF["html"][l]}</p>' for l in _REF['order'])
def _seg(a,b): i=t.index(a); j=t.index(b,i); return t[i:j]
_net=_seg('<p class="sub">','<h2>What the network shows</h2>')
_old=_seg('<p class="sub">','</div>\n</body>') if '</div>\n</body>' in t else None
_start=t.index('<p class="sub">'); _end=t.index('<div id="method"></div>')+len('<div id="method"></div>')
_tfilters='''<div class="controls" id="tfilters"><span class="lbl" style="font-weight:600">Filters</span>
 <input type="search" id="tq" placeholder="Find a paper (e.g., Lynott)">
 <span><span class="lbl">Language</span><select id="t_lang"></select></span>
 <span><span class="lbl">Category</span><select id="t_cat"></select></span>
 <span><span class="lbl">Years</span><span class="yr"><input type="range" id="ty0" aria-label="From year"><input type="range" id="ty1" aria-label="To year"></span> <span id="tyrLab" class="yrlab"></span></span>
 <span><span class="lbl">Rater group</span><select id="t_f_rg"></select></span>
 <span><span class="lbl">Perspective</span><select id="t_f_pp"></select></span>
 <span><span class="lbl">Part of speech</span><select id="t_f_pos"></select></span>
 <span><span class="lbl">N of items</span><select id="t_f_nb"></select></span>
 <button id="tclear" class="fbtn">Clear filters</button> <span id="tcount" class="lbl"></span>
</div>'''
from zoneinfo import ZoneInfo as _ZI
_now=_dt.datetime.now(_ZI('Europe/Berlin')); _stamp=_now.strftime('%Y-%m-%d, %H:%M')+' ('+_now.strftime('%Z')+')'
_body=f'''<nav class="tabs" role="tablist" aria-label="Sections">
 <button role="tab" data-t="network" aria-selected="true">Interactive network</button><button role="tab" data-t="details" aria-selected="false">Details</button><button role="tab" data-t="table" aria-selected="false">Table</button><button role="tab" data-t="references" aria-selected="false">References</button><button role="tab" data-t="contact" aria-selected="false">Contact</button>
</nav>
<section class="tabp" id="tab-network" role="tabpanel">
{_net}<div class="cards" id="cards"></div>
</section>
<section class="tabp" id="tab-details" role="tabpanel" hidden>
<div id="findings"></div>
<h3 class="fh">Method</h3>
<div id="method"></div>
</section>
<section class="tabp" id="tab-table" role="tabpanel" hidden>
<p class="sub">One row per paper in the interactive network. Click a column header to sort. The filters here work independently of the network filters.</p>
{_tfilters}
<div class="tablewrap"><table id="tbl"><thead></thead><tbody></tbody></table></div>
</section>
<section class="tabp" id="tab-references" role="tabpanel" hidden>
<p class="sub">All papers in the interactive network and the table, in APA style. Labels such as "Shao et al. (2025a)" match the entries below.</p>
<div class="refs">{_refs_html}</div>
</section>
<section class="tabp" id="tab-contact" role="tabpanel" hidden>
<h3 class="fh" style="border-top:none;padding-top:0;margin-top:4px">Didn't find your study?</h3>
<p>Contact us and attach the documentation sheet from the Planning a study tab (or ask us for a short form). After a check, the study will be added to the network and the table in the next update.</p>
<h3 class="fh">Contact</h3>
<p>Alex Miklashevsky, University of Potsdam<br><a href="#" id="mailme" data-u="armanster31" data-d="gmail.com">armanster31 [at] gmail [dot] com</a> <span class="muted">(click to write an email)</span></p>
<h3 class="fh">How to cite</h3>
<p>Miklashevsky, A., Ulianova, T., &amp; Platonova, O. (in prep.). Sensorimotor word norms: An overview.</p>
<h3 class="fh">License</h3>
<p>Data (overview table, citation network, codings and references): <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC BY 4.0</a>, please cite as above. Code: <a href="https://opensource.org/license/mit" target="_blank" rel="noopener">MIT License</a>.</p>
<h3 class="fh">Last update</h3>
<p>{_stamp}</p>
</section>'''
t=t[:_start]+_body+t[_end:]
t=t.replace('.lbl{','''.tabs{display:flex;flex-wrap:wrap;gap:4px;border-bottom:1px solid #c9c6bd;padding-left:4px;margin:6px 0 16px}
.tabs button{font:inherit;font-size:14px;padding:8px 16px;border:1px solid #c9c6bd;border-bottom:none;border-radius:8px 8px 0 0;background:#efede8;color:var(--text-primary);cursor:pointer;margin-bottom:-1px;line-height:1.2}
.tabs button:hover{background:#e4e2dc}
.tabs button[aria-selected="true"]{background:var(--surface-1,#fcfcfb);font-weight:600;border-bottom:1px solid var(--surface-1,#fcfcfb)}
.tabs button:focus-visible{outline:2px solid var(--text-primary);outline-offset:2px}
@media (prefers-color-scheme:dark){:root:where(:not([data-theme="light"])) .tabs button{background:#2c2c2a;border-color:#4a4a46}:root:where(:not([data-theme="light"])) .tabs button:hover{background:#363633}:root:where(:not([data-theme="light"])) .tabs button[aria-selected="true"]{background:var(--surface-1);border-bottom-color:var(--surface-1)}}
:root[data-theme="dark"] .tabs button{background:#2c2c2a;border-color:#4a4a46}:root[data-theme="dark"] .tabs button:hover{background:#363633}:root[data-theme="dark"] .tabs button[aria-selected="true"]{background:var(--surface-1);border-bottom-color:var(--surface-1)}
.tabp[hidden]{display:none}
.refs .ref{margin:0 0 8px;padding-left:2em;text-indent:-2em;max-width:980px}
.refs a{overflow-wrap:anywhere}
.viz-root{min-height:100vh}
#tab-table .tablewrap{max-height:none}
.lbl{''',1)
# table uses its own filter state
_a="const rows=N.filter(n=>(!st.lang||n.language.split(' / ').includes(st.lang))&&passF(n))"
assert t.count(_a)==1; t=t.replace(_a,"const rows=N.filter(tpass)")
_a="table();render();panel();\n</script>"
assert t.count(_a)==1
t=t.replace(_a,r'''// table filters (independent of the network filters)
const TS={lang:'',cat:'',f:{},y0:YMIN,y1:YMAX,q:''};
const hasCat=(n,k)=>n.pie&&n.pie.length?n.pie.some(([c])=>c===k):CL.indexOf(n.cluster)+1===k;
function tpass(n){return (!TS.lang||n.language.split(' / ').includes(TS.lang))&&(!TS.cat||hasCat(n,+TS.cat))&&n.year>=TS.y0&&n.year<=TS.y1&&FKEYS.every(k=>!TS.f[k]||(n[k]||[]).includes(TS.f[k]))&&(!TS.q||n.id.toLowerCase().includes(TS.q))}
function tcount(){const k=N.filter(tpass).length,a=TS.lang||TS.cat||TS.q||TS.y0>YMIN||TS.y1<YMAX||FKEYS.some(x=>TS.f[x]);document.getElementById('tcount').textContent=a?k+' of '+N.length+' papers shown':''}
document.getElementById('t_lang').innerHTML=document.getElementById('langSel').innerHTML;
document.getElementById('t_lang').onchange=e=>{TS.lang=e.target.value;table();tcount()};
document.getElementById('t_cat').innerHTML='<option value="">All categories</option>'+CL.map((c,i)=>`<option value="${i+1}">${c} (${N.filter(n=>hasCat(n,i+1)).length})</option>`).join('');
document.getElementById('t_cat').onchange=e=>{TS.cat=e.target.value;table();tcount()};
FKEYS.forEach(k=>{const s=document.getElementById('t_'+k);s.innerHTML=document.getElementById(k).innerHTML;s.value='';s.onchange=e=>{TS.f[k]=e.target.value;table();tcount()}});
const ty0=document.getElementById('ty0'),ty1=document.getElementById('ty1'),tyl=document.getElementById('tyrLab');
[ty0,ty1].forEach(s=>{s.min=YMIN;s.max=YMAX;s.step=1});ty0.value=YMIN;ty1.value=YMAX;tyl.textContent=YMIN+'-'+YMAX;
function tyr(e){let a=+ty0.value,b=+ty1.value;if(a>b){if(e.target===ty0){a=b;ty0.value=a}else{b=a;ty1.value=b}}TS.y0=a;TS.y1=b;ty0.style.zIndex=a>=YMAX-1?3:1;tyl.textContent=a+'-'+b;table();tcount()}
ty0.oninput=tyr;ty1.oninput=tyr;
document.getElementById('tq').oninput=e=>{TS.q=e.target.value.trim().toLowerCase();table();tcount()};
document.getElementById('tclear').onclick=()=>{TS.lang='';TS.cat='';document.getElementById('t_cat').value='';TS.q='';TS.f={};TS.y0=YMIN;TS.y1=YMAX;document.getElementById('t_lang').value='';document.getElementById('tq').value='';FKEYS.forEach(k=>document.getElementById('t_'+k).value='');ty0.value=YMIN;ty1.value=YMAX;tyl.textContent=YMIN+'-'+YMAX;table();tcount()};
// tabs
const TABS=['network','details','table','references','contact'];
function showTab(id,push){if(!TABS.includes(id))id='network';document.querySelectorAll('.tabp').forEach(s=>s.hidden=s.id!=='tab-'+id);document.querySelectorAll('.tabs button').forEach(b=>b.setAttribute('aria-selected',String(b.dataset.t===id)));if(push&&history.replaceState)history.replaceState(null,'','#'+id);if(id==='network')render()}
document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>showTab(b.dataset.t,true));
window.addEventListener('hashchange',()=>showTab(location.hash.slice(1)));
table();tcount();render();panel();showTab(location.hash.slice(1)||'network');
</script>''')
# v20: side panel renamed; table gets the filter dimensions as columns
t=t.replace('<h3>Details</h3>','<h3>Selected paper</h3>')
for _a,_b in [("click it to pin the details.","click it to show it in the Selected paper panel."),
  ("['cluster','Main category'],","['cluster','Main category'],['f_rg','Rater group'],['f_pp','Perspective'],['f_pos','Part of speech'],['n_items','N of items'],"),
  ("typeof N[0][k]==='number'?-1:1","(typeof N[0][k]==='number'||k==='n_items')?-1:1"),
  ("const x=a[sortK]??-1,y=b[sortK]??-1;","const sv=n=>{const v=n[sortK];return Array.isArray(v)?(sortK==='n_items'?(v.length?Math.max(...v):-1):v.join(', ')):(v??-1)};const x=sv(a),y=sv(b);"),
  ("+n.rater+'</span>':''}</td>","+n.rater+'</span>':''}</td><td>${(n.f_rg||[]).join(', ')}</td><td>${(n.f_pp||[]).join(', ')}</td><td>${(n.f_pos||[]).join(', ')}</td><td class=\"n\">${(n.n_items||[]).length?n.n_items.map(x=>x.toLocaleString('en-US')).join(', '):'<span class=\"muted\">not stated</span>'}</td>")]:
    assert t.count(_a)==1,(_a,t.count(_a)); t=t.replace(_a,_b)

# v21: more table columns (Study type, Rating scale, Ratings per item); panel shows rated variables and rater population
for _a,_b in [("['n_items','N of items'],","['n_items','N of items'],['f_st','Study type'],['f_scale','Rating scale'],['rpi','Ratings per item'],"),
  ("):'<span class=\"muted\">not stated</span>'}</td>","):'<span class=\"muted\">not stated</span>'}</td><td>${(n.f_st||[]).join(', ')}</td><td>${(n.f_scale||[]).join(', ')||'<span class=\"muted\">not stated</span>'}</td><td>${(n.rpi||[]).map(x=>x.replace(/</g,'&lt;')).join('; ')||'<span class=\"muted\">not stated</span>'}</td>"),
  ('Paper link</a></p>`:\'\'}','Paper link</a></p>`:\'\'}${(n.vars||[]).length?`<p class="muted" style="margin:4px 0"><b>Rated variables:</b> ${n.vars.map(x=>x.replace(/</g,"&lt;")).join(" | ")}</p>`:""}${(n.pop||[]).length?`<p class="muted" style="margin:4px 0"><b>Rater population:</b> ${n.pop.map(x=>x.replace(/</g,"&lt;")).join(" | ")}</p>`:""}')]:
    assert t.count(_a)==1,(_a[:60],t.count(_a)); t=t.replace(_a,_b)

# v24: citation communities get their own colors (--k1..--k5), distinct from the category colors (--c1..--c6) and from not assigned (gray): palette chosen by the author (11 hues: odd = categories, even = communities)
t=t.replace('--c7:#8a8984','--c7:#8a8984;--k1:#6836a9;--k2:#a93677;--k3:#a96836;--k4:#77a936;--k5:#36a968')
assert t.count('--k1:#6836a9')>=1
for _a,_b in [("return n.community?`var(--c${COMMS.indexOf(n.community)+1})`","return n.community?`var(--k${Math.min(COMMS.indexOf(n.community)+1,5)})`"),
  ('<circle r="5" fill="var(--c${i+1})"/></svg>Commu','<circle r="5" fill="var(--k${Math.min(i+1,5)})"/></svg>Commu')]:
    assert t.count(_a)==1,(_a,t.count(_a)); t=t.replace(_a,_b)

# v28: page metadata, icon, e-mail assembled on click (keeps the address away from simple harvesters)
t=t.replace('<meta charset="utf-8">','<meta charset="utf-8">\n<meta name="description" content="Interactive overview of sensorimotor word norm datasets across languages: citation network, categories of rating scales, searchable table, references and a guide for planning new rating studies.">\n<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27%3E%3Ccircle cx=%274%27 cy=%2711%27 r=%273%27 fill=%27%23363ea9%27/%3E%3Ccircle cx=%2712%27 cy=%2711%27 r=%273%27 fill=%27%23a136a9%27/%3E%3Ccircle cx=%278%27 cy=%274%27 r=%273%27 fill=%27%23a9363e%27/%3E%3C/svg%3E">',1)
_a="// tabs\nconst TABS="
assert t.count(_a)==1
t=t.replace(_a,"(function(){const m=document.getElementById('mailme');if(m)m.onclick=e=>{e.preventDefault();location.href='mailto:'+m.dataset.u+'@'+m.dataset.d}})();\n"+_a,1)
# v29: slice outlines scale with zoom (fixed-width white outlines covered small pies when zoomed in)
_a="'stroke-width':sl.length>1?1:0.8},g)"
assert t.count(_a)==1; t=t.replace(_a,"'stroke-width':Math.min((sl.length>1?1:0.8)/ZZ(),r*0.12)},g)")
# v36: visitor statistics with GoatCounter (cookie-free); site code in site_config.json, nothing added while it is empty
import json as _json, os as _os, re as _re
_cfg=_json.load(open(_os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),'site_config.json'),encoding='utf-8'))
_gc=(_cfg.get('goatcounter_code') or '').strip()
if _gc:
    assert _re.fullmatch(r'[a-z0-9-]+',_gc), 'goatcounter_code: lowercase letters, digits and hyphens only'
    _a='<h3 class="fh">Last update</h3>'
    assert t.count(_a)==1
    t=t.replace(_a,'<h3 class="fh">Visitor statistics</h3>\n<p>This page counts visits with <a href="https://www.goatcounter.com" target="_blank" rel="noopener">GoatCounter</a>, which sets no cookies and stores no personal data. It records page views, the referring site, browser, screen size and country, only as totals. See the <a href="https://www.goatcounter.com/privacy" target="_blank" rel="noopener">GoatCounter privacy policy</a>.</p>\n'+_a,1)
    _a='</script></body></html>'
    assert t.count(_a)==1
    t=t.replace(_a,'</script>\n<script data-goatcounter="https://'+_gc+'.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script></body></html>',1)
