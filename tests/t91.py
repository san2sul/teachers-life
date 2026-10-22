src=open('audit2.py').read();exec(src.split("sizes=")[0])
import copy as _c
tt=S["tt"]["list"][0];tt["start"]="08:40";tt["classMin"]=45;tt["breakMin"]=10;tt["lunchMin"]=50
tt["pre"]=[{"id":"pr1","name":"조례","start":"08:20","len":10,"clsId":"c1"}]
tt["chg"].append({"id":"gd1","scope":"day","d":0,"p":1,"from":"2026-10-28","to":"2026-10-30","type":"cancel","reason":"2학기 중간고사","created":1})
tt["days"]={"2026-10-27":{"start":"09:00","classMin":40,"breakMin":10,"lunchMin":50,"note":"단축수업"}}
for i in range(3,9):S["list"].append({"id":f"c{i}","data":{"v":3,"cls":f"{1+i//5}학년 {i}반","roster":[[f"1{i:02d}01","학생{i}"]],"phones":{},"emails":{},"teachers":[],"msg":"m","sessions":[]}})
S["staff"]=[{"id":"st1","name":"정교감","role":"교감","dept":"교무부","phone":"010-9999-0000"},{"id":"st2","name":"한부장","role":"부장","dept":"과학부","phone":"010-8888-0000"}]
with sync_playwright() as p:
  b=p.chromium.launch()
  c=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,service_workers="block");c.route("**/*",handler);A=c.new_page();A.on("pageerror",lambda e:errs.append("A:"+str(e)))
  A.goto("https://tl.test/index.html");A.evaluate("s=>{localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-lastver','9.9.9');localStorage.setItem('att-app-me','김부장');localStorage.setItem('att-app-setup','1')}",json.dumps(S));A.reload();A.wait_for_timeout(500)
  A.click(".navb[data-v=set]");A.evaluate("document.getElementById('d-share').open=true");A.wait_for_timeout(100)
  print("ttnote:",A.inner_text("#shTtNote"))
  A.click("#shSchool");A.wait_for_timeout(100);print("sum:",A.inner_text("#shSum"))
  A.locator("#d-share").screenshot(path=SP+"/shot/share_send.png")
  A.click("#mkLink");A.wait_for_timeout(500);url=A.inner_text("#linkOut");print("url len:",len(url))
  # receiver: fresh
  c2=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,service_workers="block");c2.route("**/*",handler);B=c2.new_page();B.on("pageerror",lambda e:errs.append("B:"+str(e)))
  B.goto(url);B.wait_for_timeout(1200)
  print("wizard shown:",B.is_visible(".wizw"))
  print("RECV:",B.inner_text("#sheetBox")[:500].replace("\n"," | "))
  B.screenshot(path=SP+"/shot/share_recv.png",full_page=False)
  B.click("#rcQ [data-q=none]");B.click("#rcCls [data-i='0']");B.click("#rcCls [data-i='1']");print(B.inner_text("#rcSum"))
  B.click("#rcOk");B.wait_for_timeout(400)
  st=B.evaluate("JSON.parse(localStorage.getItem('att-app-v2'))")
  print("classes:",[(x['data']['cls'],x['data'].get('year'),x['data'].get('term'),len(x['data']['roster'])) for x in st['list']])
  print("staff:",[(x['name'],x.get('phone'),x.get('year'),x.get('term')) for x in st['staff']],"period:",st.get('period'))
  t=st['tt']['list'][0];print("tt:",t['year'],t['term'],t['start'],t['classMin'],t['lunchMin'],"pre:",[(x['name'],x['start'],x['clsId']==st['list'][0]['id']) for x in t['pre']],"chg:",[(x['reason'],x['scope']) for x in t['chg']],"days:",list(t['days']),"cells:",len(t['cells']))
  print("toast:",B.evaluate("(document.querySelector('.toast')||{}).textContent"));B.wait_for_timeout(2000);print("wizard after:",B.is_visible(".wizw"),B.inner_text(".wizh") if B.is_visible(".wizw") else "");B.screenshot(path=SP+"/shot/share_wiz.png");B.click("#wzN");B.click("#wzN");B.wait_for_timeout(100);print("wiz step3:",B.evaluate("document.querySelector('.wizcls')?document.querySelector('.wizcls').textContent:'-'"),B.evaluate("document.querySelector('.wizh').textContent"));B.click("#wzX")
  # re-import same link: should update not duplicate
  B.goto(url);B.wait_for_timeout(1000);B.click("#rcOk");B.wait_for_timeout(300)
  st=B.evaluate("JSON.parse(localStorage.getItem('att-app-v2'))");t=st['tt']['list'][0]
  print("re-import classes:",len(st['list']),"chg:",len(t['chg']),"pre:",len(t['pre']),"staff:",len(st['staff']))
  # tags only share
  A.evaluate("document.getElementById('d-share').open=true");A.evaluate("()=>{for(const id of ['shStu','shTc','shStaff','shTime','shCal']){const e=document.getElementById(id);if(e.checked)e.click()} }");A.click("#shTags");print("tags sum:",A.inner_text("#shSum"))
  A.click("#mkLink");A.wait_for_timeout(400);url2=A.inner_text("#linkOut")
  B.goto(url2);B.wait_for_timeout(1000);print("tags recv:",B.inner_text("#sheetBox")[:160].replace("\n"," | "));B.click("#rcTags");B.click("#rcOk");B.wait_for_timeout(200);print("toast:",B.evaluate("(document.querySelector('.toast')||{}).textContent"))
  b.close()
print(errs)
