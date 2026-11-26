import json,math,re,matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Wedge,Circle
from matplotlib.lines import Line2D
nodes=json.load(open('nodes.json')); E=json.load(open('edges.json'))
CL=['1 Global sensory experience','2 Experience per sense','3 Perceptual features','4 Bodily involvement (no body part named)','5 Specific body part / effector','6 Body-object interaction']
COL=['#363ea9', '#b046b8', '#a9363e', '#a9a136', '#23931b', '#36a9a1']; GRAY='#8a8984'
N={n['id']:n for n in nodes}
def short(i):
    i=re.sub(r' et al\. \((\d{4})\)',r' et al. \1',i); i=re.sub(r' and (.+?) \((\d{4})\)',r' & \1 \2',i); return re.sub(r' \((\d{4})\)',r' \1',i)
fig,ax=plt.subplots(figsize=(11,9),dpi=150); ax.set_aspect('equal')
X=lambda n:n['x']; Y=lambda n:-n['y']*0.78
for e in E:
    a,b=N[e['citing']],N[e['cited']]; ax.plot([X(a),X(b)],[Y(a),Y(b)],color='#28282614',lw=0.6,zorder=1)
def R(n): return 0.006+0.0021*math.sqrt(n['cited_by'])
for n in sorted(nodes,key=lambda n:n['cited_by']):
    r=R(n); w=None if n['has_reference_list'] else r*0.5
    sl=[(COL[k-1],0.4 if s=='border' else 1) for k,s in n.get('pie',[])] or [(GRAY,1)]
    step=360/len(sl)
    for i,(c,o) in enumerate(sl):
        ax.add_patch(Wedge((X(n),Y(n)),r,90-(i+1)*step,90-i*step,width=w,facecolor=matplotlib.colors.to_rgba(c,o),edgecolor='white',lw=0.6 if len(sl)>1 else 0.4,zorder=3))
ax.set_xlim(-0.03,1.03); ax.set_ylim(-0.83,0.03)
lab=sorted([n for n in nodes if n['cited_by']>=16],key=lambda n:-n['cited_by'])
fig.canvas.draw(); rend=fig.canvas.get_renderer(); placed=[]
for n in lab:
    for dx,dy,ha,va in [(0,10,'center','bottom'),(0,-10,'center','top'),(10,0,'left','center'),(-10,0,'right','center'),(8,8,'left','bottom'),(-8,-8,'right','top'),(8,-8,'left','top'),(-8,8,'right','bottom')]:
        ppu=(ax.transData.transform((1,0))[0]-ax.transData.transform((0,0))[0])*72/fig.dpi; k=(R(n)*ppu+3)/10
        t=ax.annotate(short(n['id']),(X(n),Y(n)),xytext=(dx*k,dy*k),textcoords='offset points',ha=ha,va=va,fontsize=7.5,color='#52514e',zorder=4,bbox=dict(boxstyle='round,pad=0.1',fc='#fcfcfbdd',ec='none'),arrowprops=dict(arrowstyle='-',color='#8a8984',lw=0.5,shrinkA=0,shrinkB=R(n)*ppu))
        bb=t.get_window_extent(rend)
        if not any(bb.overlaps(p) for p in placed): placed.append(bb); break
        t.remove()
ax.set_axis_off()
H=[Line2D([],[],marker='o',ls='',markersize=8,markerfacecolor=COL[i],markeredgecolor='white',label=f"{c} ({sum(1 for n in nodes if any(k==i+1 for k,_ in n.get('pie',[])))})") for i,c in enumerate(CL)]
no=sum(1 for n in nodes if not n.get('pie'))
if no: H.append(Line2D([],[],marker='o',ls='',markersize=8,markerfacecolor=GRAY,markeredgecolor='white',label=f'Outside the categories ({no})'))
ax.legend(handles=H,loc='upper center',bbox_to_anchor=(0.5,0.0),ncol=2,frameon=False,fontsize=8.5,title='Pie slices = categories of the paper\'s scales (one equal slice each; n = papers with that category)\nNode size = cited by later table papers; ring = no reference list available',title_fontsize=8.5)
ax.set_title(f'Citation links among sensorimotor norm datasets ({len(nodes)} papers, {len(E)} links)',fontsize=11,loc='left')
fig.tight_layout(); import matplotlib; matplotlib.rcParams['svg.hashsalt']='sensorimotor-word-norms'  # reproducible ids
fig.savefig('citation_network_v2.svg',metadata={'Date':None}); fig.savefig('citation_network_v2.pdf',metadata={'CreationDate':None}); fig.savefig('citation_network_v2.png',dpi=150); print('ok')
