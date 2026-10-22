src=open('audit2.py').read();exec(src.split("sizes=")[0])
import datetime,openpyxl,sys
td=datetime.date.today();wd=td.weekday();T0=td.isoformat()
tt=S["tt"]["list"][0]
tt["cells"]={f"{wd}-1":{"subject":"물리","clsId":"c1","clsName":"","room":"과학실"},f"{wd}-3":{"subject":"통합과학","clsId":"c2","clsName":"","room":""},f"{wd}-5":{"subject":"물리","clsId":"c1","clsName":"","room":""}}
tt["chg"]=[{"id":"g1","scope":"cell","d":wd,"p":5,"from":T0,"to":T0,"type":"cancel","reason":"학교 행사","created":1}]
ros=S["list"][0]["data"]["roster"]
S["list"][0]["data"]["sessions"]=[{"id":"sx","date":T0,"time":"09:00","label":"1교시 물리","p":{r[0]:True for r in ros[2:]},"src":f"t1:{wd}:1"},
  {"id":"sy","date":(td-datetime.timedelta(days=1)).isoformat(),"time":"09:00","label":"1교시 물리","p":{r[0]:True for r in ros[1:]}},
  {"id":"sz","date":(td-datetime.timedelta(days=1)).isoformat(),"time":"13:00","label":"5교시","p":{r[0]:True for r in ros}}]
S["list"][0]["data"]["obs"]=[{"id":"o1","sid":"10101","date":"2026-10-01","tags":{"a1":2,"a3":1},"memo":"실험 설계에서 변인 통제를 스스로 제안함","at":1},{"id":"o2","sid":"10101","date":"2026-10-08","tags":{"a1":1},"memo":"모둠 발표를 이끎","at":1}]
S["evals"][0]["due"]=(td+datetime.timedelta(days=2)).isoformat()
with sync_playwright() as p:
  b=p.chromium.launch();c=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,service_workers="block",accept_downloads=True);c.route("**/*",handler);T=c.new_page();T.on("pageerror",lambda e:errs.append(str(e)))
  T.goto("https://tl.test/index.html");T.evaluate("s=>{localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-lastver','9.9.9');localStorage.setItem('att-app-me','김물리');localStorage.setItem('att-app-setup','1')}",json.dumps(S));T.reload();T.wait_for_timeout(500)
  T.click(".navb[data-v=todo]");T.wait_for_timeout(200)
  print("nav label:",T.inner_text(".navb[data-v=todo]").strip()," date:",T.inner_text("#tdDate"))
  print("TODAY:",T.inner_text("#tdToday").replace("\n"," | "))
  T.screenshot(path=SP+"/shot/today.png",full_page=True)
  T.click("#tdToday [data-i='1']");T.wait_for_timeout(200)
  print("after click lesson3: view att:",T.evaluate("!document.getElementById('v-att').hidden"),"cls:",T.inner_text("#cls"),"ses label:",T.input_value("#sLabel"))
  T.click(".navb[data-v=todo]");T.click("#tdToday [data-call='0']");T.wait_for_timeout(200)
  print("call view:",T.evaluate("!document.getElementById('v-call').hidden"),T.inner_text("#callSub"))
  T.click(".navb[data-v=todo]");T.click("#tdToday [data-sg='0']");T.wait_for_timeout(200);print("eval open:",T.is_visible("#evBack"))
  # student sheet
  T.click(".navb[data-v=att]");T.evaluate("(()=>{const c=S.list.find(x=>x.id==='c1');})()") if False else None
  T.click("[data-m=obs]");T.wait_for_timeout(150);print("stsCnt:",T.inner_text("#stsCnt"))
  T.click("#obsList [data-s='10101']");T.click("#obAll");T.wait_for_timeout(150)
  print("STU:",T.inner_text(".stk").replace("\n"," "))
  T.click("#stsGen");T.wait_for_timeout(100);print("draft:",T.input_value("#stsT"));print("meter:",T.inner_text("#stsN"))
  T.screenshot(path=SP+"/shot/stu.png",full_page=True)
  T.fill("#stsT","가"*400+"\nabc ");T.wait_for_timeout(700);print("meter2:",T.inner_text("#stsN"))
  T.fill("#stsT","가"*600);T.wait_for_timeout(700);print("meter3:",T.inner_text("#stsN"))
  T.click("#skNo");print("saved sts:",T.evaluate("Object.keys(JSON.parse(localStorage.getItem('att-app-v2')).list[0].data.sts||{})"),"cnt:",T.inner_text("#stsCnt"))
  T.click("#stsAll");T.wait_for_timeout(100);print("fillall sheet:",T.inner_text("#sheetBox")[:80].replace("\n"," "))
  with T.expect_download() as dl:T.click("#stsXl")
  f=dl.value;fp=SP+"/sts.xlsx";f.save_as(fp);ws=openpyxl.load_workbook(fp).active;print("sts xlsx:",[[c.value for c in r] for r in ws.iter_rows(min_row=4,max_row=5)])
  T.click(".navb[data-v=stat]");T.click("#stabs .chip[data-t=att]");T.click("#monXl");T.wait_for_timeout(100);print("month sheet:",T.inner_text("#maM"))
  with T.expect_download() as dl:T.click("#maOk")
  fp=SP+"/mon.xlsx";dl.value.save_as(fp);wb=openpyxl.load_workbook(fp);ws=wb.active;print("mon sheets:",wb.sheetnames,ws.page_setup.orientation)
  for r in ws.iter_rows(min_row=1,max_row=7):print("  ",[c.value for c in r])
  b.close()
print(errs)
