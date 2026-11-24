# Builds the overview table (Excel) from work/records.json, work/scales/all2.json and facets/coded2.json.
# Usage: python3 build_table.py OUTPUT.xlsx
import openpyxl, json, copy, re
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Font, PatternFill
def Q(v):
    if not isinstance(v,str): return v
    v=v.replace('“','"').replace('”','"').replace('‘',"'").replace('’',"'").replace('–','-').replace('—','-')
    return re.sub(r"(?<![A-Za-z0-9])'([^'\n]{1,200}?)'(?![A-Za-z0-9])",r'"\1"',v)
import sys,os
ROOT=os.environ.get('SMN_ROOT') or os.path.dirname(os.path.abspath(__file__))
V4=ROOT+'/templates/table_style_template.xlsx'
OUT=sys.argv[1] if len(sys.argv)>1 else ROOT+'/out/sensorimotor_norms_table.xlsx'
R=[r for r in json.load(open(ROOT+'/work/records.json')) if not r.get('_excluded')]
S=json.load(open(ROOT+'/work/scales/all2.json')); C=json.load(open(ROOT+'/facets/coded2.json'))
src=openpyxl.load_workbook(V4); h1=src['Sensorimotor norms'].cell(1,1); b1=src['Sensorimotor norms'].cell(2,1)
CATS=['1 Global sensory experience','2 Experience per sense','3 Perceptual features','4 Bodily involvement (no body part named)','5 Specific body part / effector','6 Body-object interaction']
COLS=['Language','Year','Authors','Publication type','Study type','Sensorimotor variables','Construct (coded)','Granularity']+CATS+['Number of items','Items (category)','Items (details)','Item type','Parts of speech','POS group','Item sampling','Rating scale','Raters (total)','Ratings per item','Rater population','Rater type','Rater group','Perspective','Collection mode','Reliability reported','Item SDs reported','Data level','Data repository / license','Other variables','Paper link','Data link','Comments']
W={'POS group':13,'Study type':20,'Rater type':12,'Rater group':20,'Perspective':18,'Language':14,'Year':7,'Authors':30,'Publication type':34,'Sensorimotor variables':40,'Construct (coded)':24,'Granularity':16,'Number of items':11,'Items (details)':34,'Items (category)':13,'Item type':22,'Parts of speech':20,'Item sampling':26,'Rating scale':30,'Raters (total)':18,'Ratings per item':16,'Rater population':26,'Collection mode':16,'Reliability reported':22,'Item SDs reported':14,'Data level':22,'Data repository / license':26,'Other variables':30,'Paper link':32,'Data link':32,'Comments':40}
# dataset-level category status
cat={}
for c in C:
    for k in range(1,7):
        v=c.get(f'cat{k}')
        if v in('core','border'):
            cur=cat.setdefault(c['key'],{}).get(k)
            if cur!='core': cat[c['key']][k]=v
def ckey(r): return (r['Language'], int(r['Year']) if str(r['Year']).isdigit() else 9999, r['Authors'])
R.sort(key=ckey)
ORIG={'Zhong et al. (2022)','Shao et al. (2025a)','Chen et al. (2019)','Popović Stijačić et al. (2023)','Speed and Majid (2017)','Speed and Brysbaert (2022)','Lynott et al. (2020)','Chedid et al. (2019)','Miceli et al. (2021)','Platonova and Miklashevsky (2025)','Striedl et al. (2024)','Morucci et al. (2019)','Vergallito et al. (2020)','Repetto et al. (2023)','Iida and Akita (2023)','Lee and Shin (2023)','Miklashevsky (2018)','Popović Stijačić and Filipović Đurđević (2025)','Díez-Álamo et al. (2018)','San Miguel Abella and González-Nosti (2020)'}
FLAG={'Kumcu and Yağlı (2021)'}
wb=openpyxl.Workbook(); ws=wb.active; ws.title='Sensorimotor norms'
def style_like(dst,s): dst.font=copy.copy(s.font); dst.fill=copy.copy(s.fill); dst.border=copy.copy(s.border); dst.alignment=copy.copy(s.alignment)
for j,h in enumerate(COLS,1):
    c=ws.cell(1,j,h); style_like(c,h1); c.alignment=Alignment(wrap_text=True,vertical='top')
    ws.column_dimensions[get_column_letter(j)].width=W.get(h,13)
catfill={'core':PatternFill('solid',fgColor='C6E0B4'),'border':PatternFill('solid',fgColor='FFE699')}
for i,r in enumerate(R,2):
    v3=r.get('_v3') or {}
    for j,h in enumerate(COLS,1):
        if h in CATS:
            k=int(h[0]); val=cat.get(r['_key'],{}).get(k,'')
        elif h=='Publication type':
            val=r['Publication type']+(f"; {v3['_purpose']}" if v3.get('_purpose') else '')
        elif h=='Language': val=v3.get('Language') or r['Language']
        elif h=='Comments':
            val=r.get('Comments') or ''
        elif h in v3 and h not in ('Language',): val=v3[h]
        elif h=='Raters (total)': val=r.get('Raters / ratings per item','')
        elif h=='Ratings per item': val=''
        else: val=r.get(h,'')
        cell=ws.cell(i,j,Q(val) if val is not None else '')
        cell.alignment=Alignment(wrap_text=True,vertical='top'); cell.font=copy.copy(b1.font)
        if h in CATS and val: cell.fill=catfill[val]; cell.alignment=Alignment(horizontal='center',vertical='top')
        if h=='Language' and (r['Authors'] not in ORIG or r['_key']=='Lee and Shin (2023)|English'): cell.fill=PatternFill('solid',fgColor='FFF2CC')
        if h=='Authors' and r['Authors'] in FLAG: cell.fill=PatternFill('solid',fgColor='FFFF00')
