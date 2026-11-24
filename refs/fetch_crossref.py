# Downloads Crossref metadata for DOIs in refs/dois.json that are not yet in refs/crossref_refs_meta.json.
# Needs internet access to api.crossref.org. Optional: set the environment variable SMN_CONTACT_EMAIL
# (Crossref's "polite pool" asks for a contact address in the User-Agent).
import json,os,time,urllib.request,urllib.parse
ROOT=os.environ.get('SMN_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=json.load(open(ROOT+'/refs/dois.json')); P=ROOT+'/refs/crossref_refs_meta.json'; M=json.load(open(P))
ua='sensorimotor-norms-overview'+(f" (mailto:{os.environ['SMN_CONTACT_EMAIL']})" if os.environ.get('SMN_CONTACT_EMAIL') else '')
todo=[d for d in D.values() if d not in M or 'err' in M[d]]
print('to fetch',len(todo))
for d in todo:
    try:
        req=urllib.request.Request('https://api.crossref.org/works/'+urllib.parse.quote(d),headers={'User-Agent':ua})
        m=json.load(urllib.request.urlopen(req,timeout=30))['message']
        dp=(m.get('published-print') or m.get('published-online') or m.get('issued') or {}).get('date-parts')
        M[d]={'a':[[x.get('family') or x.get('name',''),x.get('given','')] for x in m.get('author',[])],'y':(m.get('issued',{}).get('date-parts') or [[None]])[0][0],'yp':dp[0][0] if dp else None,
              't':(m.get('title') or [''])[0],'st':(m.get('subtitle') or [''])[0] if m.get('subtitle') else '','c':(m.get('container-title') or [''])[0],'v':m.get('volume',''),'i':m.get('issue',''),
              'p':m.get('page',''),'an':m.get('article-number',''),'ty':m.get('type',''),'ed':[[x.get('family'),x.get('given','')] for x in m.get('editor',[])],'pub':m.get('publisher','')}
        print('ok',d)
    except Exception as e:
        M[d]={'err':str(e)}; print('ERROR',d,e)
    time.sleep(0.5)
json.dump(M,open(P,'w'),ensure_ascii=False)
