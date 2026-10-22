src=open('audit2.py').read();exec(src.split("sizes=")[0])
cases={
 "empty":"",
 "not json":"안녕하세요 이건 백업이 아닙니다",
 "truncated":json.dumps({"v":3,"classes":[{"cls":"1반","roster":[["1","가"]]}]})[:40],
 "null classes":json.dumps({"v":3,"app":"교사의 생활","classes":None}),
 "wrong types":json.dumps({"v":3,"app":"교사의 생활","appVersion":"5.20.0","classes":[{"cls":123,"roster":"가,나","sessions":{"a":1},"phones":[],"obs":"x"}],"staff":"x","tt":{"list":"x"},"events":{"a":1},"evals":[None,1,"x"],"notes":[]}),
 "weird sessions":json.dumps({"v":3,"app":"교사의 생활","appVersion":"5.20.0","classes":[{"cls":"1반","roster":[["1","가"],[None,None],["2"]],"sessions":[{"date":"오늘","p":[1,2]},None,{"id":"s","date":"2026-10-01","p":{"1":True}}]}]}),
 "future version":json.dumps({"v":9,"app":"교사의 생활","appVersion":"9.0.0","classes":[{"cls":"1반","roster":[["1","가"]]}]}),
 "huge name":json.dumps({"v":3,"app":"교사의 생활","appVersion":"5.20.0","classes":[{"cls":"가"*5000,"roster":[["1","나"*3000]]}]}),
 "archive broken":json.dumps({"kind":"teachers-life-archive","year":"abc","classes":"x"}),
 "share broken":json.dumps({"kind":"share","v":3,"classes":None}),
}
res=[]
with sync_playwright() as p:
  b=p.chromium.launch()
  for name,txt in cases.items():
    cx=b.new_context(viewport={"width":390,"height":900},service_workers="block");cx.route("**/*",handler);T=cx.new_page();E=[];T.on("pageerror",lambda e:E.append(str(e)[:100]))
    T.add_init_script("try{localStorage.setItem('att-app-cheer',JSON.stringify({am:false,pm:false}))}catch(e){}")
    T.goto("https://tl.test/index.html");T.evaluate("s=>{localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-lastver','9.9.9');localStorage.setItem('att-app-setup','1')}",json.dumps(S));T.reload();T.wait_for_timeout(600)
    before=T.evaluate("localStorage.getItem('att-app-v2').length")
    T.evaluate("t=>{const f=new File([t],'x.json',{type:'application/json'});const dt=new DataTransfer();dt.items.add(f);const i=document.getElementById('restoreFile');i.files=dt.files;i.dispatchEvent(new Event('change'))}",txt);T.wait_for_timeout(700)
    sheet=T.inner_text("#sheetBox")[:70].replace("\n"," ") if T.is_visible("#sheetBox") else ""
    toast=T.evaluate("(document.querySelector('.toast')||{}).textContent||''")[:70]
    # if a confirm sheet appears, try merge
    merged=""
    if T.is_visible("#sheetBox .btn.pri"):
      T.click("#sheetBox .btn.pri");T.wait_for_timeout(600);merged="applied"
    for v in ["att","tt","todo","stat","set"]:T.evaluate(f"()=>{{document.getElementById('sheet').hidden=true;document.querySelector('.navb[data-v={v}]').click()}}");T.wait_for_timeout(150)
    alive=T.evaluate("!!document.querySelector('.navb') && document.querySelectorAll('main.view:not([hidden])').length===1")
    after=T.evaluate("localStorage.getItem('att-app-v2').length")
    res.append((name,alive,E[:2],sheet or toast,merged,before,after))
    cx.close()
  b.close()
for r in res:print(r)
