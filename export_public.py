# Writes the public, fixed-name outputs of the repository (called by update_all.py after the build):
#   docs/index.html                      the web page (GitHub Pages)
#   data/sensorimotor_norms_table.xlsx   the overview table (one row per paper and language)
#   data/datasets.csv                    the same table as CSV
#   data/scales.csv                      one row per rating scale, with its coding
#   data/citation_links.csv              citation links between the papers
#   data/citation_network.xlsx           papers, links, communities and summary of the network analysis
#   data/references.md / .bib / .ris    reference list (APA 7, BibTeX, RIS)
#   data/codebook.md                     description of every column of the CSV files
#   figures/citation_network.(png|svg|pdf)
# Usage: python3 export_public.py <path of the built table xlsx>
import os,sys,csv,json,re,shutil,html,unicodedata
import openpyxl
ROOT=os.path.dirname(os.path.abspath(__file__)); NET=os.path.join(ROOT,'net')
DATA=os.path.join(ROOT,'data'); DOCS=os.path.join(ROOT,'docs'); FIG=os.path.join(ROOT,'figures')
for d in (DATA,DOCS,FIG): os.makedirs(d,exist_ok=True)
table=sys.argv[1]

# ---- page, workbooks, figures
page=open(os.path.join(NET,'citation_network_v2.html'),encoding='utf-8').read().replace('citation_network_v2.xlsx','citation_network.xlsx')
open(os.path.join(DOCS,'index.html'),'w',encoding='utf-8').write(page)
if os.path.abspath(table)!=os.path.abspath(os.path.join(DATA,'sensorimotor_norms_table.xlsx')): shutil.copy(table,os.path.join(DATA,'sensorimotor_norms_table.xlsx'))
shutil.copy(os.path.join(NET,'citation_network_v2.xlsx'),os.path.join(DATA,'citation_network.xlsx'))
for e in ('png','svg','pdf'): shutil.copy(os.path.join(NET,f'citation_network_v2.{e}'),os.path.join(FIG,f'citation_network.{e}'))

# ---- make the workbooks byte-reproducible (fixed zip entry times and document dates), so unchanged data give unchanged files
import zipfile
def normalize_xlsx(path):
    zin=zipfile.ZipFile(path); items=[(i.filename,zin.read(i.filename)) for i in zin.infolist()]; zin.close()
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in items:
            if name=='docProps/core.xml': data=re.sub(rb'(<dcterms:(created|modified)[^>]*>)[^<]*',rb'\g<1>2026-01-01T00:00:00Z',data)
            zi=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0)); zi.compress_type=zipfile.ZIP_DEFLATED; z.writestr(zi,data)
for f in ('sensorimotor_norms_table.xlsx','citation_network.xlsx'): normalize_xlsx(os.path.join(DATA,f))

# ---- CSV files (UTF-8, comma-separated, header row; empty cell = not reported / not applicable)
def sheet_rows(path,name):
    ws=openpyxl.load_workbook(path,read_only=True)[name]
    rows=[['' if v is None else v for v in r] for r in ws.iter_rows(values_only=True)]
    return [r for r in rows if any(str(v).strip() for v in r)]
def write_csv(name,rows):
    with open(os.path.join(DATA,name),'w',encoding='utf-8',newline='') as f: csv.writer(f,lineterminator='\n').writerows(rows)
    return rows[0]
heads={}
heads['datasets.csv']=write_csv('datasets.csv',sheet_rows(table,'Sensorimotor norms'))
heads['scales.csv']=write_csv('scales.csv',sheet_rows(table,'Instructions by scale'))
heads['citation_links.csv']=write_csv('citation_links.csv',sheet_rows(os.path.join(NET,'citation_network_v2.xlsx'),'Links'))

# ---- references: APA (markdown), BibTeX, RIS
R=json.load(open(os.path.join(ROOT,'refs','references.json'),encoding='utf-8'))
B=json.load(open(os.path.join(ROOT,'refs','bib_meta.json'),encoding='utf-8'))
def plain(h): return html.unescape(re.sub(r'<(?!/?i>)[^>]+>','',h)).replace('<i>','*').replace('</i>','*')
with open(os.path.join(DATA,'references.md'),'w',encoding='utf-8') as f:
    f.write('# References\n\nAll papers in the overview (APA 7th edition).\n\n')
    for lab in R['order']: f.write(plain(R['html'][lab])+'\n\n')
