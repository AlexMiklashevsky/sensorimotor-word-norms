import json,openpyxl
from openpyxl.styles import Font
nodes=json.load(open('nodes.json')); E=json.load(open('edges.json')); R=json.load(open('results.json')); RJ=json.load(open('rejected.json'))
wb=openpyxl.Workbook(); ws=wb.active; ws.title='Papers'
ws.append(['Paper','Year','Language','Main category','All categories','Study type','Rater type','Reference list available','Citation community','Cited by','Could cite it','Cites','Paper link'])
for n in sorted(nodes,key=lambda n:n['id']): ws.append([n['id'],n['year'],n['language'],n['cluster'],n['cats'],n['study'],n['rater'],'yes' if n['has_reference_list'] else 'no',n.get('community'),n['cited_by'],n['potential_citers'],n['cites'],n['link']])
ws2=wb.create_sheet('Links'); ws2.append(['Citing paper','Cited paper','Cited paper is newer','Decision','Method','Reference entry (excerpt)'])
for e in sorted(E,key=lambda e:(e['citing'],e['cited'])): ws2.append([e['citing'],e['cited'],'yes' if e.get('cited_is_newer') else '',e['decision'],e['method'],(e.get('context') or '')[:500]])
ws3=wb.create_sheet('Rejected candidates'); ws3.append(['Citing paper','Cited paper','Reason'])
for e in RJ: ws3.append([e['citing'],e['cited'],e.get('reason','')])
ws4=wb.create_sheet('Communities'); ws4.append(['Community','Papers','Main categories','Study types','Most cited (cited by)','Mean pairwise co-assignment (100 runs)','Runs with all members together'])
for c,d in R['communities'].items(): ws4.append([int(c),d['size'],'; '.join(f"{a}: {b}" for a,b in d['categories']),'; '.join(f"{a}: {b}" for a,b in d['study']),'; '.join(f"{a} ({b})" for a,b in d['top']),d['mean_coassign'],d['together_all']])
ws5=wb.create_sheet('Summary')
for k in ['n_nodes_graph','n_edges','n_nodes_community','n_edges_community','modularity_best','stability_mean_ARI','stability_min_ARI','NMI_vs_cluster','ARI_vs_cluster','NMI_vs_study','ARI_vs_study','NMI_vs_language','ARI_vs_language','edges_same_category','newer_cited_edges']:
    ws5.append([k.replace('cluster','main category'),R[k]])
for s in wb.worksheets:
    for c in s[1]: c.font=Font(bold=True)
    s.freeze_panes='A2'
    for col in s.columns: s.column_dimensions[col[0].column_letter].width=min(60,max(10,max(len(str(c.value or '')) for c in col[:50])*0.9))
wb.save('citation_network_v2.xlsx'); print('ok')
