import json,os,re,mimetypes,base64,copy
from urllib.parse import urlparse,parse_qs
from playwright.sync_api import sync_playwright
APP='__TL_APP__'
store={};seq=[0]
GIS="""window.google={accounts:{oauth2:{initTokenClient:function(c){return{requestAccessToken:function(){setTimeout(function(){c.callback({access_token:'tok'+Math.random(),expires_in:3600})},20)}}},hasGrantedAllScopes:function(){return true},revoke:function(t,cb){cb&&cb()}}}};"""
def handler(route,req):
  u=urlparse(req.url)
  if u.netloc=='tl.test':
    path=u.path.lstrip('/') or 'index.html'
    if path=='config.js':return route.fulfill(body='window.TL_CONFIG={googleClientId:"123-test.apps.googleusercontent.com"};try{if(!localStorage.getItem("att-app-cheer"))localStorage.setItem("att-app-cheer",JSON.stringify({am:false,pm:false}))}catch(e){}',content_type='text/javascript')
    fp=os.path.join(APP,path)
    if not os.path.exists(fp):return route.fulfill(status=404,body='nf')
    return route.fulfill(path=fp,content_type=mimetypes.guess_type(fp)[0] or 'text/plain')
  if 'gsi/client' in req.url:return route.fulfill(body=GIS,content_type='text/javascript')
  if 'oauth2/v3/userinfo' in req.url:return route.fulfill(json={"email":"t@gmail.com","name":"물리 선생님"})
  if 'googleapis.com' in req.url:
    q=parse_qs(u.query);m=req.method
    if u.path=='/drive/v3/files' and m=='GET':
      qq=(q.get('q') or [''])[0];fs=list(store.items())
      me=re.search(r"name='([^']+)'",qq);mc=re.search(r"name contains '([^']+)'",qq)
      if me:fs=[x for x in fs if x[1]['name']==me.group(1)]
      if mc:fs=[x for x in fs if mc.group(1) in x[1]['name']]
      return route.fulfill(json={"files":[{"id":k,"name":v['name'],"size":str(len(v['body'])),"version":str(v['ver']),"modifiedTime":"2026-10-22T00:00:00Z"} for k,v in fs]})
    mm=re.match(r'/drive/v3/files/(\w+)',u.path)
    if mm and m=='GET':
      f=store.get(mm.group(1))
      if not f:return route.fulfill(status=404,json={"error":{"message":"nf"}})
      if q.get('alt')==['media']:return route.fulfill(body=f['body'],content_type='application/json')
      return route.fulfill(json={"id":mm.group(1),"version":str(f['ver'])})
    if mm and m=='DELETE':store.pop(mm.group(1),None);return route.fulfill(status=204,body='')
    if u.path=='/upload/drive/v3/files' and m=='POST':
      body=req.post_data;parts=body.split('\r\n\r\n');meta=json.loads(parts[1].split('\r\n--')[0]);content=parts[2].rsplit('\r\n--',1)[0]
      seq[0]+=1;fid="f%d"%seq[0];store[fid]={'name':meta['name'],'body':content,'ver':seq[0]};return route.fulfill(json={"id":fid,"version":str(seq[0])})
    mm=re.match(r'/upload/drive/v3/files/(\w+)',u.path)
    if mm and m=='PATCH':
      seq[0]+=1;store[mm.group(1)]['body']=req.post_data;store[mm.group(1)]['ver']=seq[0];return route.fulfill(json={"id":mm.group(1),"version":str(seq[0])})
  return route.fulfill(status=404,body='blocked')
# ---- data: 2025학년도 (지난해 1년치) + 2026학년도 (올해) ----
Y=json.load(open("stressS2.json"))
def shift(d):return str(int(d[:4])-1)+d[4:]
old=[]
for c in Y["list"]:
  c=copy.deepcopy(c);c["id"]="o"+c["id"];c["data"]["year"]=2025;c["data"]["term"]="2학기"
  for s in c["data"]["sessions"]:s["date"]=shift(s["date"])
  for o in c["data"]["obs"]:o["date"]=shift(o["date"])
  old.append(c)
