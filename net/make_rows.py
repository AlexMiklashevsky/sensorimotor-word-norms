# Rebuilds rows.json (input of the citation matching scripts match.py / pass2.py / pass3.py) from work/records.json.
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from fulltext import available
ROOT=os.environ.get('SMN_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R=[r for r in json.load(open(ROOT+'/work/records.json')) if not r.get('_excluded')]
rows=[]; FT=available()
for r in R:
    a=r['Authors']
    rows.append({'key':r['_key'],'authors':a,'lang':r['Language'],'year':str(r['Year']),'has':a in FT,'link':r.get('Paper link','')})
json.dump(rows,open(os.path.join(ROOT,'net','rows.json'),'w'),ensure_ascii=False,indent=0)
print('rows',len(rows))
