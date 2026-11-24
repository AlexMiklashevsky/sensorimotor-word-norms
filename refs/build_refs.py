import os as _os
ROOT=_os.environ.get('SMN_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# builds APA 7 reference list for the network papers -> refs/references.json {id: html}
import json,re,html,unicodedata
M=json.load(open(ROOT+'/refs/crossref_refs_meta.json'));D=json.load(open(ROOT+'/refs/dois.json'))
N=json.load(open(ROOT+'/net/nodes.json'))
EXTRA={ # DOIs found in full texts / Crossref later
 'Moseley et al. (2012)':('10.1093/cercor/bhr238',{'a':[['Moseley','Rachel'],['Carota','Francesca'],['Hauk','Olaf'],['Mohr','Bettina'],['Pulvermüller','Friedemann']],'t':'A role for the motor system in binding abstract emotional meaning','c':'Cerebral Cortex','v':'22','i':'7','p':'1634-1647','an':'','ty':'journal-article'}),
 'Kiefer et al. (2008)':('10.1523/JNEUROSCI.3579-08.2008',{'a':[['Kiefer','Markus'],['Sim','Eun-Jin'],['Herrnberger','Bärbel'],['Grothe','Jo'],['Hoenig','Klaus']],'t':'The sound of concepts: Four markers for a link between auditory and conceptual brain systems','c':'Journal of Neuroscience','v':'28','i':'47','p':'12224-12230','an':'','ty':'journal-article'}),
 'Niccolai et al. (2014)':('10.1371/journal.pone.0108059',{'a':[['Niccolai','Valentina'],['Klepp','Anne'],['Weissler','Hannah'],['Hoogenboom','Nienke'],['Schnitzler','Alfons'],['Biermann-Ruben','Katja']],'t':'Grasping hand verbs: Oscillatory beta and alpha correlates of action-word processing','c':'PLoS ONE','v':'9','i':'9','p':'','an':'e108059','ty':'journal-article'}),
 'Suggate and Stoeger (2014)':('10.1177/0142723714535768',{'a':[['Suggate','Sebastian P.'],['Stoeger','Heidrun']],'t':'Do nimble hands make for nimble lexicons? Fine motor skills predict knowledge of embodied vocabulary items','c':'First Language','v':'34','i':'3','p':'244-261','an':'','ty':'journal-article'}),
 'Yaguchi (2011)':('10.5265/jcogpsy.8.119',{'a':[['Yaguchi','Yukiyasu']],'t':'The comprehension of synesthetic expressions with onomatopeic words','c':'Japanese Journal of Cognitive Psychology','v':'8','i':'2','p':'119-129','an':'','ty':'journal-article'}),
 'Rezanova and Korshunova (2025)':('10.17223/15617793/517/5',{'a':[['Rezanova','Zoya I.'],['Korshunova','Irina S.']],'t':'Actual language experience of a bilingual as a factor influencing the perception of perceptual semantics [In Russian]','c':'Vestnik Tomskogo gosudarstvennogo universiteta','v':'','i':'517','p':'53-61','an':'','ty':'journal-article','keep':1}),
}
# fully manual entries (APA, html with <i>)
MAN={
 'Britton (2024)':'Britton, J. R. (2024). <i>Embodiment and modality exclusivity of Chinese verbs</i> [Doctoral dissertation, The Hong Kong Polytechnic University]. https://theses.lib.polyu.edu.hk/handle/200/12979',
 'Shao et al. (2026)':'Shao, Y., Hsu, Y.-Y., & Huang, C.-R. (2026). The sensorimotor norms for the Chinese classifiers. In <i>Proceedings of the Fifteenth Language Resources and Evaluation Conference</i> (pp. 11439-11450). ELRA Language Resource Association. https://doi.org/10.63317/2ub8kenhmi8d',
 'Shao et al. (2025a)':'Shao, Y., Hsu, Y.-Y., & Huang, C.-R. (2025). The sensorimotor norms for the Chinese classifiers. In P. Jin, Q. Su, & J.-F. Hong (Eds.), <i>Chinese lexical semantics</i> (Lecture Notes in Computer Science, Vol. 15552, pp. 241-254). Springer. https://doi.org/10.1007/978-981-96-3509-2_18',
 'Shao et al. (2025b)':'Shao, Y., Hsu, Y.-Y., & Huang, C.-R. (2025). Sensory and affective dimensions in Mandarin monosyllabic adjectives. In <i>Proceedings of the 39th Pacific Asia Conference on Language, Information and Computation</i> (pp. 341-351). Association for Computational Linguistics. https://aclanthology.org/2025.paclic-1.30/',
 'Chen et al. (2026)':'Chen, J., Parti, G., Zhong, Y., Huang, C.-R., & Marelli, M. (2026). <i>Chinese sensorimotor and embodiment norms for 3,000 lexicalized concepts</i> (arXiv:2605.22616). arXiv. https://arxiv.org/abs/2605.22616',
 'Conde et al. (2025)':'Conde, J., González Saiz, M., Grandury, M., Reviriego, P., Martínez, G., & Brysbaert, M. (2025). Psycholinguistic word features: A new approach for the evaluation of LLMs alignment with humans. In <i>Proceedings of the Fourth Workshop on Generation, Evaluation and Metrics (GEM²)</i> (pp. 8-17). Association for Computational Linguistics. https://aclanthology.org/2025.gem-1.2/',
 'Popović Stijačić et al. (2023)':'Popović Stijačić, M., Filipović Đurđević, D., Sekulić Sović, M., & Erdeljac, V. (2023). <i>Sensory-motor norms for 372 Croatian words</i> [Conference abstract]. 10th Novi Sad Workshop on Psycholinguistic, Neurolinguistic and Clinical Linguistic Research, Novi Sad, Serbia. https://reff.f.bg.ac.rs/bitstream/handle/123456789/5129/bitstream_21031.pdf',
 'Medler et al. (2005)':'Medler, D. A., Arnoldussen, A., Binder, J. R., & Seidenberg, M. S. (2005). <i>The Wisconsin perceptual attribute ratings database</i> [Database]. https://www.neuro.mcw.edu/ratings/index.html',
 'Van Havermaet (2013)':'Van Havermaet, L. R. (2013). <i>Semantic effects in word recognition and picture naming are moderated by body-object interaction</i> [Doctoral dissertation, Wayne State University]. https://digitalcommons.wayne.edu/oa_dissertations/711',
 'Paisios (2024)':'Paisios, D. (2024). <i>De la manipulabilité à la méthodologie et vice-versa: Un regard critique sur les pratiques expérimentales dans l\'étude des représentations d\'objets</i> [From manipulability to methodology and vice versa: A critical look at experimental practices in the study of object representations] [Doctoral dissertation, Université de Toulouse]. https://dante.univ-tlse2.fr/s/fr/item/39351',
 'Mochizuki et al. (2014)':'Mochizuki, M., Tamaki, K., & Naito, K. (2014). Body-object interaction rating for high imageable and familiar Japanese words [In Japanese]. <i>Studies in Humanities and Social Sciences, 88</i>, 145-160.',
 'Iida and Akita (2023)':'Iida, H., & Akita, K. (2023). Perceptual strength norms for 510 Japanese words, including ideophones: A comparative study with English. <i>Proceedings of the Annual Meeting of the Cognitive Science Society, 45</i>. https://escholarship.org/uc/item/1cg0835m',
 'Falcinelli et al. (2026)':'Falcinelli, I., Fini, C., Mazzuca, C., & Borghi, A. M. (2026). Age cohort variability in conceptual complexity and concreteness: The case of ecological and technological concepts. <i>Proceedings of the Annual Meeting of the Cognitive Science Society, 48</i>. https://escholarship.org/uc/item/5px9p1w0',
 'Filipović Đurđević et al. (2016)':'Filipović Đurđević, D., Popović Stijačić, M., & Karapandžić, J. (2016). A quest for sources of perceptual richness: Several candidates. In S. Halupka-Rešetar & S. Martínez-Ferreiro (Eds.), <i>Studies in language and mind</i> (pp. 187-238). Filozofski fakultet u Novom Sadu. http://digitalna.ff.uns.ac.rs/sadrzaj/2016/978-86-6065-359-0',
 'Popović Stijačić and Filipović Đurđević (2025)':'Popović Stijačić, M., & Filipović Đurđević, D. (2025). <i>Perceptual strength, concreteness, imagibility, context availability, age of acquisition, familiarity, emotional valence, and arousal ratings for 2100 Serbian nouns and their effect on visual lexical decision latencies</i> [Preprint]. PsychArchives. https://doi.org/10.23668/psycharchives.21378',
 'Díez-Álamo et al. (2025)':'Díez-Álamo, A. M., Díez, E., Wojcik, D. Z., Alonso, M. A., & Fernandez, A. (2025). <i>Perceptual strength and modality exclusivity norms for 5,500 Spanish words</i> [Unpublished dataset description; manuscript in preparation].',
 'Kumcu and Yağlı (2021)':'Kumcu, A., & Yağlı, E. (2021). <i>Sensory norms of 925 words</i> [Conference abstract]. 20th International Conference on Turkish Linguistics, Eskişehir, Turkey. https://avesis.hacettepe.edu.tr/yayin/593f5f27-0a54-4953-8577-08403c7f41dd/sensory-norms-of-925-words',
 'Kolbeneva and Alexandrov (2010)':'Kolbeneva, M. G., & Alexandrov, Yu. I. (2010). <i>Organy chuvstv, emotsii i prilagatel\'nye russkogo yazyka: Lingvo-psikhologicheskii slovar\'</i> [Senses, emotions, and adjectives of the Russian language: A linguo-psychological dictionary]. Yazyki slavyanskikh kul\'tur. https://www.lib.ipran.ru/upload/papers/20245854.pdf',
 'Marson (2023)':'Marson, F. (2023). <i>Interoception and its role in shaping words meaning: Behavioral and electrophysiological explorative evidence on the concreteness of abstract concepts</i> [Doctoral dissertation, Sapienza University of Rome]. https://iris.uniroma1.it/handle/11573/1710254',
 'Bernabeu (2020)':'Bernabeu, P. (2020). <i>Dutch modality exclusivity norms for 336 properties and 411 concepts</i> [Preprint]. PsyArXiv. https://doi.org/10.31234/osf.io/s2c5h',
}
KEEP={'English','Chinese','Mandarin','Cantonese','French','Spanish','Italian','German','Dutch','Russian','Japanese','Korean','Serbian','Croatian','Turkish','Turkic','Portuguese','Polish','Greek','Arabic','Hebrew','Estonian','Finnish','Norwegian','Swedish','Danish','Hungarian','Czech','Slovak','Basque','Catalan','Galician','Uzbek','Kazakh','Tatar','Hindi','Persian','Malay','Indonesian','Thai','Vietnamese','Brazilian','European','Lancaster','Glasgow','Warriner','Wisconsin','Brysbaert','Bayesian','Taiwan','Mainland','Ponzo','Stroop','McGurk','Spanish-English','English-Spanish','Chinese-English','English-Chinese','Western','Asian','Snodgrass','Vanderwart','Madrid','Spanish','Warriner','Tomsk','Europe','China','Japan','Italy','Germany','Spain','France','Russia','Serbia','Croatia','Turkey','Netherlands','Belgium','Flemish','Canadian','American','British','Australian','Interoception','I','Internet','Fourier','Gaussian','Likert'}
def _part(p,first_cap):
    core=re.sub(r'^[^\w]+|[^\w]+$','',p)
    if not core: return p
    if core in KEEP: return p
    if len(re.findall(r'[A-Z]',core))>=2 or (core[0].islower() and re.search(r'[A-Z]',core)): return p  # acronyms, fMRI
    i=p.index(core[0])
    if first_cap: return p[:i]+p[i].upper()+p[i+1:]
    if core[0].isupper() and not re.search(r'[A-Z]',core[1:]): return p[:i]+p[i].lower()+p[i+1:]
    return p
def sent(t):
    t=html.unescape(re.sub(r'<[^>]+>','',t)).strip()
    for a,b in [('\u2013','-'),('\u2014','-'),('\u2010','-'),('\u2011','-'),('\u2019',"'"),('\u2018',"'"),('\u201c','"'),('\u201d','"'),('psycholinguis-tic','psycholinguistic'),('Psycholinguis-tic','Psycholinguistic')]: t=t.replace(a,b)
    t=re.sub(r'\?\s+-\s+','? ',t)
    out=[];cap=True
    for w in re.split(r'(\s+)',t):
        if not w.strip(): out.append(w);continue
        parts=w.split('-')
        w2='-'.join(_part(x,cap and k==0) for k,x in enumerate(parts))
        out.append(w2)
        cap=bool(re.search(r'[:?!]$|\.$',w.rstrip('"\')]'))) and not re.search(r'\b(e\.g|i\.e|vs|al)\.$',w)
    return ''.join(out)
def ini(g):
    g=g.strip()
    if not g: return ''
    parts=re.split(r'\s+',g); res=[]
    for p in parts:
        if re.fullmatch(r'[A-Z]\.?',p): res.append(p[0]+'.');continue
        if re.fullmatch(r'([A-Z]\.)+',p): res.append(' '.join(x+'.' for x in p.split('.') if x));continue
        if '-' in p: res.append('-'.join(x[0].upper()+'.' for x in p.split('-') if x));continue
        if p.lower() in ('van','von','de','der','den','da','di','du','la','le'): continue
        res.append(p[0].upper()+'.')
    return ' '.join(res)
def fam(f):
    if f.isupper() and len(f)>2: f=f.title()
    return f
FIX={'Pulvermuller':'Pulvermüller','Brybaert':'Brysbaert'}
def authors(a):
    a=[x for x in a if x[1] or not re.search(r'Univers|Faculty|Institut|Hospital|School|Department|Tomsk',x[0])]
    L=[f"{FIX.get(fam(f),fam(f))}, {ini(g)}".rstrip(', ') for f,g in a]
    if len(L)==1: return L[0]
    if len(L)<=20: return ', '.join(L[:-1])+', & '+L[-1]
    return ', '.join(L[:19])+', ... '+L[-1]
def jour(c):
    c=html.unescape(c).replace('&amp;','&')
    return {'PLoS ONE':'PLOS ONE','The Journal of Neuroscience':'Journal of Neuroscience','The Quarterly Journal of Experimental Psychology':'Quarterly Journal of Experimental Psychology','PLOS One':'PLOS ONE','PSYCHIATRIA DANUBINA':'Psychiatria Danubina','The Japanese journal of psychology':'Japanese Journal of Psychology','Sage Open':'SAGE Open'}.get(c,c)
def fmt(lab,d,m):
    yr=N_[lab]['year']
    A=authors(m['a'])
    t=m['t'] if m.get('keep') else sent(m['t']+((': '+m['st']) if m.get('st') else ''))
    if not t.endswith(('?','.','!',']')): t+='.'
    elif t.endswith(']'): t+='.'
    v=m.get('v','');i=m.get('i','');p=(m.get('p') or m.get('an') or '').replace('–','-')
    if not p and d.startswith('10.3389/'): p=str(int(d.rsplit('.',1)[1]))
    if p and not re.search(r'\d',p.replace(d.split('/')[-1],'')) and '.' in p: p=''
    if m.get('ty') in ('journal-article',None):
        src=f"<i>{jour(m['c'])}"+(f", {v}</i>" if v else '</i>')+(f"({i})" if i and v else (f", {i}" if i else ''))+(f", {p}" if p else '')+'.'
        if not v and not i: src+=' Advance online publication.'
    else:
        src=f"<i>{jour(m.get('c',''))}</i>."
    return f"{A} ({yr}). {t} {src} https://doi.org/{d}"
N_={n['id']:n for n in N}
R={}
for n in N:
    lab=n['id']
    if lab in MAN: R[lab]=MAN[lab];continue
    if lab=='Pulvermüller et al. (1999)': M[D[lab]]['a']=[['Pulvermüller','Friedemann'],['Lutzenberger','Werner'],['Preissl','Hubert']]
    if lab in EXTRA: d,m=EXTRA[lab]
    else:
        d=D.get(lab); m=M.get(d) if d else None
    if not m or 'err' in m: R[lab]='MISSING';continue
    R[lab]=fmt(lab,d,m)
for lab in R:
    _m=re.search(r'\((\d{4})([ab])\)$',lab)
    if _m: R[lab]=R[lab].replace('('+_m.group(1)+').','('+_m.group(1)+_m.group(2)+').',1)
def _k(l):
    s=re.sub(r'<[^>]+>','',R[l]); i=re.search(r' \((\d{4}[ab]?)\)',s)
    au=s[:i.start()] if i else s
    au=unicodedata.normalize('NFKD',au).encode('ascii','ignore').decode().lower().replace('.','').replace(',','')
    return (au,i.group(1) if i else '')
ORDER=sorted(R,key=_k)
def _html(r):
    parts=re.split(r'(</?i>)',r); out=[]
    for x in parts: out.append(x if x in('<i>','</i>') else html.escape(x,quote=False))
    r=''.join(out)
    return re.sub(r'(https?://\S+?)(\.?)$',lambda m:f'<a href="{m.group(1)}" target="_blank" rel="noopener">{m.group(1)}</a>{m.group(2)}',r)
json.dump({'order':ORDER,'html':{l:_html(R[l]) for l in R}},open(ROOT+'/refs/references.json','w'),ensure_ascii=False,indent=0)
# structured metadata for the BibTeX/RIS exports (export_public.py): Crossref/EXTRA entries from the same metadata as the APA text,
# manual entries from refs/manual_refs_meta.json
MANM=json.load(open(ROOT+'/refs/manual_refs_meta.json',encoding='utf-8'))
TY={'journal-article':'article',None:'article','book-chapter':'incollection','posted-content':'misc','proceedings-article':'inproceedings'}
BIB={}
for lab in ORDER:
    yr=re.search(r'\((\d{4})[ab]?\)$',lab).group(1)
    if lab in MAN:
        if lab not in MANM: BIB[lab]={'missing':True}; continue
        BIB[lab]=dict(MANM[lab]); continue
    d,m=(EXTRA[lab] if lab in EXTRA else (D.get(lab),M.get(D.get(lab))))
    if not m or 'err' in m: BIB[lab]={'missing':True}; continue
    au=[x for x in m['a'] if x[1] or not re.search(r'Univers|Faculty|Institut|Hospital|School|Department|Tomsk',x[0])]
    t=m['t'] if m.get('keep') else sent(m['t']+((': '+m['st']) if m.get('st') else ''))
    e={'type':TY.get(m.get('ty'),'misc'),'authors':[[FIX.get(fam(f),fam(f)),(g.title() if g.isupper() and len(g)>3 else g)] for f,g in au],'year':yr,'title':t.rstrip('.'),'doi':d}
    cont=jour(m.get('c','')) if m.get('c') else ''
    if e['type']=='article': e['journal']=cont
    elif cont: e['booktitle' if e['type'] in ('incollection','inproceedings') else 'publisher']=cont
    for k,f in (('v','volume'),('i','number'),('p','pages'),('pub','publisher')):
        if m.get(k) and f not in e: e[f]=str(m[k]).replace('\u2013','-')
    if m.get('ed'): e['editors']=m['ed']
    BIB[lab]=e
json.dump(BIB,open(ROOT+'/refs/bib_meta.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
def key(l): s=re.sub(r'<[^>]+>','',R[l]); return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
for l in ORDER: print(re.sub(r'<[^>]+>','',R[l]))
