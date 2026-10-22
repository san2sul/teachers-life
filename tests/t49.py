import json
from playwright.sync_api import sync_playwright
S={"active":"c1","list":[{"id":"c1","data":{"v":3,"cls":"1학년 1반","roster":[["10101","김가"],["10102","이나"],["10103","박다"],["10104","최라"]],"phones":{"10101":"010-1111-2222","10102":"010-3333-4444","10103":"010-5555-1111"},"teachers":[],"msg":"{이름} 학생 결석","sessions":[{"id":"s1","date":__import__("datetime").date.today().isoformat(),"time":"09:00","label":"","p":{"10101":True}}]}}],"staff":[],"tt":{"list":[],"active":""},"notes":{},"events":[]}
errs=[]
with sync_playwright() as p:
  b=p.chromium.launch();c=b.new_context(viewport={"width":390,"height":844});pg=c.new_page();pg.add_init_script("try{if(!localStorage.getItem('att-app-cheer'))localStorage.setItem('att-app-cheer',JSON.stringify({am:false,pm:false}))}catch(e){}");pg.on("pageerror",lambda e:errs.append(str(e)))
  pg.goto("http://localhost:8766/index.html");pg.evaluate("s=>{localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-view','call')}",json.dumps(S));pg.reload();pg.wait_for_timeout(400)
  print("badge",pg.inner_text("#navCnt"),"|",pg.inner_text("#abCount"))
  pg.locator("#abList .crow").nth(0).locator("[data-a=done]").click();pg.wait_for_timeout(200)
  print("badge",pg.inner_text("#navCnt"),"|",pg.inner_text("#abCount"),"|",pg.inner_text("#bulk .note"))
  st=json.loads(pg.evaluate("localStorage.getItem('att-app-v2')"));ses=st["list"][0]["data"]["sessions"][0];print("p",ses["p"],"done",list(ses.get("done",{})))
  pg.screenshot(path="__TL_WORK__/dn1.png",full_page=True)
  pg.click("#doneAll");pg.click("#doneAll");pg.wait_for_timeout(200)
  print("badge hidden",pg.get_attribute("#navCnt","hidden"),"|",pg.inner_text("#abList"),"|",pg.inner_text("#abDoneCnt"))
  pg.locator("#abDone .crow").nth(0).locator("[data-a=done]").click();pg.wait_for_timeout(200)
  print("badge",pg.inner_text("#navCnt"))
  pg.reload();pg.wait_for_timeout(300);print("after reload",pg.inner_text("#abCount"))
  pg.click(".navb[data-v=att]");pg.wait_for_timeout(200);print("att tags",pg.locator(".dtag").count())
  b.close()
print(errs)
