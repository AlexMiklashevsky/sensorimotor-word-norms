# Which papers have a full text with a reference list. The full texts (txt/) are copyrighted and stay off the public
# repository, so their availability is stored in fulltext_available.json: refreshed whenever txt/ is present, read otherwise.
import os,json
ROOT=os.environ.get('SMN_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F=os.path.join(ROOT,'net','fulltext_available.json')
def available():
    t=os.path.join(ROOT,'txt')
    if os.path.isdir(t):
        s=sorted(f[:-4] for f in os.listdir(t) if f.endswith('.txt') and os.path.getsize(os.path.join(t,f))>5000)
        json.dump(s,open(F,'w',encoding='utf-8'),ensure_ascii=False,indent=0)
        return set(s)
    return set(json.load(open(F,encoding='utf-8')))