ws.freeze_panes='D2'; ws.auto_filter.ref=f"A1:{get_column_letter(len(COLS))}{ws.max_row}"
# instructions sheet
order={r['_key']:n for n,r in enumerate(R)}
rows=[s for s in S if s['key'] in order]; rows.sort(key=lambda x:order[x['key']])
code={(c['key'],c['scale']):c for c in C}
s2=wb.create_sheet('Instructions by scale')
IH=['Authors','Language','Scale','Category','Rating relation (R code)','Construct (coded)','Wording','Wording type','Scale range and anchors',"Don't-know option",'Original language / translation','Where in paper','Full text available in','Notes']
WD=[30,14,24,16,14,22,80,24,40,18,26,22,18,34]
for j,h in enumerate(IH,1):
    c=s2.cell(1,j,h); style_like(c,h1); c.alignment=Alignment(wrap_text=True,vertical='top'); s2.column_dimensions[get_column_letter(j)].width=WD[j-1]
byk={r['_key']:r for r in R}
for i,x in enumerate(rows,2):
    r=byk[x['key']]; cc=code.get((x['key'],x['scale']),{})
    cats=[f"{k}{'' if cc.get(f'cat{k}')=='core' else ' (border)'}" for k in range(1,7) if cc.get(f'cat{k}') in('core','border')]
    catv=', '.join(cats) if cats else (cc.get('status') or 'outside categories')
    vals=[r['Authors'],r['Language'],x['scale'],catv,cc.get('R',''),x.get('construct',''),x.get('wording',''),x.get('wtype',''),x.get('anchors',''),x.get('dk',''),x.get('lang',''),x.get('where',''),x.get('ft',''),x.get('notes','')]
    for j,v in enumerate(vals,1):
        c=s2.cell(i,j,Q(v)); c.alignment=Alignment(wrap_text=True,vertical='top')
s2.freeze_panes='C2'; s2.auto_filter.ref=f"A1:{get_column_letter(len(IH))}{s2.max_row}"
s3=wb.create_sheet('Code key')
KEY=[('Categories (dataset and scale level)',''),
('1','Global sensory experience (SER): one overall sensory rating'),('2','Experience per sense: one rating per modality'),('3','Perceptual features: specific features within a modality (color, motion, pain, temperature, etc.)'),
('4','Bodily involvement, no body part named'),('5','Specific body part / effector'),('6','Body-object interaction (BOI)'),
('core','green = core member of the category'),('',''),
('Rating relation (R code)',''),('R1','Experience ("to what extent do you experience ...")'),('R1p','Possible vs. actual experience rated separately'),
('R2a','Association / relatedness ("how related is the word to ...")'),('R2b','Feature relevance ("how relevant is the feature for the concept")'),
('R3','Ease of interaction (BOI-type)'),('R4','Object property ("how intense is the color of this object")'),('R4b','Feature salience (Binder et al., 2016)'),
('R6','Categorical choice, yes/no or number'),('R7','Behavior (e.g., frequency of use)'),('R1 [LLM]','LLM-generated ratings with experience-type prompt'),('R?','Unclear from available wording'),('',''),
('Number of items',''),('number','rated items in the dataset (the rated pool, not the subset selected for an experiment); empty if the paper does not state it'),('Items (category)','30-99, 100-299, 300-999, 1,000-2,999, 3,000-9,999, 10,000+ (steps of about x3, equal width on a log scale); empty if no number'),('Items (details)','breakdown, selected subsets or why the number is missing'),('',''),
('Parts of speech',''),('Nouns / Verbs / Adjectives','only that word class'),('Nouns, verbs ... (n / n)','several word classes named in the paper; counts in brackets where reported'),('Mixed (not specified)','several word classes, breakdown not reported'),('Other','classifiers, compounds, ideophones, ABB reduplicated words'),('POS group','Nouns / Verbs / Adjectives / Mixed / Other / Not reported (for filtering)'),('',''),
('Perspective',''),('own','rater\'s own experience or actions ("you experience", "you could perform")'),('typical person','generic body or person ("a human body", "someone")'),
('child','rated for a typical child ("an average 6-year-old")'),('possible vs. actual','both possible and actual experience rated'),('not specified','verbatim wording asks about association / relatedness without reference to a person'),
('(empty)','wording not available, or only paraphrased in the paper without saying whose experience is rated')]
for i,(a,b) in enumerate(KEY,1):
    s3.cell(i,1,a).font=Font(bold=(b=='')); s3.cell(i,2,b).alignment=Alignment(wrap_text=True,vertical='top')
s3.column_dimensions['A'].width=34; s3.column_dimensions['B'].width=90
wb.save(OUT); print('datasets',ws.max_row-1,'scale rows',s2.max_row-1)