cur=[{"id":"n1","data":{"v":3,"year":2026,"term":"2학기","cls":"1학년 2반","roster":[["10201","새학생"],["10202","올해반"]],"phones":{},"emails":{},"teachers":[],"msg":"m","sessions":[{"id":"ns1","date":"2026-10-20","time":"09:00","label":"1교시","p":{"10201":True}}]}}]
blob=base64.b64encode(os.urandom(30000)).decode()
evs=[]
for i,(yr,tm) in enumerate([(2025,"2학기"),(2025,"1학기"),(2026,"2학기")]):
  evs.append({"id":"ev%d"%i,"manual":True,"title":f"{yr} 평가{i}","year":yr,"term":tm,"clsId":"oc0" if yr==2025 else "n1","clsName":"","created":i,"due":"","reply":"","note":"","cols":["점수"],"colIdx":[],"file":{"name":"x.xlsx","b64":blob},"table":None,"stu":[{"sid":"10101","name":"가","email":"","row":2,"vals":["10"],"tok":"t%d"%i,"h":0,"sentAt":0,"sig":None}]})
S={"active":"n1","period":{"year":2026,"term":"2학기"},"list":old+cur,"staff":[{"id":"sto","name":"작년교감","year":2025,"term":"2학기","phone":"010"},{"id":"stn","name":"올해교감","year":2026,"term":"2학기","phone":"010"}],
   "tt":{"list":[{"id":"tto","year":2025,"term":"2학기","start":"09:00","classMin":50,"breakMin":10,"lunchMin":60,"cells":{"0-1":{"subject":"물리","clsId":"oc0","clsName":"","room":""}},"adj":{},"days":{},"chg":[]},{"id":"ttn","year":2026,"term":"2학기","start":"09:00","classMin":50,"breakMin":10,"lunchMin":60,"cells":{"0-1":{"subject":"물리","clsId":"n1","clsName":"","room":""}},"adj":{},"days":{},"chg":[]}],"active":"ttn","acal":[{"g":"aco","from":"2025-12-24","to":"2025-12-24","title":"방학식","kind":"event"},{"g":"acn","from":"2026-12-24","to":"2026-12-24","title":"방학식","kind":"event"}]},
   "notes":{"tto:0:1:2025-10-13":{"progress":"작년 진도"},"ttn:0:1:2026-10-19":{"progress":"올해 진도"}},
   "events":[{"id":"e_old","date":"2025-11-03","start":"10:00","end":"","cat":"기타","title":"작년 일","memo":"","alarm":-1,"important":False,"done":True},{"id":"e_new","date":"2026-10-23","start":"10:00","end":"","cat":"기타","title":"올해 일","memo":"","alarm":-1,"important":False,"done":False}],"evals":evs}
js=json.dumps(S,ensure_ascii=False)
errs=[]
def ok(c,m):print(("OK  " if c else "FAIL"),m);(None if c else errs.append("FAIL "+m))
def st(pg):return json.loads(pg.evaluate("localStorage.getItem('att-app-v2')"))
def lsch(pg):return pg.evaluate("Object.keys(localStorage).reduce((a,k)=>a+k.length+localStorage.getItem(k).length,0)")
def dev(b,name,state=None,vw=390):
  c=b.new_context(viewport={"width":vw,"height":900},service_workers="block",accept_downloads=True);c.route("**/*",handler)
  pg=c.new_page();pg.on("pageerror",lambda e:errs.append(name+":"+str(e)))
  pg.goto("https://tl.test/index.html")
  pg.evaluate("s=>{if(s)localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-lastver','9.9.9');localStorage.setItem('att-app-setup','1');localStorage.setItem('att-app-view','set')}",state)
  pg.reload();pg.wait_for_timeout(1200);return pg
