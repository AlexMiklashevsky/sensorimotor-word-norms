# v6: filter controls for the citation network page (executed by build_page_v2.py)
FILT=[
('</div>\n<div class="chips" id="chips"></div>','''</div>
<div class="controls" id="filters"><span class="lbl" style="font-weight:600">Filters</span>
 <span><span class="lbl">Years</span><span class="yr"><input type="range" id="y0" aria-label="From year"><input type="range" id="y1" aria-label="To year"></span> <span id="yrLab" class="yrlab"></span></span>
 <span><span class="lbl">Rater group</span><select id="f_rg"></select></span>
 <span><span class="lbl">Perspective</span><select id="f_pp"></select></span>
 <span><span class="lbl">Part of speech</span><select id="f_pos"></select></span>
 <span><span class="lbl">N of items</span><select id="f_nb"></select></span>
 <button id="fclear" class="fbtn">Clear filters</button> <span id="fcount" class="lbl"></span>
</div>
<div class="chips" id="chips"></div>'''),
('.lbl{','''.yr{position:relative;display:inline-block;width:170px;height:20px;vertical-align:middle}
.yr::before{content:"";position:absolute;left:7px;right:7px;top:9px;height:2px;background:var(--line);border-radius:1px}
.yr input{position:absolute;left:0;top:0;width:100%;height:20px;margin:0;padding:0;background:none;pointer-events:none;-webkit-appearance:none;appearance:none}
.yr input::-webkit-slider-runnable-track{height:20px;background:transparent}
.yr input::-moz-range-track{background:transparent}
.yr input::-webkit-slider-thumb{-webkit-appearance:none;pointer-events:auto;width:14px;height:14px;margin-top:3px;border-radius:50%;background:var(--text-primary);border:2px solid var(--surface-1);cursor:pointer}
.yr input::-moz-range-thumb{pointer-events:auto;width:12px;height:12px;border-radius:50%;background:var(--text-primary);border:2px solid var(--surface-1);cursor:pointer}
.yrlab{font-variant-numeric:tabular-nums;font-size:13px}
.fbtn{font:inherit;font-size:13px;padding:4px 10px;border:1px solid var(--line);border-radius:8px;background:var(--surface-1);color:var(--text-primary);cursor:pointer}
.lbl{'''),
("&&(!st.lang||n.language.split(' / ').includes(st.lang))}","&&(!st.lang||n.language.split(' / ').includes(st.lang))&&passF(n)}"),
("st.labels==='top'&&(st.lang||n.cited_by","st.labels==='top'&&(st.lang||(anyF()&&st.nvis<=50)||n.cited_by"),
("function render(){\n","function render(){\n st.nvis=N.filter(visible).length;const fc=document.getElementById('fcount');if(fc)fc.textContent=(anyF()||st.lang)?st.nvis+' of '+N.length+' papers shown':'';\n"),
("const rows=N.filter(n=>!st.lang||n.language.split(' / ').includes(st.lang))","const rows=N.filter(n=>(!st.lang||n.language.split(' / ').includes(st.lang))&&passF(n))"),
("// cards & findings","""// filters (v6): a paper passes if any of its language rows has the value
const FKEYS=['f_rg','f_pp','f_pos','f_nb'];
const NBO=['30-99','100-299','300-999','1,000-2,999','3,000-9,999','10,000+','Not stated'];
const YMIN=Math.min(...N.map(n=>n.year)),YMAX=Math.max(...N.map(n=>n.year));
st.f={};st.y0=YMIN;st.y1=YMAX;st.nvis=N.length;
function passF(n){return n.year>=st.y0&&n.year<=st.y1&&FKEYS.every(k=>!st.f[k]||(n[k]||[]).includes(st.f[k]))}
function anyF(){return st.y0>YMIN||st.y1<YMAX||FKEYS.some(k=>st.f[k])}
FKEYS.forEach(k=>{const cnt={};N.forEach(n=>(n[k]||[]).forEach(v=>cnt[v]=(cnt[v]||0)+1));
 const keys=k==='f_nb'?NBO.filter(v=>cnt[v]):Object.keys(cnt).sort((a,b)=>cnt[b]-cnt[a]||a.localeCompare(b));
 const sel=document.getElementById(k);sel.innerHTML='<option value="">All</option>'+keys.map(v=>`<option value="${v}">${v} (${cnt[v]})</option>`).join('');
 sel.onchange=e=>{st.f[k]=e.target.value;render();table()}});
const y0=document.getElementById('y0'),y1=document.getElementById('y1'),yl=document.getElementById('yrLab');
[y0,y1].forEach(s=>{s.min=YMIN;s.max=YMAX;s.step=1});y0.value=YMIN;y1.value=YMAX;
function yr(e){let a=+y0.value,b=+y1.value;if(a>b){if(e.target===y0){a=b;y0.value=a}else{b=a;y1.value=b}}st.y0=a;st.y1=b;y0.style.zIndex=a>=YMAX-1?3:1;yl.textContent=a+'-'+b;render();table()}
y0.oninput=yr;y1.oninput=yr;yl.textContent=YMIN+'-'+YMAX;
document.getElementById('fclear').onclick=()=>{FKEYS.forEach(k=>{st.f[k]='';document.getElementById(k).value=''});y0.value=YMIN;y1.value=YMAX;st.y0=YMIN;st.y1=YMAX;yl.textContent=YMIN+'-'+YMAX;st.lang='';document.getElementById('langSel').value='';render();table()};
// cards & findings"""),
]
for a,b in FILT:
    assert t.count(a)==1,(t.count(a),a[:70]); t=t.replace(a,b)
# v9: NMI card shows only the category value
_a=",[R.NMI_vs_cluster.toFixed(2)+' vs '+R.NMI_vs_language.toFixed(2),'agreement (NMI) of communities with main category vs. language']"
assert t.count(_a)==1; t=t.replace(_a,",[R.NMI_vs_cluster.toFixed(2),'overlap (NMI, 0-1) between citation communities and theoretical constructs (main categories)']")
