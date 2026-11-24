# Copies the R results (analysis/node_metrics.csv) into nodes.json and flags citations of newer papers in edges.json.
import json,csv
N=json.load(open('nodes.json')); E=json.load(open('edges.json')); M={r['id']:r for r in csv.DictReader(open('analysis/node_metrics.csv',encoding='utf-8'))}
for n in N:
    r=M[n['id']]
    n['cited_by']=int(r['cited_by']); n['cites']=int(r['cites']); n['potential_citers']=int(r['potential_citers'])
    n['community']=int(r['community']) if r['community'] else None
Y={n['id']:n['year'] for n in N}
for e in E: e['cited_is_newer']=Y[e['cited']]>Y[e['citing']]
json.dump(N,open('nodes.json','w'),ensure_ascii=False,indent=0); json.dump(E,open('edges.json','w'),ensure_ascii=False,indent=0)
print('merged R results into',len(N),'nodes')