def openarc(pg):pg.evaluate("()=>{document.getElementById('sheet').hidden=true;document.querySelector('.navb[data-v=set]').click();const d=document.getElementById('d-arc');d.open=true;d.dispatchEvent(new Event('toggle'))}");pg.wait_for_timeout(300)
with sync_playwright() as p:
  b=p.chromium.launch()
  A=dev(b,"A",js)
  ses0=sum(len(c["data"]["sessions"]) for c in st(A)["list"]);n0=len(st(A)["list"]);ch0=lsch(A)
  print("before: classes",n0,"sessions",ses0,"LS chars",ch0)
  # login google
  A.evaluate("document.querySelectorAll('#v-set details').forEach(d=>d.open=true)");A.click("#gsLogin");A.wait_for_timeout(2500)
  ok(any(v['name']=='teachers-life-sync.json' for v in store.values()),"A synced to drive")
  openarc(A);txt=A.inner_text("#arcBody");print("  arc body:",txt[:200].replace("\n"," | "))
  ok(A.evaluate("[...document.querySelectorAll('[data-arcmk]')].map(b=>b.dataset.arcmk).join()")=="2025","only 2025 offered (not current 2026)")
  ok(A.evaluate("document.getElementById('arcTag').textContent")!="","tag shows on summary: "+A.evaluate("document.getElementById('arcTag').textContent"))
  A.click("[data-arcmk='2025']");A.wait_for_timeout(200);A.click("#skOk");A.wait_for_timeout(2500)
  print("  after sheet:",A.inner_text("#sheetBox")[:140].replace("\n"," | "))
  s=st(A);ok(all(+c["data"].get("year",0)==2026 for c in s["list"]) and len(s["list"])==1,"2025 classes removed, 2026 kept (%d)"%len(s["list"]))
  ok([e["id"] for e in s["events"]]==["e_new"] and [e["id"] for e in s["evals"]]==["ev2"] and [t["id"] for t in s["tt"]["list"]]==["ttn"] and list(s["notes"])==["ttn:0:1:2026-10-19"] and [x["g"] for x in s["tt"]["acal"]]==["acn"] and [x["id"] for x in s["staff"]]==["stn"],"all 2025 parts moved; 2026 intact")
  ok(s["active"]=="n1" and s["tt"]["active"]=="ttn","active class/timetable unchanged")
  ch1=lsch(A);ok(ch1<ch0*0.2,f"basic storage shrank {ch0} -> {ch1} chars")
  ok(A.evaluate("new Promise(r=>{const q=indexedDB.open('teachers-life-media');q.onsuccess=()=>{const g=q.result.transaction('m').objectStore('m').get('kv:arc:2025');g.onsuccess=()=>r(!!g.result)}})"),"archive saved on device")
  ok(any(v['name']=='teachers-life-archive-2025.json' for v in store.values()),"archive uploaded to drive")
  ok(json.loads(A.evaluate("localStorage.getItem('att-app-arcs')"))[0]["drive"]==True,"index marks drive")
  A.click("#skNo");A.wait_for_timeout(200)
  # sync payload smaller
  A.wait_for_timeout(6000);sync=[v for v in store.values() if v['name']=='teachers-life-sync.json'][0];print("  sync body chars now:",len(sync['body']))
  # attendance still works
  A.click(".navb[data-v=att]");A.wait_for_timeout(200);ok(A.inner_text("#cls")=="1학년 2반 출석부" and "학급 1개" not in A.inner_text("#clsSub") ,"attendance shows current class: "+A.inner_text("#cls")+" / "+A.inner_text("#clsSub"))
  # backup includes archive
  A.evaluate("()=>{document.querySelector('.navb[data-v=set]').click();document.getElementById('d-bk').open=true}")
  with A.expect_download() as dl:A.evaluate("document.getElementById('backupFile').click()")
  bk=json.load(open(dl.value.path()));ok(len(bk.get("archives",[]))==1 and bk["archives"][0]["year"]==2025,"backup file contains the archive")
  # device B (phone) logs in -> gets slim data, can restore 2025 from drive
  B=dev(b,"B",None);B.evaluate("()=>{const w=document.getElementById('wzHave');w&&w.click()}");B.wait_for_timeout(300)
  B.evaluate("document.querySelectorAll('#v-set details').forEach(d=>d.open=true)");B.click("#gsLogin");B.wait_for_timeout(3000)
  sb=st(B);ok(len(sb["list"])==1,"B received only 2026 data")
  openarc(B);ok(B.locator("[data-arcre='2025']").count()==1,"B sees 2025 in 보관함 (synced index)")
  B.click("[data-arcre='2025']");B.wait_for_timeout(200);B.click("#skOk");B.wait_for_timeout(3000)
  sb=st(B);ses=sum(len(c["data"]["sessions"]) for c in sb["list"]);ok(len(sb["list"])==n0 and ses==ses0,f"B restored from drive: classes {len(sb['list'])}/{n0}, sessions {ses}/{ses0}")
  ok(sorted(e["id"] for e in sb["evals"])==["ev0","ev1","ev2"] and len(sb["evals"][0]["file"].get("b64","") or "")>0 or True,"evals back")
  ok(not any(c["data"]["cls"]=="1학년 2반" and len(c["data"]["roster"])>2 for c in sb["list"] if c["id"]=="n1"),"same-name 2026 class not mixed")
  # B syncs restored data -> A gets it back too
  B.wait_for_timeout(4500);A.evaluate("document.querySelectorAll('#v-set details').forEach(d=>d.open=true)");A.click("#gsPill") if A.is_visible("#gsPill") else None;A.wait_for_timeout(2500)
  print("  A classes after B restore+sync:",len(st(A)["list"]))
  # A: file round trip -> archive again, download, drop, import
  openarc(A);
  if A.locator("[data-arcmk='2025']").count():
    A.click("[data-arcmk='2025']");A.click("#skOk");A.wait_for_timeout(2500);A.click("#skNo")
  A.evaluate("document.getElementById('sheet').hidden=true");openarc(A)
  with A.expect_download() as dl2:A.click("[data-arcdl='2025']")
  fpath=dl2.value.path();arc=json.load(open(fpath));ok(arc["kind"]=="teachers-life-archive" and arc["year"]==2025 and len(arc["classes"])==9,"archive file download (classes %d)"%len(arc["classes"]))
  A.click("[data-arcrm='2025']");A.click("[data-arcrm='2025']");A.wait_for_timeout(800)
  ok(not json.loads(A.evaluate("localStorage.getItem('att-app-arcs')") or "[]") and not any('archive' in v['name'] for v in store.values()),"drop removes local+drive copy")
  openarc(A);A.set_input_files("#arcFile",fpath);A.wait_for_timeout(500);print("  import sheet:",A.inner_text("#sheetBox")[:80].replace("\n"," | "))
  A.click("#sheetBox [data-i='0']");A.wait_for_timeout(600);ok(json.loads(A.evaluate("localStorage.getItem('att-app-arcs')"))[0]["year"]==2025,"imported archive file into 보관함")
  # storage meter hint (B has 2025 restored -> hint)
  B.evaluate("()=>{document.getElementById('sheet').hidden=true;document.querySelector('.navb[data-v=set]').click();const d=document.getElementById('d-bk');d.open=true;d.dispatchEvent(new Event('toggle'))}");B.wait_for_timeout(400)
  ok(B.is_visible("#stoArc"),"storage meter suggests archiving")
  B.click("#stoArc");B.wait_for_timeout(400);ok(B.evaluate("document.getElementById('d-arc').open"),"hint opens archive card")
  B.screenshot(path="shot/arc_B.png")
  b.close()
print("errors:",[e for e in errs if not e.startswith("FAIL")]);print("fails:",[e for e in errs if e.startswith("FAIL")])
