# v10: description of the six categories under the graph (appended to the findings)
import collections as _co
def _cat(k):
    anyc=[n for n in nodes if any(c==k for c,_ in n['pie'])]
    main=[n for n in nodes if n['cluster'].startswith(str(k)+' ')]
    top=', '.join(f"{n['id']} ({n['cited_by']})" for n in sorted(main,key=lambda n:(-n['cited_by'],n['id']))[:5])
    st=_co.Counter(n['study'] for n in main); cm=_co.Counter(n.get('community') for n in main if n.get('community'))
    return len(anyc),len(main),top,st,cm,main
_d={k:_cat(k) for k in range(1,7)}
def _h(k): a,m,_,_,_,_=_d[k]; return f"{a} papers; main category of {m}"
def _top(k): return _d[k][2]
def _cm(k,c): return _d[k][4].get(c,0)
def _st(k,s): return _d[k][3].get(s,0)
_ST1={'norming study':'norming study','stimulus ratings in experimental study':'set of stimulus ratings in an experimental study','model-generated':'set of model-generated (LLM) ratings','thesis':'thesis','database':'database'}
_ST={'norming study':'norming studies','stimulus ratings in experimental study':'stimulus ratings in experimental studies','model-generated':'model-generated (LLM) ratings','thesis':'theses','database':'databases'}
def _stats(k):
    a,m,_,st,cm,main=_d[k]
    if not m: return ''
    parts=', '.join(f"{n} {(_ST1 if n==1 else _ST).get(x,x)}" for x,n in st.most_common())
    com=', '.join(f"{c} ({n})" for c,n in sorted(cm.items(),key=lambda z:-z[1]))
    nocom=m-sum(cm.values())
    return f"Of the {m} main-category papers: {parts}."  # per-community counts removed (user, 2026-11-25)
def _cooc(k):
    anyc=[n for n in nodes if any(c==k for c,_ in n['pie'])]
    alone=sum(1 for n in anyc if {c for c,_ in n['pie']}=={k})
    other=_co.Counter(c for n in anyc for c,_ in n['pie'] if c!=k)
    top=other.most_common(1)[0] if other else None
    return alone,top,len(anyc)
def _cotext(k):
    alone,top,n=_cooc(k)
    t=(f"None of the {n} papers uses only this category" if alone==0 else f"{alone} of the {n} papers use only this category")
    if top and top[1]>1: t+=f"; it is most often combined with category {top[0]} ({top[1]} {'paper' if top[1]==1 else 'papers'})"
    return t+'.'
F+=f"""
<p><b>The six categories.</b> Each rating scale in the overview table was assigned to one or more categories according to what raters were asked to judge. Categories were defined top-down, based on theoretical analysis of constructs measured in available datasets. A paper's pie shows every category its scales belong to, and its main category is the one with the most scales (see "How the network was built"). Counts below: papers with at least one scale in the category, and papers for which it is the main category; "most cited" lists main-category papers with the number of later table papers citing them.</p>
<ul>
<li><b>1 Global sensory experience (SER; {_h(1)}):</b> one overall rating of how much sensory experience a word evokes, without separating the senses (Juhasz et al., 2011: "the degree of sensory experience each one evokes for you"). {_stats(1)} {_cotext(1)} Most cited: {_top(1)}.</li>
<li><b>2 Experience per sense ({_h(2)}):</b> a separate rating for each modality (vision, hearing, touch, taste, smell, often interoception), as in the Lancaster norms ("To what extent do you experience WORD", answered by seeing, by hearing, etc.). {_stats(2)} {_cotext(2)} Most cited: {_top(2)}.</li>
<li><b>3 Perceptual features ({_h(3)}):</b> specific features within a modality (or cross-modally), such as color, shape, visual motion, loudness, pain, temperature or weight (Amsel et al., 2012: "How vivid (intense) is the color of this object?"; the feature ratings of Binder et al., 2016). {_stats(3)} {_cotext(3)} Most cited: {_top(3)}.</li>
<li><b>4 Bodily involvement, no body part named ({_h(4)}):</b> how much a word's meaning involves the body or bodily movement in general, without specifying an effector (e.g., the relative embodiment ratings of Sidhu et al., 2014; Tomasino et al., 2007: whether the word refers to a movement). This category, unlike category 6, can include verbs, both concrete and abstract (e.g., walk, run, think). {_stats(4)} {_cotext(4)} Most cited: {_top(4)}.</li>
<li><b>5 Specific body part / effector ({_h(5)}):</b> which body part an action involves, typically hand/arm, leg/foot and face/mouth (Hauk and Pulvermüller, 2004: "Does this word remind you of an action you could perform with your arms, hands, or fingers?"). Also includes norms for manipulability / graspability, as they also imply a specific effector, the hand. {_stats(5)} {_cotext(5)} Most cited: {_top(5)}.</li>
<li><b>6 Body-object interaction (BOI; {_h(6)}):</b> the ease with which a human body can physically interact with what a word refers to (Tillotson et al., 2008: "the ease with which a human body can physically interact with what they represent"). Unlike category 4, this category is defined for objects; some BOI datasets nevertheless include verbs or adjectives (e.g., Pexman et al., 2019; Muraki et al., 2022; Dickinson and Yates, 2026). {_stats(6)} {_cotext(6)} Most cited: {_top(6)}.</li>
</ul>"""
# v11: perspective explanation
import collections as _co2
_pp=_co2.Counter(v for n in nodes for v in n.get('f_pp',[]))
F+=f"""
<p><b>Perspective: whose experience raters are asked to judge.</b> Coded from the exact instruction wording. A paper can have more than one value when its scales or language versions are worded differently, so the counts (papers) add up to more than {len(nodes)}.</p>
<ul>
<li><b>own ({_pp['own']}):</b> the rater's own experience or actions, e.g., "To what extent do you experience WORD" (Lancaster norms) or "the degree of sensory experience each one evokes for you" (Juhasz et al., 2011).</li>
<li><b>typical person ({_pp['typical person']}):</b> a generic body or person, e.g., "the ease with which a human body can physically interact with what they represent" (Tillotson et al., 2008).</li>
<li><b>child ({_pp['child']}):</b> a typical child, e.g., "how easily the average 6-year-old can physically interact (using the body: hands, mouth, etc.) with what each word represents" (Muraki et al., 2022).</li>
<li><b>possible vs. actual ({_pp['possible vs. actual']}):</b> two separate scales, one for whether the referent "CAN BE EXPERIENCED" through a sense and one for how often "YOU EXPERIENCED IT" (the Serbian norms of Filipović Đurđević, Popović Stijačić and colleagues).</li>
<li><b>not specified ({_pp['not specified']}):</b> the exact wording is available but names no experiencer; it asks about association or about properties of the thing itself, e.g., "How much do you associate this item with a particular colour?" (Hoffman and Lambon Ralph, 2013) or "To what degree do you think of this thing as ..." (Binder et al., 2016). "You" may appear, but as the person giving the judgment, not as the person having the experience.</li>
<li><b>No wording available ({_pp['No wording available']}):</b> the paper does not print the instruction or only paraphrases it, so the perspective is unknown rather than absent.</li>
</ul>"""
# v13: reorder blocks in the order of the controls, each with a heading identical to the control label
def _cut(s,a,b=None):
    i=s.index(a); j=s.index(b,i) if b else len(s); return s[i:j]
