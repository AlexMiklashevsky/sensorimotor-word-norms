import os as _os
ROOT=_os.environ.get('SMN_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys,re,json,unicodedata
sys.path.insert(0,'.'); from titles import T
from rapidfuzz import fuzz
def fold(s):
    s=s.replace('ﬁ','fi').replace('ﬂ','fl').replace('–','-').replace('—','-').replace('’',"'").replace('​',''); s=unicodedata.normalize('NFKD',s); s=''.join(c for c in s if not unicodedata.combining(c)); return re.sub(r'\s+',' ',s)
rows=json.load(open('rows.json')); papers={}
for x in rows:
    if not x['authors'].startswith('MSc'): papers.setdefault(x['authors'],x)
L=json.load(open('edges.json')); have={(e['citing'],e['cited']) for e in L}
out=[]
for P,x in papers.items():
    if not x['has']: continue
    t=fold(open(f'{ROOT}/txt/{P}.txt',encoding='utf-8',errors='ignore').read()); low=t.lower()
    for Tk,(sur,yr,frag) in T.items():
        if Tk==P or (P,Tk) in have: continue
        f=fold(frag).lower()
        if len(f)<20: continue
        al=fuzz.partial_ratio_alignment(f,low)
        s=fold(sur).lower()
        # also in-text: surname then year within 200 chars, not co-author
        it=None
        for m in re.finditer(re.escape(s),low):
            if re.search(r'(, |& |and |-)$',low[max(0,m.start()-6):m.start()]): continue
            if re.search(r'\b'+yr+r'[a-z]?\b',low[m.end():m.end()+200]): it=t[max(0,m.start()-40):m.end()+160]; break
        if al.score>=78 or it:
            out.append(dict(citing=P,cited=Tk,title_score=round(al.score),title_ctx=t[max(0,al.dest_start-80):al.dest_end+40],intext=it))
json.dump(out,open('pass3.json','w'),ensure_ascii=False,indent=0)
print(len(out))
for o in out:
    if o['title_score']>=78: print(f"T{o['title_score']} {o['citing'][:20]:20} -> {o['cited'][:22]:22} | {o['title_ctx'][:170]}")
