from pathlib import Path
from html.parser import HTMLParser
import subprocess,concurrent.futures,re,json,html
p=Path(__file__).parent/'references'
class Text(HTMLParser):
 def __init__(self):super().__init__();self.out=[]
 def handle_data(self,data):self.out.append(data)
ids={917,928,931,935,940,941,943,944,945,946,947,948,949,951,952,953,954,956,957,958,959,961,966,967,968,969,970,971,972,974,975,976,977,978,980,984,985,986,987,988,989,990,991,992,993,997,998,1001,1002,1003,1014,1016,1017}
urls=[u for u in json.loads((p/'catalog_urls.json').read_text()) if int(u.split('/home/')[1].split('-')[0]) in ids]
def get(u):
 ident=u.split('/home/')[1].split('-')[0];f=p/(ident+'.html')
 r=subprocess.run(['curl','-sSL','--fail','--max-time','25',u,'-o',str(f)],capture_output=True)
 if r.returncode:return {'url':u,'error':r.returncode}
 s=f.read_text();m=re.search(r'data-product="([^"]+)"',s)
 if not m:return {'url':u,'error':'Missing product data'}
 data=json.loads(html.unescape(m.group(1)))
 raw=re.sub('</(?:p|h2|h3)>','\n',data.get('description',''))
 text=html.unescape(re.sub('<[^>]+>','',raw));(p/(ident+'.txt')).write_text(text)
 partmatch=re.search(r'Part number:\s*([^\n]+)',text,re.I)
 ims=list(dict.fromkeys(re.findall(r'https://www.zd-racing.com/\d+-large_default/[^"\s<>]+',s)))
 return {'id':ident,'url':u,'description':text,'title':data.get('name'),'part_number':partmatch.group(1).strip() if partmatch else '', 'images':ims[:1]}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e:results=list(e.map(get,urls))
(p/'parts_review.json').write_text(json.dumps(results,indent=2,ensure_ascii=False))
for r in results:
 print(r.get('id',r['url']),r.get('error','OK'))
 for line in r.get('description','').splitlines():
  if re.search(r'\bsize\b|\d\s*mm|\d\s*[x×*]\s*\d|specification|teeth|\b38T\b|\b46T\b',line,re.I):print(' ',line)
