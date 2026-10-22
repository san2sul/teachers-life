src=open('audit2.py').read();exec(src.split("sizes=")[0])
import openpyxl
tt=S["tt"]["list"][0];tt["cells"]={"0-1":{"subject":"물리","clsId":"c1","clsName":"","room":""},"1-2":{"subject":"물리","clsId":"c1","clsName":"","room":""}}
tt["chg"]=[{"id":"g1","scope":"cell","d":0,"p":1,"from":"2026-10-19","to":"2026-10-19","type":"cancel","reason":"결강","created":1},{"id":"g2","scope":"day","d":0,"p":1,"from":"2026-10-20","to":"2026-10-20","type":"cancel","reason":"재량휴업","created":2}]
ros=S["list"][0]["data"]["roster"][:3];S["list"][0]["data"]["roster"]=ros
S["list"][0]["data"]["sessions"]=[{"id":"s1","date":"2026-10-19","time":"09:00","label":"1교시 물리","p":{},"src":"t1:0:1"},
 {"id":"s2","date":"2026-10-20","time":"09:55","label":"2교시 물리","p":{},"src":"t1:1:2"},
 {"id":"s3","date":"2026-10-16","time":"09:00","label":"수업","p":{ros[0][0]:True}},
 {"id":"s4","date":"2026-10-21","time":"09:00","label":"수업","p":{ros[0][0]:True,ros[1][0]:True}}]
with sync_playwright() as p:
  b=p.chromium.launch();c=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,service_workers="block",accept_downloads=True);c.route("**/*",handler);T=c.new_page();T.on("pageerror",lambda e:errs.append(str(e)))
  T.goto("https://tl.test/index.html");T.evaluate("s=>{localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-lastver','9.9.9');localStorage.setItem('att-app-me','김물리');localStorage.setItem('att-app-setup','1')}",json.dumps(S));T.reload();T.wait_for_timeout(500)
  T.click(".navb[data-v=stat]");T.click("#stabs .chip[data-t=att]");T.click("#presets [data-p=all]");T.wait_for_timeout(200)
  print("KPI:",T.inner_text("#kpis").replace("\n"," "))
  print("byStu:",T.inner_text("#stuTbl").replace("\n"," | ")[:300])
  T.click("#monXl");T.wait_for_timeout(100)
  with T.expect_download() as dl:T.click("#maOk")
  fp=SP+"/mon2.xlsx";dl.value.save_as(fp);ws=openpyxl.load_workbook(fp).active
  for r in ws.iter_rows(min_row=4,max_row=7,values_only=True):print("  ",r)
  # attendance view for 10/19
  T.click(".navb[data-v=att]");T.fill("#date","2026-10-19");T.dispatch_event("#date","change");T.wait_for_timeout(200)
  print("offBar:",T.inner_text("#offBar"),"| stats:",T.inner_text("#sp"),T.inner_text("#sa"),"| tab:",T.inner_text("#tabs .tab >> nth=0").replace("\n"," "))
  print("nav call badge:",T.evaluate("document.getElementById('navCnt').hidden"))
  # manual off on 10/21
  T.fill("#date","2026-10-21");T.dispatch_event("#date","change");T.wait_for_timeout(200)
  print("offBar 10/21:",T.inner_text("#offBar"))
  T.click("#offSet");T.wait_for_timeout(150);T.click("#sheetBox button:has-text('결강')");T.wait_for_timeout(200)
  print("after set:",T.inner_text("#offBar"),"|",T.inner_text("#sa"))
  T.click(".navb[data-v=stat]");T.click("#stabs .chip[data-t=att]");T.wait_for_timeout(200);print("KPI2:",T.inner_text("#kpis").replace("\n"," "))
  T.click(".navb[data-v=att]");T.click("#offUndo");T.wait_for_timeout(150);print("undo:",T.inner_text("#sa"))
  b.close()
print(errs)
