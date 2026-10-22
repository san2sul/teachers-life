import json,os,re,base64,mimetypes
from urllib.parse import urlparse,parse_qs,unquote
from playwright.sync_api import sync_playwright
APP='__TL_APP__';SP='__TL_WORK__'
store={};ver=[0];sent=[];who={"email":"t@gmail.com","name":"물리 선생님"}
GIS="""window.google={accounts:{oauth2:{initTokenClient:function(c){return{requestAccessToken:function(o){window.__lastReq=o;setTimeout(function(){c.callback({access_token:'tok'+Math.random(),expires_in:3600})},20)}}},hasGrantedAllScopes:function(){return true},revoke:function(t,cb){cb&&cb()}}}};"""
def handler(route,req):
  u=urlparse(req.url)
  if u.netloc=='tl.test':
    path=u.path.lstrip('/') or 'index.html'
    if path=='config.js':return route.fulfill(body='window.TL_CONFIG={googleClientId:"123-test.apps.googleusercontent.com"};try{if(!localStorage.getItem("att-app-cheer"))localStorage.setItem("att-app-cheer",JSON.stringify({am:false,pm:false}))}catch(e){}',content_type='text/javascript')
    fp=os.path.join(APP,path)
    if not os.path.exists(fp):return route.fulfill(status=404,body='nf')
    return route.fulfill(path=fp,content_type=mimetypes.guess_type(fp)[0] or 'text/plain')
  if 'gsi/client' in req.url:return route.fulfill(body=GIS,content_type='text/javascript')
  if 'oauth2/v3/userinfo' in req.url:return route.fulfill(json=who)
  if 'gmail.googleapis.com' in req.url:
    raw=json.loads(req.post_data)['raw'];raw+= '='*(-len(raw)%4);sent.append(base64.urlsafe_b64decode(raw).decode());return route.fulfill(json={"id":"m"+str(len(sent))})
  if 'googleapis.com' in req.url:
    q=parse_qs(u.query);m=req.method;key=who['email']
    st=store.setdefault(key,{})
    if u.path=='/drive/v3/files' and m=='GET':return route.fulfill(json={"files":[{"id":k,"version":str(v['ver'])} for k,v in st.items()]})
    mm=re.match(r'/drive/v3/files/(\w+)',u.path)
    if mm and m=='GET':
      f=st.get(mm.group(1))
      if not f:return route.fulfill(status=404,json={"error":{"message":"nf"}})
      if q.get('alt')==['media']:return route.fulfill(body=f['body'],content_type='application/json')
      return route.fulfill(json={"id":mm.group(1),"version":str(f['ver'])})
    if u.path=='/upload/drive/v3/files' and m=='POST':
      body=req.post_data;content=body.split('\r\n\r\n')[2].rsplit('\r\n--',1)[0];ver[0]+=1;fid='f'+key[:3]+str(ver[0]);st[fid]={'body':content,'ver':ver[0]};return route.fulfill(json={"id":fid,"version":str(ver[0])})
    mm=re.match(r'/upload/drive/v3/files/(\w+)',u.path)
    if mm and m=='PATCH':ver[0]+=1;st[mm.group(1)]={'body':req.post_data,'ver':ver[0]};return route.fulfill(json={"id":mm.group(1),"version":str(ver[0])})
  return route.fulfill(status=404,body='blocked')
S={"active":"c1","list":[{"id":"c1","data":{"v":3,"cls":"1학년 1반","roster":[["10101","김가"],["10102","이나"],["10103","박다"]],"phones":{"10102":"010-3333-4444"},"emails":{"10102":"lee@ex.com"},"teachers":[],"msg":"m","sessions":[]}}],"staff":[],"tt":{"list":[],"active":""},"notes":{},"events":[]}
errs=[]
def ctx(b,w=390):
  c=b.new_context(viewport={"width":w,"height":860},service_workers="block",permissions=["clipboard-read","clipboard-write"],accept_downloads=True);c.route("**/*",handler);return c
