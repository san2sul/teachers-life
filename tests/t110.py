src=open('audit2.py').read();exec(src.split("sizes=")[0])
import copy
X=copy.deepcopy(S);X["tt"]["list"][0]["chg"]=[]
# Monday 10/19 1교시 = c1. A teacher started a check from the 출석 tab (＋ 체크 추가) instead of tapping the timetable cell
X["list"][0]["data"]["sessions"]=[{"id":"m1","date":"2026-10-19","time":"09:03","label":"","p":{"10101":True}}]
CLK="(()=>{const fixed=new Date('2026-10-19T09:20:00+09:00').getTime();const D=Date;const off=fixed-D.now();class FD extends D{constructor(...a){if(!a.length)super(D.now()+off);else super(...a)}static now(){return D.now()+off}};window.Date=FD})()"
with sync_playwright() as p:
  b=p.chromium.launch();cx=b.new_context(viewport={"width":390,"height":900},service_workers="block");cx.route("**/*",handler);T=cx.new_page()
  T.add_init_script(CLK);T.add_init_script("try{localStorage.setItem('att-app-cheer',JSON.stringify({am:false,pm:false}))}catch(e){}")
  T.goto("https://tl.test/index.html");T.evaluate("s=>{localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-lastver','9.9.9');localStorage.setItem('att-app-setup','1')}",json.dumps(X));T.reload();T.wait_for_timeout(800)
  T.click(".navb[data-v=todo]");T.wait_for_timeout(300)
  print("오늘 수업:",T.inner_text("#tdToday .tdls").replace("\n"," | ")[:300])
  T.click(".navb[data-v=tt]");T.wait_for_timeout(300);print("timetable cell:",T.inner_text('.tc[data-d="0"][data-p="1"]').replace("\n"," "))
  T.click('.tc[data-d="0"][data-p="1"]');T.wait_for_timeout(300);print("after tapping cell, sessions:",len(json.loads(T.evaluate("localStorage.getItem('att-app-v2')"))["list"][0]["data"]["sessions"]))
  T.click(".navb[data-v=att]");T.wait_for_timeout(200);print("att tabs:",T.inner_text("#tabs").replace("\n"," | "))
  b.close()
