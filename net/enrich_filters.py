# adds filter fields (aggregated over a paper's language rows) to nodes.json
import json,re
from dims import dim
S=json.load(open('../work/scales/all2.json')); CO={(c['key'],c['scale']):c for c in json.load(open('../facets/coded2.json'))}
R=[r for r in json.load(open('../work/records.json')) if not r.get('_excluded')]
N=json.load(open('nodes.json'))
def split(v): return [x.strip() for x in (v or '').split(';') if x.strip()]
by={}
for r in R: by.setdefault(r['Authors'],[]).append(r)
RX=re.compile(r'(-?\d+)\s*(?:\([^)]*\))?\s*(?:-|to)\s*\+?(-?\d+)')
def fmts(text):
    t=(text or '').lower(); out=[]
    for m in RX.finditer(t):
        a,b=int(m.group(1)),int(m.group(2))
        if b>a and b-a<=100: out.append(f'{a} to {b}' if a<0 else f'{a}-{b}'); break
    if re.search(r'yes/no|yes-no|\byes or no\b',t): out.append('yes/no')
    if re.search(r'select all|multiple choice|\bcheck\b',t): out.append('select all that apply')
    return out
SC={}
for sc in S: SC.setdefault(sc['key'],[]).append(sc)
BO=['30-99','100-299','300-999','1,000-2,999','3,000-9,999','10,000+']
for n in N:
    rows=by[n['id']]; v=lambda f:[r['_v3'].get(f,'') for r in rows]
    U=lambda L:list(dict.fromkeys(L))
    n['f_rt']=U(v('Rater type'))
    n['f_rg']=U([('LLM' if x=='n/a' else x) for s in v('Rater group') for x in (split(s) or ['Not reported'])])
    n['f_pp']=U([x for s in v('Perspective') for x in (split(s) or ['No wording available'])])
    n['f_pos']=U([s or 'Not reported' for s in v('POS group')])
    n['f_nb']=U([s or 'Not stated' for s in v('Items (category)')])
    keys=[r['_key'] for r in rows]
    n['f_dim']=U(sorted(f"{k}|{dim(k,sc['scale'])}" for kk in keys for sc in SC.get(kk,[]) for k in range(1,7) if CO.get((kk,sc['scale']),{}).get(f'cat{k}')=='core'))
    f=[]
    for r in rows:
        x=fmts(r.get('Rating scale'))
        if not x: x=[y for sc in SC.get(r['_key'],[]) for y in fmts(sc.get('anchors'))][:1]
        f+=x
    n['f_scale']=U(f)
    n['f_st']=U(v('Study type'))
    n['rpi']=U([s for s in v('Ratings per item') if s])
    n['vars']=U([r.get('Sensorimotor variables','') for r in rows if r.get('Sensorimotor variables')])
    n['pop']=U([r.get('Rater population','') for r in rows if r.get('Rater population')])
    n['n_items']=sorted(set(r['Number of items'] for r in rows if isinstance(r.get('Number of items'),int)))
json.dump(N,open('nodes.json','w'),ensure_ascii=False,indent=0)
import collections
for f in ['f_rt','f_rg','f_pp','f_pos','f_nb','f_scale','f_st']: print(f,collections.Counter(x for n in N for x in n[f]))
print(min(n['year'] for n in N),max(n['year'] for n in N))