with sync_playwright() as p:
  b=p.chromium.launch()
  T=ctx(b,1100).new_page();T.add_init_script("try{localStorage.setItem('att-app-gmail','1')}catch(e){}");T.on("response",lambda r:r.status==404 and print("404:",r.url[:90]));T.on("pageerror",lambda e:errs.append("T:"+str(e)));T.on("console",lambda m:m.type=="error" and "status of 404" not in m.text and errs.append("Tc:"+m.text))  # 404: 가짜 드라이브가 지운 파일에 답하는 정상 응답
  T.goto("https://tl.test/index.html");T.evaluate("s=>{localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-view','stat')}",json.dumps(S));T.reload();T.wait_for_timeout(500)
  T.set_input_files("#evFile",SP+"/eval_test.xlsx");T.wait_for_timeout(1500)
  print("UPLOAD:",T.inner_text("#sheetBox")[:420].replace("\n"," | "))
  T.screenshot(path=SP+"/ev_up.png")
  T.fill("#evReply","t@gmail.com");T.click("#evOk");T.wait_for_timeout(500)
  T.screenshot(path=SP+"/ev_detail.png",full_page=True)
  print("DETAIL:",T.inner_text("#evDetail")[:200].replace("\n"," | "))
  # copy link for student 1 (index 0)
  T.click("#evStu [data-a=copy][data-i='0']");T.wait_for_timeout(300);link=T.evaluate("navigator.clipboard.readText()");print("LINK len",len(link),link[:60])
  # student page
  Sp=ctx(b).new_page();Sp.on("pageerror",lambda e:errs.append("S:"+str(e)))
  Sp.goto(link);Sp.wait_for_timeout(600);print("SIGN:",Sp.inner_text("main")[:200].replace("\n"," | "))
  Sp.check("#ok");bx=Sp.locator("#cv").bounding_box()
  Sp.mouse.move(bx["x"]+30,bx["y"]+80);Sp.mouse.down()
  for i in range(30):Sp.mouse.move(bx["x"]+30+i*8,bx["y"]+80+(20 if i%6<3 else -20))
  Sp.mouse.up();Sp.wait_for_timeout(200);Sp.screenshot(path=SP+"/sg1.png")
  Sp.click("#send");Sp.wait_for_timeout(500);Sp.screenshot(path=SP+"/sg2.png")
  href=Sp.get_attribute("#mail","href");print("MAILTO:",unquote(href)[:160].replace("\n"," "))
  rlink=re.search(r'(https://tl\.test/(?:index\.html)?#r=[A-Za-z0-9_\-.]+)',unquote(href)).group(1);print("reply len",len(rlink))
  T.goto(rlink);T.wait_for_timeout(1000);print("AFTER R:",T.inner_text("#evDetail")[:120].replace("\n"," | "))
  # other students: sign via generated links and paste
  pastes=[]
  for i in (1,2):
    T.click(f"#evStu [data-a=copy][data-i='{i}']");T.wait_for_timeout(200);l=T.evaluate("navigator.clipboard.readText()")
    Sp.goto("about:blank");Sp.goto(l);Sp.wait_for_timeout(500);Sp.check("#ok");bx=Sp.locator("#cv").bounding_box()
    Sp.mouse.move(bx["x"]+40,bx["y"]+60);Sp.mouse.down()
    for k in range(20):Sp.mouse.move(bx["x"]+40+k*10,bx["y"]+60+k*3)
    Sp.mouse.up();Sp.click("#send");Sp.wait_for_timeout(400);pastes.append(unquote(Sp.get_attribute("#mail","href")))
  T.fill("#evPaste","\n".join(pastes));T.click("#evPasteOk");T.wait_for_timeout(500)
  print("AFTER PASTE:",T.inner_text("#evDetail")[:100].replace("\n"," | "))
  T.screenshot(path=SP+"/ev_done.png",full_page=True)
  T.click("#evXl");T.wait_for_timeout(300)
  with T.expect_download() as d:T.click("#eoOk")
  d.value.save_as(SP+"/ev_out.xlsx");print("XLSX:",d.value.suggested_filename)
  # gmail send: login first
  T.click(".navb[data-v=set]");T.wait_for_timeout(200);T.evaluate("document.querySelectorAll('#v-set details').forEach(d=>d.open=true)") or T.click("#gsLogin");T.wait_for_timeout(1200)
  T.click(".navb[data-v=stat]");T.wait_for_timeout(200)
  # clear one signature to make need list
  T.click("#evStu [data-a=unsig][data-i='2']");T.click("#skOk");T.wait_for_timeout(200)
  T.click("#evGm");T.wait_for_timeout(200);T.click("#skOk");T.wait_for_timeout(2500)
  print("GMAIL sent:",len(sent));print(sent[0][:300] if sent else "")
  # account switch
  who.update({"email":"school@hs.kr","name":"학교 계정"})
  T.click(".navb[data-v=set]");T.wait_for_timeout(300);T.evaluate("document.querySelectorAll('#v-set details').forEach(d=>d.open=true)") or T.click("#gsAdd");T.wait_for_timeout(1500)
  st=json.loads(T.evaluate("localStorage.getItem('att-app-v2')"));print("after switch classes:",[c['data']['cls'] for c in st['list']],"evals",len(st.get('evals',[])),"| accts:",T.inner_text(".accts"))
  who.update({"email":"t@gmail.com","name":"물리 선생님"})
  T.click("[data-acct='t@gmail.com']");T.wait_for_timeout(1500)
  st=json.loads(T.evaluate("localStorage.getItem('att-app-v2')"));print("switch back classes:",[c['data']['cls'] for c in st['list']],"evals",len(st.get('evals',[])))
  b.close()
print("errors:",errs)
