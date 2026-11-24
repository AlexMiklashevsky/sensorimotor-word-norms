import os as _os
ROOT=_os.environ.get('SMN_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import json,collections,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
ren={'Van Havermaet and Wurm (2014)':'Van Havermaet (2013)'}
gone={'Ghandhari et al. (2020)','Ghio et al. (2013)','McLean et al. (2026)','Shebani and Pulvermüller (2018)','Trumpp et al. (2013)','Wang et al. (2023)'}
NOREF={'Suzuki et al. (2006)'}
REJ={('Wu et al. (2013)','Yang et al. (2011)'),('Vanhoutte et al. (2015)','Moseley et al. (2014)'),('Trott and Bergen (2026)','Conde et al. (2025)'),('Speed et al. (2025)','Kiefer et al. (2008)'),('Gijssels and Casasanto (2020)','Lynott and Connell (2013)')}
rej=json.load(open('rejected.json')); REJ|={(e['citing'],e['cited']) for e in rej}
acc={}
for e in json.load(open('old_v1/edges.json')):
    e=dict(e,citing=ren.get(e['citing'],e['citing']),cited=ren.get(e['cited'],e['cited']))
    if {e['citing'],e['cited']}&gone: continue
    acc[(e['citing'],e['cited'])]=e
V=json.load(open('new_verif.json'))
for e in V['ok']+V['bad']:
    k=(e['citing'],e['cited'])
    if k in REJ or k in acc or e['citing'] in NOREF: continue
    strong=e['score']>=90 and e['year_exact'] and e.get('vctx')
    e['method']='reference list (v2 run: author + year + title, then title + author)'
    e['decision']='auto' if strong else 'checked: reference entry verified by hand (two-column layout, year differs or partial title)'
    if e.get('vctx'): e['context']=e['vctx']
    acc[k]=e
for P,tgt,f,ctx in json.load(open('retarget.json')):
    if tgt=='Moseley et al. (2014)' and (P,tgt) not in acc:
        acc[(P,tgt)]=dict(citing=P,cited=tgt,score=100,year_exact=False,context=ctx,method='reference list (targeted re-match after correcting the paper behind the row)',decision='checked: reference entry verified by hand (cited as 2014 print version)')
for e in json.load(open('new3.json')):
    k=(e['citing'],e['cited'])
    if k in REJ or k in acc: continue
    acc[k]=dict(citing=e['citing'],cited=e['cited'],score=None,year_exact=True,context=e['ctx'],method='reference list (PDF obtained later; title + author check)',decision='manual: reference verified by hand' if e.get('manual') else 'checked: reference entry verified by hand')
# add rejected new ones to rejected list
newrej=[dict(citing=a,cited=b,reason=r) for (a,b),r in {('Speed et al. (2025)','Kiefer et al. (2008)'):'reference is Trumpp et al. (2013) "Losing the sound of concepts", not Kiefer et al. (2008)',('Wu et al. (2013)','Yang et al. (2011)'):'reference is Yang and Shu (2011, Neuroscience Letters), not Yang et al. (2011, Brain and Language)',('Vanhoutte et al. (2015)','Moseley et al. (2014)'):'reference is Moseley et al. (2013, Scientific Reports), not the paper behind the Moseley et al. (2014) row'}.items()]
json.dump(rej+[r for r in newrej if (r['citing'],r['cited']) not in {(x['citing'],x['cited']) for x in rej}],open('rejected.json','w'),ensure_ascii=False,indent=0)
L=[{k:e.get(k) for k in ('citing','cited','score','year_exact','context','method','decision')} for e in acc.values()]
json.dump(L,open('edges.json','w'),ensure_ascii=False,indent=0)
print(len(L),'edges',collections.Counter(e['decision'].split(':')[0] for e in L))
# nodes
R=[r for r in json.load(open('../work/records.json')) if not r.get('_excluded')]
C=json.load(open('../facets/coded2.json'))
CATN={1:'1 Global sensory experience',2:'2 Experience per sense',3:'3 Perceptual features',4:'4 Bodily involvement (no body part named)',5:'5 Specific body part / effector',6:'6 Body-object interaction'}
P={}
for r in R:
    a=r['Authors']; n=P.setdefault(a,dict(id=a,year=int(r['Year']) if str(r['Year']).isdigit() else 2026,langs=[],keys=[],link=r['Paper link'],rater=r['_v3'].get('Rater type','human'),study=r['_v3'].get('Study type','')))
    n['langs'].append(r['_v3'].get('Language') or r['Language']); n['keys'].append(r['_key'])
from fulltext import available; FT=available()
nodes=[]
for a,n in P.items():
    if 'in preparation' in a: continue
    core=collections.Counter(); status={}
    for c in C:
        if c['key'] in n['keys'] and not (c.get('status') or '').startswith(('excluded','outside')):
            for k in range(1,7):
                v=c.get(f'cat{k}')
                if v=='core': core[k]+=1; status[k]='core'
                elif v=='border' and status.get(k)!='core': status[k]='border'
    if core: prim=sorted(core.items(),key=lambda kv:(-kv[1],kv[0]))[0][0]
    elif status: prim=min(status)
    else: prim=None
    langs=list(dict.fromkeys(l.split(' (')[0] for l in n['langs']))
    has=a in FT and a not in NOREF
    nodes.append(dict(id=a,year=n['year'],language=' / '.join(langs),lang1=langs[0] if len(langs)==1 else 'Multilingual',cluster=CATN[prim] if prim else 'Outside the categories',
        cats=', '.join(f"{k}{'' if status[k]=='core' else ' (border)'}" for k in sorted(status)),rater=n['rater'],study=n['study'],pie=[[k,status[k]] for k in sorted(status)],has_reference_list=has,link=n['link']))
json.dump(nodes,open('nodes.json','w'),ensure_ascii=False,indent=0)
print(len(nodes),'nodes',collections.Counter(n['cluster'] for n in nodes),sum(not n['has_reference_list'] for n in nodes),'hollow')
ids={n['id'] for n in nodes}
L=[e for e in json.load(open('edges.json')) if e['citing'] in ids and e['cited'] in ids]
json.dump(L,open('edges.json','w'),ensure_ascii=False,indent=0); print(len(L),'edges after node filter')
