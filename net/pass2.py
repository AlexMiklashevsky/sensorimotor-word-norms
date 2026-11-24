import os as _os
ROOT=_os.environ.get('SMN_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys,re,json,unicodedata
sys.path.insert(0,'.'); from titles import T
from rapidfuzz import fuzz
def fold(s):
    s=s.replace('ﬁ','fi').replace('ﬂ','fl').replace('–','-').replace('—','-').replace('’',"'").replace('​','')
    s=unicodedata.normalize('NFKD',s); s=''.join(c for c in s if not unicodedata.combining(c)); return re.sub(r'\s+',' ',s)
rows=json.load(open('rows.json')); papers={}
for x in rows:
    if not x['authors'].startswith('MSc'): papers.setdefault(x['authors'],x)
E=json.load(open('raw_edges.json')); have={(e['citing'],e['cited']) for e in E if e['score']>0}
new=[]
for P,x in papers.items():
    if not x['has']: continue
    t=fold(open(f'{ROOT}/txt/{P}.txt',encoding='utf-8',errors='ignore').read()); low=t.lower()
    for Tk,(sur,yr,frag) in T.items():
        if Tk==P or (P,Tk) in have: continue
        f=fold(frag).lower()
        if len(f)<20: continue
        for m in re.finditer(re.escape(f[:18]),low):
            seg=low[m.start():m.start()+len(f)+10]
            sc=fuzz.partial_ratio(f,seg)
            if sc<92: continue
            before=low[max(0,m.start()-260):m.start()]
            s=fold(sur).lower()
            if s in before:
                ys=re.findall(r'\b(?:19|20)\d\d(?=[a-z]?\b)',before[before.rfind(s):]+low[m.end():m.end()+200])
                new.append(dict(citing=P,cited=Tk,score=round(sc),year_exact=yr in ys,years=ys[:4],in_refsection=True,context=t[max(0,m.start()-200):m.start()+120],src='pass2'))
                break
json.dump(new,open('pass2.json','w'),ensure_ascii=False,indent=0)
for e in new: print(f"{e['citing'][:24]:24} -> {e['cited'][:26]:26} {e['years']} | {e['context'][60:250]}")
