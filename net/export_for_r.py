# Writes the network as CSV files for the R analysis (analysis/communities.R).
import json,csv,os
os.makedirs('analysis',exist_ok=True)
N=json.load(open('nodes.json')); E=json.load(open('edges.json'))
with open('analysis/nodes.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['id','year','has_reference_list','main_category','language','study_type'])
    for n in N: w.writerow([n['id'],n['year'],int(bool(n['has_reference_list'])),n['cluster'],n['lang1'],n['study']])
with open('analysis/edges.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['citing','cited'])
    for e in E: w.writerow([e['citing'],e['cited']])
print('exported',len(N),'nodes',len(E),'edges')
