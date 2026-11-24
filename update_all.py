# Rebuilds everything from the data files and runs the consistency checks.
# Usage: python3 update_all.py                      (public outputs with fixed names: docs/, data/, figures/)
#        python3 update_all.py --table-version 22 --network-version 31   (also versioned copies in out/, for the Drive)
# Always written: docs/index.html, data/*, figures/* (see export_public.py) and out/check_report.txt
# Requirements: R 4.x with igraph and jsonlite (community analysis); Python 3.9+ with openpyxl, networkx, numpy, scipy, matplotlib (layout, figures), rapidfuzz (citation matching only).
import os,sys,subprocess,shutil,argparse
ROOT=os.path.dirname(os.path.abspath(__file__)); os.environ['SMN_ROOT']=ROOT
ap=argparse.ArgumentParser(); ap.add_argument('--table-version',type=int); ap.add_argument('--network-version',type=int)
ap.add_argument('--relayout',action='store_true',help='recompute the whole network layout instead of keeping stored positions (net/positions.json)')
ap.add_argument('--skip-network-analysis',action='store_true',help='reuse nodes/edges/communities; only rebuild texts, page, figures')
a=ap.parse_args(); os.environ['SMN_RELAYOUT']='1' if a.relayout else '0'; OUT=os.path.join(ROOT,'out'); os.makedirs(OUT,exist_ok=True)
def run(script,cwd=ROOT,*args):
    print('>>',script,*args); r=subprocess.run([sys.executable,script,*args],cwd=cwd)
    if r.returncode: sys.exit(f'STOPPED: {script} failed (see the error above)')
NET=os.path.join(ROOT,'net')
TABLE=os.path.join(ROOT,'data','sensorimotor_norms_table.xlsx'); os.makedirs(os.path.dirname(TABLE),exist_ok=True)
run('build_table.py',ROOT,TABLE)
if a.table_version: shutil.copy(TABLE,os.path.join(OUT,f'sensorimotor_norms_table_v{a.table_version}.xlsx'))
run('net/make_rows.py'); run('refs/make_dois.py')
if not a.skip_network_analysis:
    run('assemble_v2.py',NET); run('export_for_r.py',NET)
    print('>> Rscript analysis/communities.R'); r=subprocess.run(['Rscript','analysis/communities.R'],cwd=NET,env=dict(os.environ,LANG='C.UTF-8',LC_ALL='C.UTF-8'))
    if r.returncode: sys.exit('STOPPED: the R analysis failed (is R with the packages igraph and jsonlite installed?)')
    run('merge_r.py',NET); run('layout_v2.py',NET)
for s in ['enrich_filters.py','make_graphdata.py']: run(s,NET)
run('refs/build_refs.py')
for s in ['build_page_v2.py','static_fig_v2.py','make_xlsx_v2.py']: run(s,NET)
run('export_public.py',ROOT,TABLE)
v=a.network_version
if v:
    html=open(os.path.join(NET,'citation_network_v2.html'),encoding='utf-8').read().replace('citation_network_v2.xlsx',f'citation_network_v{v}.xlsx')
    open(os.path.join(OUT,f'citation_network_v{v}.html'),'w',encoding='utf-8').write(html)
    for e in ['xlsx','png','svg','pdf']: shutil.copy(os.path.join(NET,f'citation_network_v2.{e}'),os.path.join(OUT,f'citation_network_v{v}.{e}'))
run('check_all.py')
print('\nDone. Public outputs in docs/, data/, figures/'+(f'; versioned copies in {OUT}' if a.table_version or v else ''))