_comm=F[:F.index('<p>Category 2 is split')]
_split=_cut(F,'<p>Category 2 is split','<p><b>Most cited within')
_most=_cut(F,'<p><b>Most cited within','\n<p><b>The six categories.')
_cats=_cut(F,'<p><b>The six categories.','\n<p><b>Perspective: whose')
_pers=_cut(F,'<p><b>Perspective: whose')
_cats=_cats.replace('<p><b>The six categories.</b> ','<p>')
_most=_most.replace('<p><b>Most cited within the table</b> (','<p>Most cited within the table (')
_pers=_pers.replace('<p><b>Perspective: whose experience raters are asked to judge.</b> Coded from the exact instruction wording.','<p>Whose experience the instruction asks raters to judge, coded from the exact instruction wording. This is independent of Rater group: adults can rate for a typical child (Perspective = child, Rater group = general adults), and children can rate their own experience (Perspective = own, Rater group = children).')

_rgc=_co2.Counter(v for n in nodes for v in n.get('f_rg',[]))
def _who(v): return ', '.join(n['id'] for n in nodes if v in n.get('f_rg',[]))
_MAINRG=['general adults','L2 bilinguals','LLM','older adults','children']
_rest=sorted((g for g in _rgc if g not in _MAINRG and g!='Not reported'),key=lambda g:(-_rgc[g],g))
_small=('<li><b>Other groups:</b> '+'; '.join(f"{g} ({_rgc[g]}: {_who(g)})" for g in _rest)+'.</li>') if _rest else ''
_rg=f"""<p>Who actually gave the ratings: the sample of raters, not the person the instruction asks about (that is Perspective, below). A paper can have more than one group, e.g., when it compares two samples, so the counts (papers) add up to more than {len(nodes)}.</p>
<ul>
<li><b>general adults ({_rgc['general adults']}):</b> adult samples without a special selection criterion.</li>
<li><b>L2 bilinguals ({_rgc['L2 bilinguals']}):</b> speakers rating words in their second language, e.g., Chinese-English or Turkic-Russian bilinguals ({_who('L2 bilinguals')}).</li>
<li><b>LLM ({_rgc['LLM']}):</b> ratings generated by large language models instead of people ({_who('LLM')}).</li>
<li><b>older adults ({_rgc['older adults']}):</b> samples of older adults, sometimes compared with young adults ({_who('older adults')}).</li>
<li><b>children ({_rgc['children']}):</b> children rated the words themselves ({_who('children')}). Compare Perspective = child, where adults rate on behalf of a typical child.</li>
{_small}
</ul>"""
_H=lambda s:f'<h3 class="fh">{s}</h3>\n'
F=_H('Main category')+_cats.strip()+'\n'+_H('Citation community')+_comm.strip()+'\n'+_split.strip()+'\n'+_H('Rater group')+_rg+'\n'+_H('Perspective')+_pers.strip()
t=t.replace('h3{margin:0 0 4px;font-size:14px}','h3{margin:0 0 4px;font-size:14px}\nh3.fh{font-size:15px;margin:22px 0 6px;padding-top:12px;border-top:1px solid var(--line)}\n#findings h3.fh:first-child{border-top:none;padding-top:0;margin-top:4px}',1)
# v17: page title
for _a,_b in [('<title>Citation network of sensorimotor norm datasets</title>','<title>Sensorimotor word norms: an overview</title>'),('<h1>Who cites whom: sensorimotor norm datasets</h1>','<h1>Sensorimotor word norms: an overview</h1>')]:
    assert t.count(_a)==1; t=t.replace(_a,_b)
