src=open('audit2.py').read();exec(src.split("sizes=")[0])
import copy
P='<img src=x onerror="window.__x=(window.__x||0)+1">'
Q='"><svg onload="window.__x=(window.__x||0)+1">'
X=copy.deepcopy(S)
c=X["list"][0]["data"];c["cls"]="1학년 1반"+P;c["roster"][0][1]="김가람"+P;c["roster"][1][1]="이나래"+Q;c["msg"]="문구"+P
c["teachers"][0]["name"]="김국어"+P;c["teachers"][0]["subject"]="국어"+Q
c["obs"]=[{"id":"o1","sid":c["roster"][0][0],"date":"2026-10-16","tags":{"a1":1},"memo":"메모"+P,"at":1}]
c["sts"]={c["roster"][0][0]:{"t":"세특"+P,"at":1}}
c["sessions"][0]["label"]="2교시"+P
X["staff"][0]["name"]="정교감"+P;X["staff"][0]["dept"]="교무부"+Q
t=X["tt"]["list"][0];t["cells"]["0-1"]["subject"]="물리"+P;t["cells"]["0-1"]["room"]="실험실"+Q
t["chg"][0]["reason"]="임시"+P;t.setdefault("acal",[])
X["tt"]["acal"]=[{"g":"ac1","from":"2026-10-22","to":"2026-10-22","title":"행사"+P,"kind":"event"}]
X["events"][0]["title"]="상담"+P;X["events"][0]["memo"]="메모"+Q;X["events"][0]["date"]="2026-10-22"
X["notes"]={f"{t['id']}:0:1:2026-10-19":{"progress":"진도"+P,"memo":"메모"+Q,"task":"과제"+P}}
X["evals"][0]["title"]="수행"+P;X["evals"][0]["cols"]=["과제"+P,"발표","보고서"];X["evals"][0]["stu"][0]["name"]="가람"+P;X["evals"][0]["note"]="안내"+Q
X["obsTags"]=None
js=json.dumps(X,ensure_ascii=False)
hits=[]
with sync_playwright() as p:
  b=p.chromium.launch()
  for W in (390,1440):
    cx=b.new_context(viewport={"width":W,"height":900},service_workers="block");cx.route("**/*",handler);T=cx.new_page();T.on("pageerror",lambda e:errs.append(str(e)))
    T.add_init_script("try{localStorage.setItem('att-app-cheer',JSON.stringify({am:false,pm:false}))}catch(e){}")
    T.goto("https://tl.test/index.html");T.evaluate("s=>{localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-lastver','9.9.9');localStorage.setItem('att-app-setup','1');localStorage.setItem('att-app-me','김물리<img src=x onerror=window.__x=1>')}",js);T.reload();T.wait_for_timeout(900)
    def chk(where):
      v=T.evaluate("window.__x||0")
      if v:hits.append((W,where,v));T.evaluate("window.__x=0")
    for v in ["tt","att","call","todo","stat","set"]:
      T.evaluate(f"()=>{{document.getElementById('sheet').hidden=true;document.querySelector('.navb[data-v={v}]').click();document.querySelectorAll('main.view:not([hidden]) details').forEach(d=>{{d.open=true;d.dispatchEvent(new Event('toggle'))}})}}");T.wait_for_timeout(400);chk("view "+v)
    # sheets: student sheet, event editor, eval detail, cell menu, obs tab, call tabs, stat tabs
    steps=["document.querySelector('.navb[data-v=att]').click();document.querySelector('#amode [data-m=obs]').click()",
      "document.querySelector('#obsList [data-e]')&&document.querySelector('#obsList [data-e]').click()",
      "document.getElementById('sheet').hidden=true;document.querySelector('.navb[data-v=att]').click();document.querySelector('#amode [data-m=att]').click();document.querySelector('[data-av=list]')&&document.querySelector('[data-av=list]').click()",
      "document.querySelector('.navb[data-v=tt]').click();document.querySelector('.tc[data-d=\"0\"][data-p=\"1\"]').click()",
      "document.getElementById('sheet').hidden=true;document.querySelector('.navb[data-v=todo]').click();document.querySelector('#tdList .tdb')&&document.querySelector('#tdList .tdb').click()",
      "document.getElementById('sheet').hidden=true;document.querySelector('.navb[data-v=stat]').click();const e=document.querySelector('#stabs .chip[data-t=eval]');e&&e.click();const d=document.querySelector('[data-ev]');d&&d.click()",
      "document.getElementById('sheet').hidden=true;document.querySelector('.navb[data-v=call]').click();document.querySelectorAll('#v-call .chip').forEach(c=>c.click())",
      "document.getElementById('sheet').hidden=true;document.querySelector('.navb[data-v=stat]').click();const a=document.querySelector('#stabs .chip[data-t=att]');a&&a.click()",
      "document.getElementById('sheet').hidden=true;document.querySelector('.navb[data-v=set]').click();const s=document.getElementById('d-share');s.open=true;s.dispatchEvent(new Event('toggle'))"]
    for i,sjs in enumerate(steps):
      try:T.evaluate("()=>{"+sjs+"}");T.wait_for_timeout(400);chk("step %d"%i)
      except Exception as e:print("step err",i,str(e)[:100])
    # student overview sheet (name click in obs list)
    try:
      T.evaluate("()=>{document.getElementById('sheet').hidden=true;document.querySelector('.navb[data-v=att]').click();document.querySelector('#amode [data-m=obs]').click()}");T.wait_for_timeout(200)
      T.evaluate("()=>{const n=document.querySelector('#obsList .onm, #obsList [data-s]');n&&n.click()}");T.wait_for_timeout(400);chk("student sheet")
    except Exception as e:print("stu err",str(e)[:80])
    cx.close()
  b.close()
print("SCRIPT RAN:",hits);print("errs",errs[:5])
