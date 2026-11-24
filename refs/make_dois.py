# Rebuilds refs/dois.json (paper label -> DOI) from the paper links in work/records.json.
import json,os,re
ROOT=os.environ.get('SMN_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R=[r for r in json.load(open(ROOT+'/work/records.json')) if not r.get('_excluded')]
old=json.load(open(ROOT+'/refs/dois.json')) if os.path.exists(ROOT+'/refs/dois.json') else {}
D={}
for r in R:
    a=r['Authors']
    if a in D: continue
    m=re.search(r'10\.\d{4,9}/[^\s;,"<>]+',r.get('Paper link') or '')
    if m: D[a]=re.sub(r'[\.\)]+$','',m.group(0)).replace('/full','').replace('/abstract','')
    elif a in old: D[a]=old[a]
json.dump(D,open(ROOT+'/refs/dois.json','w'),ensure_ascii=False,indent=0)
print('dois',len(D))
