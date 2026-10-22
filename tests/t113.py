src=open('audit2.py').read();exec(src.split("sizes=")[0])
import copy
X=copy.deepcopy(S)
td="2026-10-22"
X["events"]=[{"id":"e1","date":td,"start":"10:00","end":"","cat":"업무","title":"오늘 회의","memo":"","alarm":-1,"important":False,"done":False},
 {"id":"e2","date":td,"start":"13:00","end":"","cat":"업무","title":"오늘 상담","memo":"","alarm":-1,"important":True,"done":False},
 {"id":"e3","date":"2026-10-15","start":"09:00","end":"","cat":"업무","title":"지난 보고서","memo":"","alarm":-1,"important":False,"done":False},
 {"id":"e4","date":"2026-10-28","start":"09:00","end":"","cat":"업무","title":"다음 주 협의","memo":"","alarm":-1,"important":False,"done":False}]
X["list"][0]["data"]["teachers"].append({"id":"t2","subject":"수학","name":"이수학","phone":"010-3333-4444"})
CLK="(()=>{const fixed=new Date('2026-10-22T09:20:00+09:00').getTime();const D=Date;const off=fixed-D.now();class FD extends D{constructor(...a){if(!a.length)super(D.now()+off);else super(...a)}static now(){return D.now()+off}};window.Date=FD})()"
F=[]
def ok(c,m):print(("OK  " if c else "FAIL"),m);(None if c else F.append(m))
def st(T):return json.loads(T.evaluate("localStorage.getItem('att-app-v2')"))
with sync_playwright() as p:
  b=p.chromium.launch();c=b.new_context(viewport={"width":390,"height":844},has_touch=True,is_mobile=True,device_scale_factor=2,service_workers="block");c.route("**/*",handler);T=c.new_page();T.on("pageerror",lambda e:errs.append(str(e)))
  T.add_init_script(CLK);T.add_init_script("try{localStorage.setItem('att-app-cheer',JSON.stringify({am:false,pm:false}))}catch(e){}")
  T.goto("https://tl.test/index.html");T.evaluate("s=>{localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-lastver','9.9.9');localStorage.setItem('att-app-setup','1');localStorage.setItem('att-app-todo',JSON.stringify({range:'all'}))}",json.dumps(X));T.reload();T.wait_for_timeout(900)
  cdp=c.new_cdp_session(T)
  def touch(sel,dx,dy=0,steps=8,nth=0):
    T.locator(sel).nth(nth).evaluate("e=>e.scrollIntoView({block:'center'})");T.wait_for_timeout(150)
    bb=T.locator(sel).nth(nth).bounding_box();x=bb["x"]+bb["width"]*0.7;y=bb["y"]+bb["height"]/2
    cdp.send("Input.dispatchTouchEvent",{"type":"touchStart","touchPoints":[{"x":x,"y":y}]})
    for i in range(1,steps+1):cdp.send("Input.dispatchTouchEvent",{"type":"touchMove","touchPoints":[{"x":x+dx*i/steps,"y":y+dy*i/steps}]});T.wait_for_timeout(16)
    cdp.send("Input.dispatchTouchEvent",{"type":"touchEnd","touchPoints":[]});T.wait_for_timeout(300)
  def tapdel():
    bb=T.locator(".swdel").bounding_box();T.touchscreen.tap(bb["x"]+bb["width"]/2,bb["y"]+bb["height"]/2);T.wait_for_timeout(500)
  # --- KPI sheets
  T.click(".navb[data-v=todo]");T.wait_for_timeout(300)
  T.click("[data-kpi=today]");T.wait_for_timeout(250);ok("오늘 할 일" in T.inner_text("#sheetBox h2") and T.locator(".kpir").count()==2,"오늘 할 일 칸 -> 2개 목록: "+T.inner_text("#sheetBox h2"))
  T.click("#skNo");T.click("[data-kpi=over]");T.wait_for_timeout(250);ok(T.locator(".kpir").count()==1 and "지난 보고서" in T.inner_text(".kpil"),"지난 미완료 칸 -> 1개")
  T.click(".kpir .tdc");T.wait_for_timeout(250);ok(T.locator(".kpir").count()==0 and [e for e in st(T)["events"] if e["id"]=="e3"][0]["done"],"check in sheet marks done")
  T.click("#skNo");T.click("[data-kpi=open]");T.wait_for_timeout(250);n_open=T.locator(".kpir").count();ok(n_open==3,"남은 할 일 칸 -> 3개 (%d)"%n_open)
  T.click(".kpir .tdb >> nth=0");T.wait_for_timeout(250);ok(T.is_visible("#evTitle") or "일정" in T.inner_text("#sheetBox"),"tap row opens editor");T.evaluate("document.getElementById('sheet').hidden=true")
  # swipe inside KPI sheet
  T.click("[data-kpi=open]");T.wait_for_timeout(250)
  touch(".kpir",-150);ok(T.is_visible(".swdel"),"swipe in sheet shows delete button");tapdel()
  ok(len(st(T)["events"])==3 and T.locator(".kpir").count()==2,"deleted from sheet")
  T.click("#utoast button");T.wait_for_timeout(300);ok(len(st(T)["events"])==4,"undo restores")
  T.evaluate("document.getElementById('sheet').hidden=true")
  # --- swipe on 오늘 list rows; vertical drag must not open
  T.evaluate("document.querySelector('#tdRange .chip[data-r=all]').click()");T.wait_for_timeout(200)
  touch("#tdList .td",-15,120);ok(not T.is_visible(".swdel") and not T.evaluate("!!document.querySelector('.swopen')"),"vertical drag does not open delete")
  touch("#tdList .td",-30);ok(not T.evaluate("!!document.querySelector('.swopen')"),"short swipe snaps back")
  n0=len(st(T)["events"]);touch("#tdList .td",-140);ok(T.evaluate("!!document.querySelector('#tdList .swopen')"),"swipe opens row")
  T.wait_for_timeout(300);bb=T.locator("#tdList .td.swopen .tdb").bounding_box();T.touchscreen.tap(bb["x"]+20,bb["y"]+10);T.wait_for_timeout(300)
  ok(not T.evaluate("!!document.querySelector('.swopen')") and T.evaluate("document.getElementById('sheet').hidden"),"tapping open row just closes it (no editor)")
  touch("#tdList .td",-140);tapdel();ok(len(st(T)["events"])==n0-1,"swipe delete on 오늘 list")
  T.click("#utoast button");T.wait_for_timeout(300);ok(len(st(T)["events"])==n0,"undo")
  # --- timetable agenda + day sheet
  T.click(".navb[data-v=tt]");T.wait_for_timeout(300)
  if T.locator("#agList .ev").count():
    n0=len(st(T)["events"]);touch("#agList .ev",-140);tapdel();ok(len(st(T)["events"])==n0-1,"agenda event swipe delete");T.click("#utoast button");T.wait_for_timeout(200)
  T.evaluate("document.querySelector('.dbtn[data-date=\"2026-10-22\"]').click()");T.wait_for_timeout(300)
  n0=len(st(T)["events"]);touch("#sheetBox .ev",-140);ok(T.is_visible(".swdel"),"delete button shows above the sheet");tapdel();ok(len(st(T)["events"])==n0-1 and T.locator("#sheetBox .ev").count()==1,"day sheet event swipe delete")
  T.click("#utoast button");T.wait_for_timeout(200);T.evaluate("document.getElementById('sheet').hidden=true")
  # change list
  T.evaluate("()=>{const d=document.getElementById('ttChg');d.open=true}");T.wait_for_timeout(200)
  n0=len(st(T)["tt"]["list"][0]["chg"]);touch("#ttChgList .prow",-140);tapdel();ok(len(st(T)["tt"]["list"][0]["chg"])==n0-1,"수업 변동 swipe delete");T.click("#utoast button");T.wait_for_timeout(200);ok(len(st(T)["tt"]["list"][0]["chg"])==n0,"undo change")
  # settings: students / teachers / staff
  T.click(".navb[data-v=set]");T.evaluate("()=>{['d-stu','d-tc','d-staff'].forEach(i=>{const d=document.getElementById(i);d.open=true;d.dispatchEvent(new Event('toggle'))})}");T.wait_for_timeout(300)
  r0=st(T)["list"][0]["data"];n0=len(r0["roster"]);first=r0["roster"][0][0];ph=r0["phones"].get(first)
  touch("#stuList .prow",-140);tapdel();r1=st(T)["list"][0]["data"];ok(len(r1["roster"])==n0-1 and first not in r1["phones"],"student swipe delete (phone removed too)")
  T.click("#utoast button");T.wait_for_timeout(300);r2=st(T)["list"][0]["data"];ok(len(r2["roster"])==n0 and r2["roster"][0][0]==first and r2["phones"].get(first)==ph,"undo restores student at same place with phone")
  n0=len(st(T)["list"][0]["data"]["teachers"]);touch("#tcEdit .prow",-140);tapdel();ok(len(st(T)["list"][0]["data"]["teachers"])==n0-1,"teacher swipe delete");T.click("#utoast button");T.wait_for_timeout(200)
  n0=len(st(T)["staff"]);touch("#staffEdit .prow",-140);tapdel();ok(len(st(T)["staff"])==n0-1,"staff swipe delete");T.click("#utoast button");T.wait_for_timeout(200);ok(len(st(T)["staff"])==n0,"undo staff")
  # eval list
  T.click(".navb[data-v=stat]");T.evaluate("()=>{const e=document.querySelector('#stabs .chip[data-t=eval]');e&&e.click()}");T.wait_for_timeout(300)
  n0=len(st(T)["evals"]);touch("#evList .prow[data-ev]" if T.locator("#evList .prow[data-ev]").count() else ".prow[data-ev]",-140);tapdel();ok(len(st(T)["evals"])==n0-1,"evaluation swipe delete");T.click("#utoast button");T.wait_for_timeout(300);ok(len(st(T)["evals"])==n0,"undo evaluation")
  # plain tap on a row still works normally
  T.click(".navb[data-v=set]");T.wait_for_timeout(200);T.locator("#staffEdit .prow").first.evaluate("e=>e.scrollIntoView({block:'center'})");T.wait_for_timeout(200);bb=T.locator("#staffEdit .prow").first.bounding_box();T.touchscreen.tap(bb["x"]+40,bb["y"]+bb["height"]/2);T.wait_for_timeout(300);ok(not T.evaluate("document.getElementById('sheet').hidden"),"normal tap still opens editor")
  T.screenshot(path="shot/sw_last.png")
  b.close()
print("fails",F);print(errs)
