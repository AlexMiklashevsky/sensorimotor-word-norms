import os as _os
ROOT=_os.environ.get('SMN_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import json
D=open('graphdata.json').read(); R=json.load(open('results.json'))
nodes=json.load(open('nodes.json')); EE=json.load(open('edges.json')); C=R['communities']
def names(c,k=6): return ', '.join(f"{a} ({n})" for a,n in C[str(c)]['top'][:k])
top=', '.join(f"{a} {k} of {n}" for a,k,n in R['top_cited'][:5])
C5=(f"<li><b>Community 5 ({C['5']['size']}):</b> "+", ".join(a for a,_ in C['5']['top'])+"; too small to interpret.</li>") if '5' in C else ""
F=f"""<p><b>Citation groups follow category lines and the norming vs. experimental divide, not language.</b> Community detection on the citation links (Louvain, best of 100 runs) finds {R['n_communities']} communities (modularity {R['modularity_best']}; agreement between the 100 runs: ARI mean {R['stability_mean_ARI']}, lowest {R['stability_min_ARI']}). The communities agree moderately with each paper's main category (NMI {R['NMI_vs_cluster']}, ARI {R['ARI_vs_cluster']}), less with study type (norming study, stimulus ratings in an experimental study, etc.; NMI {R['NMI_vs_study']}, ARI {R['ARI_vs_study']}), and hardly at all with language (NMI {R['NMI_vs_language']}, ARI {R['ARI_vs_language']}). {round(R['edges_same_category']*100)}% of all links connect two papers with the same main category.</p>
<ul>
<li><b>Community 1 - experience per sense ({C['1']['size']} papers):</b> Lynott and Connell (2009, 2013), the Lancaster norms and their adaptations across languages, the Tomsk databases (Russian, Tatar, Khakas, Uzbek), and all LLM papers. Almost all are category 2. Pairs of members fall into the same community in {round(C['1']['mean_coassign']*100)}% of runs on average. Most cited: {names(1)}.</li>
<li><b>Community 2 - neuroscience stimulus ratings ({C['2']['size']}):</b> {dict(C['2']['study']).get('stimulus ratings in experimental study',0)} of {C['2']['size']} papers are ratings collected to select stimuli for brain or behavioral experiments (Pulvermüller, Kiefer, Hauk, González and colleagues; action-verb studies in L1 and L2). They mix categories 5, 2 and 4: effector ratings and modality ratings from this line cite each other rather than the norming literature. Most cited: {names(2)}. All its members stay together in {C['2']['together_all']} of 100 runs.</li>
<li><b>Community 3 - body-object interaction and global sensory experience ({C['3']['size']}):</b> the Siakaluk/Pexman BOI line and its adaptations together with the SER datasets (Juhasz, Bonin, Hinojosa, Díez-Álamo 2019, Song and Li, Wu and Mu, Yi, Van Hoey), plus the attribute ratings of Amsel et al. (2012) and Díez-Álamo et al. (2018). Categories 6 and 1 cite each other heavily (pairs together in {round(C['3']['mean_coassign']*100)}% of runs on average). Most cited: {names(3)}.</li>
<li><b>Community 4 - Italian abstract-concepts work ({C['4']['size']}):</b> Villani et al. (2019), Repetto et al. (2023), Falcinelli et al. (2024, 2026), Mazzuca et al. (2022) and recent papers that build on them, including Barca et al. (2026). It is the least stable group (pairs of members together in {round(C['4']['mean_coassign']*100)}% of runs on average); in most runs some of its papers join other communities.</li>
{C5}
</ul>
<p><b>Category 2 is split by tradition.</b> Modality ratings from norming studies sit in community 1, but modality ratings collected as stimulus checks (Kiefer, González, Pulvermüller 1999, Hoenig, Dreyer) sit in community 2, and the Italian abstract-concepts work forms community 4.</p>
<p><b>Most cited within the table</b> (cited by k of n table papers that could cite it, i.e., published the same year or later, or citing it as a preprint): {top}. These counts reflect the composition of the table and the age of each paper, not general impact.</p>"""
na=sum(1 for e in EE if e['decision']=='auto'); nc=sum(1 for e in EE if e['decision'].startswith('checked')); nm=sum(1 for e in EE if e['decision'].startswith('manual'))
M=f"""<ul>
<li><b>Links:</b> each reference list in the {sum(1 for n in nodes if n['has_reference_list'])} papers with full text was matched against the table by script: first author, year (±1 for online-first, preprint or in-press versions) and a distinctive title fragment (fuzzy matching), in two passes (anchored on the author, then on the title). Names in co-author position were excluded. Every new candidate was then checked by locating the title fragment with the first author's surname just before it in the citing text. {na} links matched automatically; {nc} with a year difference, partial title or two-column layout were checked against the reference entry, and {nm} were found only by hand (page breaks, a differently spelled author name). {len(json.load(open('rejected.json')))} candidate links were rejected (e.g., a different paper by the same author and year). Every link, with the reference entry it rests on, is in the workbook citation_network_v2.xlsx.</li>
<li><b>Ring-shaped nodes</b> have no reference list available (no PDF, a web page, a dataset description, or a full text without references); they can be cited but cannot cite, so their low number of outgoing links is missing data. One node per paper: papers with several language rows are one node ("Multilingual" for the language comparison). Where a row merges a rating paper with a later experimental paper that reused the ratings (Hauk and Pulvermüller, 2004, with Hauk, Johnsrude and Pulvermüller, 2004), only citations of the rating paper count; where a dataset was published twice (Van Havermaet, 2013, dissertation and the 2014 article), citations of either version count.</li>
<li>{R['newer_cited_edges']} links point to a paper with a later table year (cited as a preprint or in press).</li>
<li><b>Main category:</b> each paper gets the category (1-6, as in the overview table) with the most scales coded "core" on the "Instructions by scale" sheet; ties go to the lower category number. The full set of categories is shown in the Selected paper panel (click a node in the Interactive network tab) and in the Table tab. LLM and model-based papers keep their category; rater type is shown in the Selected paper panel.</li>
<li><b>Communities:</b> Louvain on the undirected graph, without the papers lacking a reference list and without isolated papers ({R['n_nodes_community']} papers, {R['n_edges_community']} links), resolution 1, best modularity of 100 seeds; communities with fewer than {R['min_community_size']} papers are shown as not assigned ({R['n_unassigned']} papers). Agreement with categories, study type and language: NMI and ARI on the papers in communities; chance level for the category agreement from 2,000 shuffles of the category labels (NMI mean {R['NMI_vs_cluster_null_mean']}, 99th percentile {R['NMI_vs_cluster_null_p99']}). Analysis in {R['software']}; script analysis/communities.R.</li>
</ul>"""
CL=['1 Global sensory experience','2 Experience per sense','3 Perceptual features','4 Bodily involvement (no body part named)','5 Specific body part / effector','6 Body-object interaction']+(['Outside the categories'] if any(n['cluster']=='Outside the categories' for n in nodes) else [])
t=open('page_template.html').read()
rep=[("const CL=['Modality-based strength (Lancaster line)','Body interaction & affordances','Effector & action relatedness','Global sensory experience (SER)','Feature relevance','Computational (LLM / embeddings)','Fine-grained attributes'];","const CL="+json.dumps(CL,ensure_ascii=False)+";"),
("Color and shape show the construct cluster (or, if switched, the citation community).","Color and shape show the paper's main category from the overview table (or, if switched, the citation community)."),
('data-v="cluster">Construct cluster</button>','data-v="cluster">Main category</button>'),
('aria-label="Citation network of 92 sensorimotor norm papers"',f'aria-label="Citation network of {R["n_nodes_graph"]} sensorimotor norm papers"'),
("Shape still shows the construct cluster.","Shape still shows the main category."),
("agreement (NMI) of communities with construct cluster vs. language","agreement (NMI) of communities with main category vs. language"),
("'papers (MSc theses excluded)'","'papers'"),
("['cluster','Construct cluster']","['cluster','Main category']"),
("<td>${n.cluster}</td>","<td>${n.cluster}${n.cats?'<br><span class=\"muted\">all: '+n.cats+'</span>':''}${n.rater&&n.rater!=='human'?'<br><span class=\"muted\">'+n.rater+'</span>':''}</td>"),
]
for a,b in rep:
    assert a in t,a[:60]; t=t.replace(a,b)

PIE=[
("Color and shape show the paper's main category from the overview table (or, if switched, the citation community).",
 "Each node is a pie with one equal slice per category that the paper's scales belong to; if switched, color shows the citation community. Ring-shaped nodes have no reference list available."),
(" const p=el('path',{d:shapePath(SHAPES[CL.indexOf(n.cluster)],rad(n)),'stroke-width':n.has_reference_list?1.5:2},g);"," const p=el('g',{},g);"),
("const c=colorOf(n);p.setAttribute('fill',n.has_reference_list?c:'var(--surface-1)');p.setAttribute('stroke',n.has_reference_list?'var(--surface-1)':c);","drawNode(n,p);"),
("function visible(n){return st.active.has(n.cluster)&&","function visible(n){return (st.color==='community'?st.activeC.has(n.community||'na'):(n.pie&&n.pie.length?n.pie.some(([k])=>st.active.has(CL[k-1])):st.active.has(n.cluster)))&&"),
("const cnt=N.filter(n=>n.cluster===c).length;","const cnt=N.filter(n=>(n.pie||[]).some(([k])=>k===i+1)||(!(n.pie||[]).length&&n.cluster===c)).length;"),
('<path d="${shapePath(SHAPES[i],5)}" fill="var(--c${i+1})"/>','<circle r="5" fill="var(--c${i+1})"/>'),
("t.textContent='Shape still shows the main category.';","t.textContent='Pies return in the \"Main category\" view.';"),
("Hollow nodes have no reference list available (no PDF, a web page or a dataset description), so they can only receive citations.","Pie slices: categories of its rating scales. Ring-shaped nodes have no reference list available (no PDF, a web page or a dataset description), so they can only receive citations."),
("No reference list available (hollow node)","No reference list available (ring-shaped node)"),
("function rad(n){","""function arc(r0,r1,a0,a1){const f=a1-a0>Math.PI?1:0,c=Math.cos,s=Math.sin;if(a1-a0>=2*Math.PI-1e-6){const o=`M${r1},0A${r1},${r1} 0 1,1 ${-r1},0A${r1},${r1} 0 1,1 ${r1},0z`;return r0?o+`M${r0},0A${r0},${r0} 0 1,0 ${-r0},0A${r0},${r0} 0 1,0 ${r0},0z`:o}
 let d=`M${r1*c(a0)},${r1*s(a0)}A${r1},${r1} 0 ${f},1 ${r1*c(a1)},${r1*s(a1)}`;d+=r0?`L${r0*c(a1)},${r0*s(a1)}A${r0},${r0} 0 ${f},0 ${r0*c(a0)},${r0*s(a0)}z`:'L0,0z';return d}
function drawNode(n,g){g.innerHTML='';g.parentNode.firstChild.setAttribute('r',rad(n)*1.1+6/ZZ());const r=rad(n)*1.1,r0=n.has_reference_list?0:r*0.5;
 let sl=st.color==='cluster'&&n.pie&&n.pie.length?n.pie.map(([k,s])=>[`var(--c${k})`,s==='border'?0.4:1]):[[colorOf(n),1]];
 if(st.color==='cluster'&&!(n.pie&&n.pie.length))sl=[['var(--c7)',1]];
 const step=2*Math.PI/sl.length;sl.forEach(([c,o],i)=>{const a0=-Math.PI/2+i*step;el('path',{d:arc(r0,r,a0,a0+step),fill:c,'fill-opacity':o,'fill-rule':'evenodd',stroke:'var(--surface-1)','stroke-width':sl.length>1?1:0.8},g)})}
function rad(n){return (4+1.55*Math.sqrt(n.cited_by))/Math.pow(ZZ(),0.8)}\nfunction rad0(n){"""),
]
for a,b in PIE:
    assert a in t,a[:70]; t=t.replace(a,b)

ZOOM=[
("const W=1000,H=720,M={l:40,r:40,t:30,b:70};","const W=1000,H=720,M={l:40,r:40,t:30,b:70};let VB={x:0,y:0,w:W,h:H};"),
('<div class="stage" id="stage">','<div class="stage" id="stage"><div class="zoombar"><button id="zin" aria-label="Zoom in">+</button><button id="zout" aria-label="Zoom out">&minus;</button><button id="zreset">Reset</button></div>'),
(".stage{border:1px solid var(--line);border-radius:10px;background:var(--surface-1);position:relative}",
 ".stage{border:1px solid var(--line);border-radius:10px;background:var(--surface-1);position:relative;overflow:hidden}.stage svg{touch-action:none;cursor:grab}.stage svg.dragging{cursor:grabbing}.zoombar{position:absolute;right:10px;top:10px;display:flex;gap:4px;z-index:2}.zoombar button{font:inherit;font-size:13px;min-width:30px;height:28px;border:1px solid var(--line);border-radius:6px;background:var(--surface-1);color:var(--text-primary);cursor:pointer}.zoombar button:hover{background:var(--surface-2)}.zhint{position:absolute;left:12px;top:10px;font-size:11.5px;color:var(--text-muted);pointer-events:none}"),
("st.labels==='top'&&n.cited_by>=8","st.labels==='top'&&(st.lang||n.cited_by>=Math.max(1,8/ZZ()))"),
("l.setAttribute('y',y-rad(n)-5);","l.setAttribute('y',y-rad(n)*1.1-4/ZZ());l.style.fontSize=(10.5/ZZ())+'px';l.style.strokeWidth=(3/ZZ())+'px';"),
("l.setAttribute('y',y+rad(N[i])+12)","l.setAttribute('y',y+rad(N[i])*1.1+11/ZZ())"),
("const edgeEls=E.map(([a,b])=>el('line',{stroke:'var(--edge)','stroke-width':0.8},gE));","const edgeEls=E.map(([a,b])=>el('line',{stroke:'var(--edge)','stroke-width':0.8,'vector-effect':'non-scaling-stroke'},gE));"),
("function render(){","""function ZZ(){return W/VB.w}
function setVB(){VB.w=Math.min(W,Math.max(W/8,VB.w));VB.h=VB.w*H/W;VB.x=Math.min(W-VB.w,Math.max(0,VB.x));VB.y=Math.min(H-VB.h,Math.max(0,VB.y));svg.setAttribute('viewBox',`${VB.x} ${VB.y} ${VB.w} ${VB.h}`)}
function svgPt(ev){const r=svg.getBoundingClientRect();return [VB.x+(ev.clientX-r.left)/r.width*VB.w,VB.y+(ev.clientY-r.top)/r.height*VB.h]}
function zoomAt(f,px,py){const nw=Math.min(W,Math.max(W/8,VB.w/f));const k=nw/VB.w;VB.x=px-(px-VB.x)*k;VB.y=py-(py-VB.y)*k;VB.w=nw;setVB();render()}
svg.addEventListener('wheel',ev=>{ev.preventDefault();const [px,py]=svgPt(ev);zoomAt(Math.exp(-ev.deltaY*0.0015),px,py)},{passive:false});
let drag=null,dragged=false;
svg.addEventListener('pointerdown',ev=>{if(ev.button!==0)return;drag={sx:ev.clientX,sy:ev.clientY,x:VB.x,y:VB.y};dragged=false});
window.addEventListener('pointermove',ev=>{if(!drag)return;const dx=ev.clientX-drag.sx,dy=ev.clientY-drag.sy;if(!dragged&&Math.hypot(dx,dy)<4)return;dragged=true;svg.classList.add('dragging');const r=svg.getBoundingClientRect();VB.x=drag.x-dx/r.width*VB.w;VB.y=drag.y-dy/r.height*VB.h;setVB()});
window.addEventListener('pointerup',()=>{if(drag&&dragged)render();drag=null;svg.classList.remove('dragging')});
svg.addEventListener('click',ev=>{if(dragged){ev.stopPropagation();dragged=false}},true);
svg.addEventListener('dblclick',ev=>{ev.preventDefault();const [px,py]=svgPt(ev);zoomAt(2,px,py)});
document.getElementById('zin').onclick=()=>zoomAt(1.5,VB.x+VB.w/2,VB.y+VB.h/2);
document.getElementById('zout').onclick=()=>zoomAt(1/1.5,VB.x+VB.w/2,VB.y+VB.h/2);
document.getElementById('zreset').onclick=()=>{VB={x:0,y:0,w:W,h:H};setVB();render()};
function render(){"""),
("Hover a node to highlight its links; click it to pin the details.","Hover a node to highlight its links; click it to pin the details. Zoom with the mouse wheel, a double-click or the +/&minus; buttons; drag to move around."),
]
for a,b in ZOOM:
    assert a in t,a[:70]; t=t.replace(a,b)

LANGF=[
('<input type="search" id="q" placeholder="Find a paper (e.g., Lynott)">','<input type="search" id="q" placeholder="Find a paper (e.g., Lynott)"> <span><span class="lbl">Language</span><select id="langSel" aria-label="Filter by language"></select></span>'),
('input[type=search]{','select{font:inherit;padding:5px 8px;border:1px solid var(--line);border-radius:8px;background:var(--surface-1);color:var(--text-primary)}input[type=search]{'),
("&&(!st.q||n.id.toLowerCase().includes(st.q))}","&&(!st.q||n.id.toLowerCase().includes(st.q))&&(!st.lang||n.language.split(' / ').includes(st.lang))}"),
("document.getElementById('q').oninput=e=>{st.q=e.target.value.trim().toLowerCase();render()};","""document.getElementById('q').oninput=e=>{st.q=e.target.value.trim().toLowerCase();render()};
(()=>{const cnt={};N.forEach(n=>n.language.split(' / ').forEach(l=>cnt[l]=(cnt[l]||0)+1));const sel=document.getElementById('langSel');
 sel.innerHTML='<option value="">All languages ('+N.length+')</option>'+Object.keys(cnt).sort().map(l=>`<option value="${l}">${l} (${cnt[l]})</option>`).join('');
 sel.onchange=e=>{st.lang=e.target.value;render();table()}})();"""),
("const rows=N.slice().sort(","const rows=N.filter(n=>!st.lang||n.language.split(' / ').includes(st.lang)).slice().sort("),
]
for a,b in LANGF:
    assert a in t,a[:70]; t=t.replace(a,b)

exec(open('filters_patch.py').read())
t=t.replace("${n.language} · ${n.cluster}","${n.language} · ${n.cluster}${n.cats?' (all: '+n.cats+')':''}${n.rater&&n.rater!=='human'?' · '+n.rater:''}")
import re
t=re.sub(r"t\.textContent=c\.split\(' \('\)\[0\]\.replace\([^;]*\)\}\)\}","t.textContent=({'1 Global sensory experience':'1 Global (SER)','2 Experience per sense':'2 Per sense','3 Perceptual features':'3 Features','4 Bodily involvement (no body part named)':'4 Bodily','5 Specific body part / effector':'5 Effector','6 Body-object interaction':'6 BOI','Outside the categories':'Outside'})[c]||c})}",t)
import re as _re
NEWC='--c1:#1f5fbf;--c2:#e8590c;--c3:#1baf7a;--c4:#d9a900;--c5:#b0207a;--c6:#8f5713;--c7:#8a8984'
t=_re.sub(r'--c1:#[0-9a-f]{6};--c2:#[0-9a-f]{6};--c3:#[0-9a-f]{6};--c4:#[0-9a-f]{6};--c5:#[0-9a-f]{6};--c6:#[0-9a-f]{6};--c7:#[0-9a-f]{6}',NEWC,t)
exec(open('cats_patch.py').read())
exec(open('tabs_patch.py').read())
exec(open('plan_patch.py').read())
html=t.replace('__DATA__',D).replace('__FINDINGS__',json.dumps(F,ensure_ascii=False)).replace('__METHOD__',json.dumps(M,ensure_ascii=False))
open('citation_network_v2.html','w').write(html); print(len(html), 'c.replace' in html)
