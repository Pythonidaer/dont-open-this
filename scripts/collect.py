"""Read public English News listing metadata; compare against the post sitemap.
No article bodies, credentials, or private APIs are collected.
"""
import json,re,html,time,threading,urllib.request,urllib.error,xml.etree.ElementTree as ET,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from urllib.parse import urljoin,urlsplit
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[1]
CACHE=Path('/workspace/scratch/fcc-list-cache');CACHE.mkdir(exist_ok=True)
BASE='https://www.freecodecamp.org/news/'
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
sitemap_path=CACHE/'sitemap-posts.xml'
if not sitemap_path.exists():
 result=subprocess.run(['curl','-f','-L','--max-time','30','-sS',BASE+'sitemap-posts.xml','-o',str(sitemap_path)],capture_output=True,text=True)
 if result.returncode:raise RuntimeError('Sitemap retrieval failed: '+result.stderr[:200])
sitemap=ET.parse(sitemap_path)
entries=sitemap.findall('.//s:url',ns)
urls={e.find('s:loc',ns).text:e.find('s:lastmod',ns).text if e.find('s:lastmod',ns) is not None else None for e in entries}
def norm(u):return u.rstrip('/')+'/'
urls={norm(k):v for k,v in urls.items()}
def text(s):return html.unescape(re.sub('<[^>]*>','',s)).strip()
def parse(s):
 out=[]
 for card in re.findall(r'<article\b[^>]*class="post-card"[^>]*>(.*?)</article>',s,re.S):
  title=re.search(r'<h2 class="post-card-title">\s*<a href="([^"]+)">(.*?)</a>',card,re.S)
  if not title:continue
  tags=re.findall(r'<a[^>]+href="([^"]*/tag/[^"/]+/?)"[^>]*>(.*?)</a>',card,re.S)
  author=re.search(r'<a[^>]*class="meta-item"[^>]*>(.*?)</a>',card,re.S)
  date=re.search(r'<time[^>]+datetime="([^"]+)"',card)
  out.append(dict(url=norm(urljoin(BASE,html.unescape(title[1]))),title=text(title[2]),tags=[text(t[1]).lstrip('#') for t in tags],author=text(author[1]) if author else None,date=date[1] if date else None,metadataSource='public-listing'))
 return out
stop=threading.Event()
def fetch(i):
 p=CACHE/f'{i}.html'
 if p.exists():return i,parse(p.read_text()),None
 if stop.is_set():return i,[], 'stopped after access error'
 u=BASE+(f'{i}/' if i else '')
 try:
  result=subprocess.run(['curl','-L','--max-time','22','-sS','-w','\n%{http_code}',u],capture_output=True,text=True)
  s,_,status=result.stdout.rpartition('\n')
  if status!='200':
   if status in ('403','429'):stop.set()
   return i,[],'HTTP '+status+' '+result.stderr[:120]
  if 'post-card-title' not in s:return i,[],'no article cards'
  p.write_text(s);time.sleep(.18)
  return i,parse(s),None
 except Exception as e:
  if isinstance(e,urllib.error.HTTPError) and e.code in (403,429):stop.set()
  return i,[],str(e)
allposts={};errors=[];pages=0
# Fetch the sitemap-sized public listing range; retain any differences explicitly.
with ThreadPoolExecutor(max_workers=4) as pool:
 futures=[pool.submit(fetch,i) for i in range((len(urls)+24)//25)]
 for future in as_completed(futures):
  i,records,error=future.result()
  if error:errors.append({'page':i,'error':error})
  else:pages+=1
  for r in records:allposts[r['url']]=r
  if (pages+len(errors))%25==0:print(json.dumps({'pages':pages,'records':len(allposts),'errors':len(errors)}),flush=True)
# Preserve sitemap-only entries as explicit URL-only records; no guessed author/date/tag.
for u,modified in urls.items():
 if u not in allposts:allposts[u]=dict(url=u,title=None,tags=[],author=None,date=None,metadataSource='sitemap-only',modified=modified)
for p in allposts.values():p['inSitemap']=p['url'] in urls
posts=list(allposts.values());posts.sort(key=lambda p:(p['date'] or '',p['url']),reverse=True)
manifest=dict(collected=datetime.now(ZoneInfo('America/New_York')).date().isoformat(),timezone='America/New_York',sitemapURL=BASE+'sitemap-posts.xml',sitemapCount=len(urls),indexed=len(posts),withMetadata=sum(p['metadataSource']=='public-listing' for p in posts),sitemapOnly=sum(p['metadataSource']=='sitemap-only' for p in posts),listingOnly=sum(not p['inSitemap'] for p in posts),pagesFetched=pages,errors=[e for e in errors if e['error']!='stopped after access error'],pagesSkipped=sum(e['error']=='stopped after access error' for e in errors),tagScope='Primary topic tag exposed by public listing cards; not a complete per-article tag inventory.')
(ROOT/'dist/articles.json').write_text(json.dumps(dict(manifest=manifest,articles=posts),ensure_ascii=False,separators=(',',':')))
(ROOT/'INVENTORY.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(manifest),flush=True)
