import os as _os
ROOT=_os.environ.get('SMN_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import re,json,sys,unicodedata
sys.path.insert(0,'.')
from titles import T
from rapidfuzz import fuzz
def fold(s):
    s=s.replace('ﬁ','fi').replace('ﬂ','fl').replace('–','-').replace('—','-').replace('’',"'").replace('‘',"'")
    s=unicodedata.normalize('NFKD',s); s=''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'\s+',' ',s)
rows=json.load(open('rows.json'))
papers={}
for x in rows:
    a=x['authors']
    if a.startswith('MSc'): continue
    papers.setdefault(a,x)
texts={}
for a,x in papers.items():
    if x['has']: texts[a]=fold(open(f'{ROOT}/txt/{a}.txt',encoding='utf-8',errors='ignore').read())
def refstart(t):
    m=None
    for m0 in re.finditer(r'\b(References|REFERENCES|Bibliography|BIBLIOGRAPHY|Literature Cited|Références|Referencias|Literatur|Bibliographie|Reference)\b',t): m=m0
    # choose last heading that is followed by many years
    best=None
    for m0 in re.finditer(r'\b(References|REFERENCES|Bibliography|BIBLIOGRAPHY|Literature Cited|Références|Referencias|Bibliographie)\b',t):
        seg=t[m0.end():m0.end()+3000]
        if len(re.findall(r'\b(19|20)\d\d\b',seg))>=8: best=m0.start() if best is None else best
    return best
out=[]
for P,t in texts.items():
    rs=refstart(t); low=t.lower()
    for Tk,(sur,yr,frag) in T.items():
        if Tk==P: continue
        s=fold(sur).lower(); f=fold(frag).lower()
        best=None
        for m in re.finditer(re.escape(s),low):
            pre=low[max(0,m.start()-6):m.start()]
            if re.search(r'(, |& |and |; |-)$',pre): continue   # co-author position or part of compound name
            win=low[m.start():m.start()+450]
            al=fuzz.partial_ratio_alignment(f,win) if len(f)>12 else None
            if al is None:
                i=win.find(f); sc=100 if i>=0 else 0; ds=i if i>=0 else 999
            else: sc=al.score; ds=al.dest_start
            seg=win[:ds]
            ys=re.findall(r'\b(?:19|20)\d\d(?=[a-z]?\b)',seg) if ds<400 else []
            nyear=len(ys)
            ys_all=re.findall(r'\b(?:19|20)\d\d(?=[a-z]?\b)',win[:ds+len(f)+120])
            yok=yr in ys_all; ynear=any(abs(int(y)-int(yr))==1 for y in ys_all)
            if ds>300 or nyear>1: continue
            inref= rs is not None and m.start()>=rs
            cand=(sc,yok,ynear,inref,m.start(),t[max(0,m.start()-20):m.start()+300])
            if best is None or (cand[0],cand[1],cand[3])>(best[0],best[1],best[3]): best=cand
        if best and best[0]>=70 and (best[1] or best[2]):
            out.append(dict(citing=P,cited=Tk,score=round(best[0]),year_exact=best[1],in_refsection=best[3],context=best[5]))
        else:
            # in-text fallback: surname (+ et al./and) followed by year
            m=re.search(re.escape(s)+r'[^()\d]{0,40}[\(,]?\s?'+yr+r'[a-z]?\b',low)
            if m: out.append(dict(citing=P,cited=Tk,score=0,year_exact=True,in_refsection=False,context='IN-TEXT ONLY: '+t[max(0,m.start()-60):m.end()+60]))
json.dump(out,open('raw_edges.json','w'),ensure_ascii=False,indent=0)
import collections
print(len(out),'candidate edges;',sum(1 for e in out if e['score']>=90 and e['year_exact']),'strong;',sum(1 for e in out if e['score']==0),'in-text only')
print('papers w/o ref section:',[P for P,t in texts.items() if refstart(t) is None])
