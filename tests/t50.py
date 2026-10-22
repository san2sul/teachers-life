import json,os,re,time,mimetypes
from urllib.parse import urlparse,parse_qs
from playwright.sync_api import sync_playwright
APP='__TL_APP__';SP='__TL_WORK__'
store={};ver=[0]
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
      return route.fulfill(json={"files":[{"id":k,"version":str(v['ver']),"modifiedTime":"x"} for k,v in store.items()]})
    mm=re.match(r'/drive/v3/files/(\w+)',u.path)
    if mm and m=='GET':
      f=store.get(mm.group(1))
      if not f:return route.fulfill(status=404,json={"error":{"message":"nf"}})
      if q.get('alt')==['media']:return route.fulfill(body=f['body'],content_type='application/json')
      return route.fulfill(json={"id":mm.group(1),"version":str(f['ver'])})
    if mm and m=='DELETE':store.pop(mm.group(1),None);return route.fulfill(status=204,body='')
    if u.path=='/upload/drive/v3/files' and m=='POST':
      body=req.post_data;parts=body.split('\r\n\r\n');content=parts[2].rsplit('\r\n--',1)[0]
      ver[0]+=1;store['f1']={'body':content,'ver':ver[0]};return route.fulfill(json={"id":"f1","version":str(ver[0])})
    mm=re.match(r'/upload/drive/v3/files/(\w+)',u.path)
    if mm and m=='PATCH':
      ver[0]+=1;store[mm.group(1)]={'body':req.post_data,'ver':ver[0]};return route.fulfill(json={"id":mm.group(1),"version":str(ver[0])})
  return route.fulfill(status=404,body='blocked')
S={"active":"c1","list":[{"id":"c1","data":{"v":3,"cls":"1학년 1반","roster":[["10101","김가"],["10102","이나"]],"phones":{"10101":"010-1111-2222"},"teachers":[],"msg":"m","sessions":[{"id":"s1","date":"2026-10-16","time":"09:00","label":"","p":{"10101":True}}]}},{"id":"c2","data":{"v":3,"cls":"1학년 2반","roster":[["10201","최다"]],"phones":{},"teachers":[],"msg":"m","sessions":[]}}],"staff":[{"id":"st1","name":"정교감","dept":"교무실","role":"교감","phone":"010-1234-0001"}],"tt":{"list":[],"active":""},"notes":{},"events":[]}
errs=[]
def dev(b,name,state=None):
  c=b.new_context(viewport={"width":1280 if name=="A" else 390,"height":900},service_workers="block",ignore_https_errors=True);c.route("**/*",handler)
  pg=c.new_page();pg.on("pageerror",lambda e:errs.append(name+":"+str(e)));pg.on("console",lambda m:m.type=="error" and errs.append(name+" console:"+m.text))
  pg.goto("https://tl.test/index.html")
  if state:pg.evaluate("s=>localStorage.setItem('att-app-v2',s)",json.dumps(state))
  pg.evaluate("localStorage.setItem('att-app-view','set')");pg.reload();pg.wait_for_timeout(500);return pg
def st(pg):return json.loads(pg.evaluate("localStorage.getItem('att-app-v2')"))
def summ(pg):s=st(pg);return [(c['data']['cls'],[r[1] for r in c['data']['roster']],len(c['data']['sessions'])) for c in s['list']],[x['name'] for x in s['staff']],len(s['events'])
with sync_playwright() as p:
  b=p.chromium.launch()
  A=dev(b,"A",S)
  A.evaluate("document.querySelectorAll('#v-set details').forEach(d=>d.open=true)") or A.click("#gsLogin");A.wait_for_timeout(1500)
  print("A after login:",A.inner_text("#gsBody")[:120].replace("\n"," | "),"| pill:",A.inner_text("#gsPill"),"| store:",list(store))
  A.screenshot(path=SP+"/gs_A.png")
  B=dev(b,"Bphone")
  print("B wizard:",B.is_visible(".wizw"));B.click("#wzHave");print("B sync open:",B.evaluate("document.getElementById('d-sync').open"))
  B.evaluate("document.querySelectorAll('#v-set details').forEach(d=>d.open=true)") or B.click("#gsLogin");B.wait_for_timeout(1500);print("B summary:",summ(B))
  # B adds a student via state edit and save()
  B.evaluate("()=>{}")
  # concurrent edits: A renames class c2 via UI-less: modify through app functions isn't exposed; use clsIn input on class c1
  A.evaluate("document.getElementById('clsIn').closest('details').open=true");A.fill("#clsIn","1학년 1반(물리)");A.wait_for_timeout(200)
  B.click(".navb[data-v=att]");B.wait_for_timeout(200);B.get_by_text("＋ 출석 체크 시작").click();B.wait_for_timeout(200);B.locator(".st").nth(1).click();B.wait_for_timeout(200)
  # both wait for autosync; A first
  A.wait_for_timeout(3500);B.wait_for_timeout(3500)
  print("store ver",ver[0])
  A.evaluate("document.querySelectorAll('#v-set details').forEach(d=>d.open=true)") or A.click("#gsPill");A.wait_for_timeout(1500);B.evaluate("document.querySelectorAll('#v-set details').forEach(d=>d.open=true)") or B.click("#gsPill");B.wait_for_timeout(1500)
  print("A:",summ(A));print("B:",summ(B))
  sa=st(A)['list'][0]['data'];sb=st(B)['list'][0]['data']
  print("A sessions",[x["p"] for x in sa["sessions"]],"cls",sa["cls"],"| B sessions",[x["p"] for x in sb["sessions"]],"cls",sb["cls"])
  B.screenshot(path=SP+"/gs_B.png")
  # device C with own data -> first link sheet
  S2={"active":"x1","list":[{"id":"x1","data":{"v":3,"cls":"2학년 3반","roster":[["20301","한별"]],"phones":{},"teachers":[],"msg":"m","sessions":[]}}],"staff":[],"tt":{"list":[],"active":""},"notes":{},"events":[]}
  C=dev(b,"C",S2);C.evaluate("document.querySelectorAll('#v-set details').forEach(d=>d.open=true)") or C.click("#gsLogin");C.wait_for_timeout(1500)
  print("C sheet:",C.inner_text("#sheetBox")[:160].replace("\n"," | "))
  C.click("#flMerge");C.wait_for_timeout(1500);print("C:",summ(C))
  A.evaluate("document.querySelectorAll('#v-set details').forEach(d=>d.open=true)") or A.click("#gsPill");A.wait_for_timeout(1500);print("A after C:",summ(A))
  # drop csv on A
  A.evaluate("""()=>{const f=new File(['학번,이름,전화번호\\n10103,박다,010-5555-6666'],'명단.csv',{type:'text/csv'});const dt=new DataTransfer();dt.items.add(f);window.dispatchEvent(new DragEvent('drop',{dataTransfer:dt,bubbles:true,cancelable:true}))}""")
  A.wait_for_timeout(300);print("drop choose:",A.inner_text("#sheetBox")[:80].replace("\n"," | "))
  A.locator("#sheetBox [data-i='0']").click();A.wait_for_timeout(800);print("bulk:",A.inner_text("#bkMsg")[:80])
  A.screenshot(path=SP+"/gs_drop.png")
  # logout
  A.keyboard.press("Escape")
  b.close()
print("errors:",errs)
