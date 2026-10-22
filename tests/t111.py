exec(open("t110.py").read().split("with sync_playwright() as p:")[0])
F=[]
def ok(c,m):print(("OK  " if c else "FAIL"),m);(None if c else F.append(m))
with sync_playwright() as p:
  b=p.chromium.launch();cx=b.new_context(viewport={"width":390,"height":900},service_workers="block");cx.route("**/*",handler);T=cx.new_page();E=[];T.on("pageerror",lambda e:E.append(str(e)))
  T.add_init_script(CLK);T.add_init_script("try{localStorage.setItem('att-app-cheer',JSON.stringify({am:false,pm:false}))}catch(e){}")
  T.goto("https://tl.test/index.html");T.evaluate("s=>{localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-lastver','9.9.9');localStorage.setItem('att-app-setup','1')}",json.dumps(X));T.reload();T.wait_for_timeout(800)
  T.click(".navb[data-v=todo]");T.wait_for_timeout(300);txt=T.inner_text("#tdToday .tdls")
  ok(txt.count("1학년 1반")==1 and "출석 1/8" in txt,"legacy manual check shows once, linked to 1교시: "+txt.replace("\n"," | ")[:120])
  T.click(".navb[data-v=tt]");T.wait_for_timeout(300);ok("1/8" in T.inner_text('.tc[data-d="0"][data-p="1"]'),"timetable cell shows its count")
  T.click('.tc[data-d="0"][data-p="1"]');T.wait_for_timeout(300)
  if T.is_visible("#cmAtt"):T.click("#cmAtt");T.wait_for_timeout(300)
  s=json.loads(T.evaluate("localStorage.getItem('att-app-v2')"))["list"][0]["data"]["sessions"]
  ok(len(s)==1 and s[0]["src"].endswith(":0:1") and s[0]["p"]=={"10101":True},"tapping the cell reuses that check (no duplicate), keeps marks")
  # new check from 출석 tab during 1교시 for class with existing linked -> plain new; for class c2 (no lesson now) -> plain
  T.evaluate("()=>{const S=JSON.parse(localStorage.getItem('att-app-v2'));S.list[0].data.sessions=[];localStorage.setItem('att-app-v2',JSON.stringify(S))}");T.reload();T.wait_for_timeout(700)
  T.click(".navb[data-v=att]");T.wait_for_timeout(200);T.evaluate("document.getElementById('sheet').hidden=true")
  T.evaluate("()=>{const b=document.getElementById('startSes');if(!b.closest('[hidden]'))b.click();else document.querySelector('#tabs .tab.add').click()}");T.wait_for_timeout(300)
  s=json.loads(T.evaluate("localStorage.getItem('att-app-v2')"))["list"][0]["data"]["sessions"]
  ok(len(s)==1 and s[0].get("src","").endswith(":0:1") and s[0]["label"].startswith("1교시") and s[0]["time"]=="09:00","＋ 체크 추가 during 1교시 auto-links: "+str({k:s[0].get(k) for k in ("time","label","src")}))
  T.click(".navb[data-v=todo]");T.wait_for_timeout(200);ok(T.inner_text("#tdToday .tdls").count("1학년 1반")==1,"today list single entry")
  print("errs",E);b.close()
print("fails",F)