def ascii_(s): return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode()
keys={}
def bibkey(lab):
    m=re.match(r'(.+?) (?:et al\.|and .+?)? ?\((\d{4})([ab]?)\)$',lab)
    k=re.sub(r'[^A-Za-z]','',ascii_(m.group(1).split(' and ')[0]))+m.group(2)+m.group(3)
    base=k; i=0
    while k in keys.values(): i+=1; k=base+'abcdefgh'[i]
    keys[lab]=k; return k
def bibesc(s): return str(s).replace('&','\\&').replace('%','\\%').replace('#','\\#').replace('_','\\_')
def names(L): return ' and '.join(f'{f}, {g}' if g else f'{{{f}}}' for f,g in L)
bib=[]; ris=[]
RISTY={'article':'JOUR','inproceedings':'CPAPER','incollection':'CHAP','phdthesis':'THES','book':'BOOK','misc':'GEN','unpublished':'UNPB'}
for lab in R['order']:
    e=B.get(lab,{}); k=bibkey(lab)
    if e.get('missing') or not e: sys.exit(f'export_public: no structured reference metadata for {lab} (add it to refs/manual_refs_meta.json)')
    flds=[('author',names(e['authors'])),('title','{'+bibesc(e['title'])+'}'),('year',e['year'])]
    if e.get('editors'): flds.append(('editor',names(e['editors'])))
    for f in ('journal','booktitle','series','volume','number','pages','publisher','school','note'):
        if e.get(f): flds.append((f,bibesc(e[f]).replace('-','--') if f=='pages' else bibesc(e[f])))
    if e.get('doi'): flds.append(('doi',e['doi']))
    if e.get('url'): flds.append(('url',e['url']))
    bib.append(f"@{e['type']}{{{k},\n"+',\n'.join(f'  {a} = {{{v}}}' if not v.startswith('{') else f'  {a} = {v}' for a,v in flds)+'\n}\n')
    r=[f"TY  - {RISTY.get(e['type'],'GEN')}"]+[f'AU  - {f}, {g}'.rstrip(', ') for f,g in e['authors']]+[f'ED  - {f}, {g}'.rstrip(', ') for f,g in e.get('editors',[])]
    r+=[f"TI  - {e['title']}",f"PY  - {e['year']}"]
    if e.get('journal'): r.append(f"JO  - {e['journal']}")
    if e.get('booktitle'): r.append(f"T2  - {e['booktitle']}")
    if e.get('series'): r.append(f"T3  - {e['series']}")
    if e.get('volume'): r.append(f"VL  - {e['volume']}")
    if e.get('number'): r.append(f"IS  - {e['number']}")
    if e.get('pages'):
        sp,_,ep=e['pages'].partition('-'); r.append(f'SP  - {sp}')
        if ep: r.append(f'EP  - {ep}')
    if e.get('publisher') or e.get('school'): r.append(f"PB  - {e.get('publisher') or e.get('school')}")
    if e.get('note'): r.append(f"N1  - {e['note']}")
    if e.get('doi'): r.append(f"DO  - {e['doi']}")
    if e.get('url'): r.append(f"UR  - {e['url']}")
    ris.append('\n'.join(r+[f'ID  - {k}','ER  - '])+'\n')
open(os.path.join(DATA,'references.bib'),'w',encoding='utf-8').write('\n'.join(bib))
open(os.path.join(DATA,'references.ris'),'w',encoding='utf-8').write('\n'.join(ris))

# ---- codebook
CB=json.load(open(os.path.join(ROOT,'codebook_columns.json'),encoding='utf-8'))
missing=[(f,h) for f,H in heads.items() for h in H if h not in CB.get(f,{})]
if missing: sys.exit('export_public: columns without a codebook description (add them to codebook_columns.json): '+'; '.join(f'{f}: {h}' for f,h in missing))
with open(os.path.join(DATA,'codebook.md'),'w',encoding='utf-8') as f:
    f.write(open(os.path.join(ROOT,'codebook_intro.md'),encoding='utf-8').read().rstrip()+'\n')
    for fn,H in heads.items():
        n=sum(1 for _ in open(os.path.join(DATA,fn),encoding='utf-8'))-1
        f.write(f'\n## {fn}\n\n{CB[fn]["_file"]} {n} rows.\n\n| Column | Description |\n|---|---|\n')
        for h in H: f.write(f'| {h} | {CB[fn][h]} |\n')
print('public outputs written: docs/index.html, data/ (table, 3 CSV files, network workbook, references .md/.bib/.ris, codebook), figures/')
