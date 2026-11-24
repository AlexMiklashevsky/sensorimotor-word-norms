import json,networkx as nx,math,random
nodes=json.load(open('nodes.json')); E=json.load(open('edges.json'))
G=nx.Graph(); G.add_nodes_from(n['id'] for n in nodes)
for e in E: G.add_edge(e['citing'],e['cited'])
H=G.subgraph([n for n in G if G.degree(n)>0]).copy()
pos=nx.kamada_kawai_layout(H)
import numpy as np
c=np.mean(np.array(list(pos.values())),axis=0)
for k,v in list(pos.items()):
    d=np.array(v)-c; r=np.linalg.norm(d)
    pos[k]=tuple(c+d/(r+1e-9)*(r**0.6)) if r>0 else tuple(v)
for n in G:
    if n not in pos: pos[n]=(0,0)
# place isolates in a row at the bottom
iso=[n for n in G if G.degree(n)==0]
xs=[p[0] for p in pos.values()]; ys=[p[1] for p in pos.values()]
core={k:v for k,v in pos.items() if k not in iso}
x0,x1=min(v[0] for v in core.values()),max(v[0] for v in core.values()); y0,y1=min(v[1] for v in core.values()),max(v[1] for v in core.values())
for i,n in enumerate(sorted(iso)): pos[n]=(x0+(i+0.5)*(x1-x0)/max(1,len(iso)), y0-(y1-y0)*0.12)
X0,X1=min(p[0] for p in pos.values()),max(p[0] for p in pos.values()); Y0,Y1=min(p[1] for p in pos.values()),max(p[1] for p in pos.values())
ORDER=['1 Global sensory experience','2 Experience per sense','3 Perceptual features','4 Bodily involvement (no body part named)','5 Specific body part / effector','6 Body-object interaction','Outside the categories']
ORDER=[c for c in ORDER if any(n['cluster']==c for n in nodes)]
lane={c:i for i,c in enumerate(ORDER)}
random.seed(3)
byl={}
# Stable layout: positions are stored in positions.json. Papers already there keep their place; new papers go next to the
# papers they are linked to (isolated new papers join the row of isolated papers). Run update_all.py --relayout to redo the whole layout.
import os,sys,hashlib
PF=os.path.join(os.path.dirname(os.path.abspath(__file__)),'positions.json')
deg=dict(G.degree())
if os.path.exists(PF) and os.environ.get('SMN_RELAYOUT')!='1':
    S=json.load(open(PF,encoding='utf-8')); placed={}
    for n in nodes:
        q=S.get(n['id'])
        if q and not (q['iso'] and deg[n['id']]>0) and not (not q['iso'] and deg[n['id']]==0): placed[n['id']]=(q['x'],q['y'])
    isoy=max([q['y'] for q in S.values() if q['iso']] or [1.0])
    def jit(i,k): return (int(hashlib.md5((i+k).encode()).hexdigest()[:6],16)/0xffffff-0.5)*0.04
    for _ in range(5):
        for n in nodes:
            i=n['id']
            if i in placed or deg[i]==0: continue
            nb=[placed[m] for m in G.neighbors(i) if m in placed]
            if nb or _==4: placed[i]=(round(min(0.98,max(0.02,(sum(p[0] for p in nb)/len(nb) if nb else 0.5)+jit(i,'x'))),4),round(min(0.9,max(0.02,(sum(p[1] for p in nb)/len(nb) if nb else 0.5)+jit(i,'y'))),4))
    used=[placed[i][0] for i in placed if deg[i]==0]
    for i in sorted(n['id'] for n in nodes if n['id'] not in placed and deg[n['id']]==0):
        x=0.02
        while any(abs(x-u)<0.03 for u in used): x+=0.03
        placed[i]=(round(min(x,0.98),4),isoy); used.append(x)
    for n in nodes: n['x'],n['y']=placed[n['id']]
    new=[n['id'] for n in nodes if n['id'] not in S]
    print('stored positions kept'+(f'; placed new papers {new}' if new else ''))
else:
    for n in nodes:
        p=pos[n['id']]; n['x']=round((p[0]-X0)/(X1-X0),4); n['y']=round(1-(p[1]-Y0)/(Y1-Y0),4)
    print('full layout computed')
json.dump({n['id']:{'x':n['x'],'y':n['y'],'iso':deg[n['id']]==0} for n in sorted(nodes,key=lambda n:n['id'])},open(PF,'w',encoding='utf-8'),ensure_ascii=False,indent=0)
for n in nodes:
    byl.setdefault((n['cluster'],n['year']),[]).append(n)
for (c,y),L in byl.items():
    for j,n in enumerate(sorted(L,key=lambda n:n['id'])):
        n['ty']=round((lane[c]+0.5+(j-(len(L)-1)/2)*0.17)/len(ORDER),4)
json.dump(nodes,open('nodes.json','w'),ensure_ascii=False,indent=0)
print('isolates',iso)
