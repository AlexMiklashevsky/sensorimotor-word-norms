import json
nodes=json.load(open('nodes.json')); E=json.load(open('edges.json')); R=json.load(open('results.json'))
keep=['id','year','language','cluster','cats','pie','rater','study','community','cited_by','potential_citers','cites','has_reference_list','x','y','ty','link','f_rt','f_rg','f_pp','f_pos','f_nb','n_items','f_dim','f_scale','f_st','rpi','vars','pop']
D=dict(nodes=[{k:n.get(k) for k in keep if n.get(k) is not None} for n in nodes],edges=[[e['citing'],e['cited'],1 if e.get('cited_is_newer') else 0] for e in E],res={k:v for k,v in R.items() if k not in('communities','category_mixing','studytype_mixing')})
json.dump(D,open('graphdata.json','w'),ensure_ascii=False,separators=(',',':'))
