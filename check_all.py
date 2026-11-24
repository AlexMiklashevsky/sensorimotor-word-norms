# Consistency checks after an update. Prints a report and writes out/check_report.txt.
# Usage: python3 check_all.py                 (run the checks)
#        python3 check_all.py --accept-communities   (after rereading the community texts: store current communities as checked)
import json,os,re,sys,collections
ROOT=os.environ.get('SMN_ROOT') or os.path.dirname(os.path.abspath(__file__))
J=lambda p:json.load(open(os.path.join(ROOT,p)))
sys.path.insert(0,ROOT+'/net')
R=[r for r in J('work/records.json') if not r.get('_excluded')]
N=J('net/nodes.json'); NB={n['id']:n for n in N}
S=J('work/scales/all2.json'); C={(c['key'],c['scale']):c for c in J('facets/coded2.json')}
REF=J('refs/references.json'); D=J('refs/dois.json'); M=J('refs/crossref_refs_meta.json')
from titles import T
from dims import dim
E,W=[],[]   # errors (must fix), warnings (check)
labs=sorted({r['Authors'] for r in R})
if '--accept-communities' in sys.argv:
    sig={}
    for n in N:
        if n.get('community'): sig.setdefault(str(n['community']),[]).append(n['id'])
    p=ROOT+'/net/community_signature.json'; old=json.load(open(p))
    old['communities']={k:sorted(v) for k,v in sorted(sig.items())}; json.dump(old,open(p,'w'),ensure_ascii=False,indent=1)
    print('Stored current communities as checked.'); sys.exit()
# 1 every table paper is in the network (except "in preparation")
for a in labs:
    if a not in NB and 'in prep' not in a: E.append(f'Not in the network: {a}')
for a in NB:
    if a not in labs: E.append(f'Network node without table row: {a}')
# 2 labels: year in label = Year field; same label used for one paper only
for r in R:
    m=re.search(r'\((\d{4})[a-z]?\)$',r['Authors'])
    if not m: W.append(f'Label without year: {r["Authors"]}')
    elif str(r['Year'])!=m.group(1): E.append(f'Label year differs from Year field: {r["Authors"]} vs {r["Year"]}')
by=collections.defaultdict(set)
for r in R: by[r['Authors']].add((r.get('Paper link') or '').strip())
for a,l in by.items():
    if len(l)>1: W.append(f'Label used with different paper links (one label = one paper?): {a}')
# 3 references
for a in NB:
    h=REF['html'].get(a)
    if not h or h=='MISSING': E.append(f'No reference entry: {a} (add DOI to Paper link and run refs/fetch_crossref.py, or add a manual entry in refs/build_refs.py)')
for a,d in D.items():
    if a in NB and (d not in M or 'err' in M.get(d,{})) and REF['html'].get(a,'MISSING')=='MISSING': E.append(f'No Crossref metadata for {a} ({d}): run refs/fetch_crossref.py')
# 4 citation matching needs a title fragment per paper
for a in NB:
    if a not in T: W.append(f'No title fragment in net/titles.py (needed to find citations of this paper): {a}')
# 5 coding: every record has scales, every scale has a category, derived fields filled
skeys=collections.Counter(s['key'] for s in S)
for r in R:
    k=r['_key']
    if not skeys[k]: E.append(f'No scales in work/scales/all2.json: {k}')
    v3=r.get('_v3',{})
    for f in ['Study type','Rater type','Rater group','POS group']:
        if not v3.get(f): E.append(f'Missing {f}: {k}')
    if isinstance(r.get('Number of items'),int) and not v3.get('Items (category)'): E.append(f'Missing Items (category): {k}')
for s in S:
    c=C.get((s['key'],s['scale']))
    if s['key'] in {r['_key'] for r in R}:
        if not c: E.append(f'Scale not coded in facets/coded2.json: {s["key"]} / {s["scale"]}')
        elif not any(c.get(f'cat{i}') in ('core','border') for i in range(1,7)) and not c.get('R'): W.append(f'Scale without category: {s["key"]} / {s["scale"]}')
        if c:
            for i in range(1,7):
                if c.get(f'cat{i}')=='core' and dim(i,s['scale'])=='other': W.append(f'Dimension not recognized (add a rule in net/dims.py): category {i}, {s["key"]} / {s["scale"]}')
# 6 hand-written community texts
sig=J('net/community_signature.json')['communities']; cur=collections.defaultdict(set)
for n in N:
    if n.get('community'): cur[str(n['community'])].add(n['id'])
if set(sig)!=set(cur): W.append(f'Number of citation communities changed ({len(sig)} -> {len(cur)}): reread the community texts in net/build_page_v2.py, then run check_all.py --accept-communities')
else:
    for k in sig:
        a,b=set(sig[k]),cur[k]; jac=len(a&b)/len(a|b)
        if jac<1: W.append(f'Community {k} changed (overlap {jac:.0%}; new: {sorted(b-a)}; left: {sorted(a-b)}): reread its text in net/build_page_v2.py, then run check_all.py --accept-communities')
rep=['CHECK REPORT',f'{len(labs)} papers, {len(R)} table rows, {len(N)} network nodes','',f'ERRORS ({len(E)}) - fix before publishing:']+[' - '+x for x in E]+['',f'WARNINGS ({len(W)}) - check:']+[' - '+x for x in W]
os.makedirs(ROOT+'/out',exist_ok=True); open(ROOT+'/out/check_report.txt','w').write('\n'.join(rep)+'\n'); print('\n'.join(rep))
