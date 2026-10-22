import json,re
from playwright.sync_api import sync_playwright
S={"active":"c1","list":[
 {"id":"c1","data":{"v":3,"cls":"1학년 1반","roster":[["10101","김가"],["10102","이나"]],"phones":{"10101":"010-1111-2222","10102":"010-3333-4444"},"teachers":[{"id":"t1","name":"박수학","role":"수학","phone":"010-5555-6666"}],"msg":"m","sessions":[{"id":"s1","date":"2026-10-13","time":"09:00","label":"","p":{"10101":True}}]}},
 {"id":"c2","data":{"v":3,"cls":"1학년 2반","roster":[["10201","최다"]],"phones":{"10201":"010-7777-8888"},"teachers":[],"msg":"m","sessions":[]}}],
 "staff":[{"id":"s1","name":"정교감","dept":"교무실","role":"교감","phone":"010-1234-0001"},{"id":"s2","name":"한부장","dept":"학생부","role":"부장","phone":"010-1234-0002"},{"id":"s3","name":"오선생","dept":"학생부","role":"","phone":"010-1234-0003"}],
 "tt":{"list":[],"active":""},"notes":{},"events":[]}
errs=[]
with sync_playwright() as p:
  b=p.chromium.launch()
  ctx=b.new_context(viewport={"width":390,"height":844},permissions=["clipboard-read","clipboard-write"])
  pg=ctx.new_page();pg.add_init_script("try{if(!localStorage.getItem('att-app-cheer'))localStorage.setItem('att-app-cheer',JSON.stringify({am:false,pm:false}))}catch(e){}");pg.on("pageerror",lambda e:errs.append(str(e)))
  pg.goto("http://localhost:8766/index.html");pg.evaluate("s=>{localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-view','set')}",json.dumps(S));pg.reload()
  pg.wait_for_timeout(500)
  print("warn:",pg.inner_text("#appUrlWarn"))
  pg.evaluate("document.querySelectorAll('#v-set details').forEach(d=>d.open=true)") or pg.click("#appQr");pg.wait_for_timeout(800);print("appqr img:",pg.locator("#appQrBox img").count())
  pg.evaluate("document.querySelectorAll('#v-set details').forEach(d=>d.open=true)") or pg.click("#appCopy");print("clip:",pg.evaluate("navigator.clipboard.readText()")[:60].replace("\n"," "))
  print("sum0:",pg.inner_text("#shSum"))
  pg.click("#shCls [data-all]");pg.check("#shPh");pg.check("#shStaff");pg.wait_for_timeout(100)
  print("sum1:",pg.inner_text("#shSum"))
  pg.evaluate("document.querySelectorAll('#v-set details').forEach(d=>d.open=true)") or pg.click("#shStaffPick");pg.click("#pkStD [data-d='교무실']");pg.click("#pkStOk")
  print("sum2:",pg.inner_text("#shSum"))
  pg.check("#shStPh")
  pg.locator("#d-share").screenshot(path="__TL_WORK__/sh1.png")
  pg.click("#mkLink");pg.wait_for_timeout(300);url=pg.inner_text("#linkOut");print("url len",len(url))
  pg.click("#linkQrBtn");pg.wait_for_timeout(500);print("linkqr img:",pg.locator("#linkQr img").count(),pg.inner_text("#linkQr")[:40])
  # validation
  pg.uncheck("#shStu");pg.uncheck("#shTc");pg.uncheck("#shStaff");pg.click("#mkLink");pg.wait_for_timeout(200);print("toast:",pg.inner_text("#toast") if pg.locator("#toast").count() else "")
  # receive on fresh context
  ctx2=b.new_context(viewport={"width":390,"height":844});p2=ctx2.new_page();p2.add_init_script("try{if(!localStorage.getItem('att-app-cheer'))localStorage.setItem('att-app-cheer',JSON.stringify({am:false,pm:false}))}catch(e){}");p2.on("pageerror",lambda e:errs.append(str(e)))
  p2.goto(url.replace("index.html","index.html"));p2.wait_for_timeout(800)
  print("sheet:",p2.inner_text("#sheetBox")[:400].replace("\n"," | "))
  p2.screenshot(path="__TL_WORK__/sh2.png")
  p2.click("#rcOk");p2.wait_for_timeout(300)
  st=json.loads(p2.evaluate("localStorage.getItem('att-app-v2')"))
  print("recv classes:",[(c["data"]["cls"],len(c["data"]["roster"]),len(c["data"]["phones"]),len(c["data"]["teachers"])) for c in st["list"]],"staff:",[(x["name"],x["phone"]) for x in st["staff"]])
  # receive again into same: no phones version -> keeps phones
  pg.check("#shStu");pg.uncheck("#shPh");pg.check("#shTc");pg.click("#mkLink");pg.wait_for_timeout(300);url2=pg.inner_text("#linkOut")
  p2.goto(url2);p2.wait_for_timeout(800);print("sheet2:",p2.inner_text("#sheetBox")[:300].replace("\n"," | "));p2.click("#rcOk");p2.wait_for_timeout(300)
  st=json.loads(p2.evaluate("localStorage.getItem('att-app-v2')"))
  print("recv2:",[(c["data"]["cls"],len(c["data"]["roster"]),len(c["data"]["phones"]),len(c["data"]["teachers"])) for c in st["list"]],len(st["staff"]))
  b.close()
print("errors:",errs)
