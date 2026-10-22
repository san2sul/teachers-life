src=open('audit2.py').read();exec(src.split("sizes=")[0])
import datetime
td=datetime.date.today();T0=td.isoformat();wd=td.weekday()
tt=S["tt"]["list"][0];tt["chg"]=[];tt["start"]="09:00";tt["classMin"]=45;tt["breakMin"]=10;tt["lunchMin"]=60;tt["pre"]=[]
nxt=(td+datetime.timedelta(days=(7-wd)%7 or 7)).isoformat()  # next monday... 
with sync_playwright() as p:
  b=p.chromium.launch();c=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,service_workers="block");c.route("**/*",handler);T=c.new_page();T.on("pageerror",lambda e:errs.append(str(e)))
  T.goto("https://tl.test/index.html");T.evaluate("s=>{localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-lastver','9.9.9');localStorage.setItem('att-app-me','김물리');localStorage.setItem('att-app-setup','1')}",json.dumps(S));T.reload();T.wait_for_timeout(500)
  T.click(".navb[data-v=tt]");T.wait_for_timeout(200)
  print("generic pre row:",T.is_visible("tr.prer.gen"))
  T.click(f"tr.prer.gen .lc[data-date='{T0}']");T.wait_for_timeout(150);print("menu:",T.inner_text("#sheetBox h2"))
  T.click("#actQ [data-n='정문지도']");T.check("#actAll");T.click("#actOk");T.wait_for_timeout(150)
  print("pre row:",T.inner_text("tr.prer.gen").replace("\n"," "))
  T.click(f"tr.lunch .lc[data-date='{T0}']");T.fill("#actN","점심 상담");T.select_option("#actC","학생 면담");T.click("#actOk");T.wait_for_timeout(150)
  T.wait_for_timeout(100)
  # event via agenda: today 12:40 normal; today 16:40 weekly after
  T.click("#agAdd");T.fill("#evTitle","학부모 통화");T.fill("#evDate",T0);T.fill("#evStart","12:40");T.wait_for_timeout(100);print("weekly offered(lunch):",T.is_visible("#evWkL"),T.inner_text("#evWkT") if T.is_visible("#evWkL") else "");T.click("#evOk");T.wait_for_timeout(150)
  T.click("#agAdd");T.fill("#evTitle","교과협의회");T.click("#evCats [data-c='부서 업무']");T.fill("#evDate",T0);T.fill("#evStart","16:50");T.wait_for_timeout(100);T.check("#evWk");T.click("#evOk");T.wait_for_timeout(200)
  print("toast:",T.evaluate("(document.querySelector('.toast')||{}).textContent"))
  print("lunch row:",T.inner_text("tr.lunch").replace("\n"," "))
  print("after row:",T.inner_text("tr.after").replace("\n"," "))
  st=T.evaluate("JSON.parse(localStorage.getItem('att-app-v2'))");print("acts:",st['tt']['list'][0].get('acts'))
  print("events:",[(e['date'],e['start'],e['title']) for e in st['events'] if e['date']==T0])
  T.screenshot(path=SP+"/shot/gap_tt.png",full_page=True)
  T.click(".navb[data-v=todo]");T.wait_for_timeout(150);print("TODAY:",T.inner_text("#tdToday").replace("\n"," | ")[:400]);T.screenshot(path=SP+"/shot/gap_today.png")
  # no-school day hides acts
  T.evaluate("t=>0",None)
  st['tt']['list'][0]['chg']=[{"id":"x1","scope":"day","d":0,"p":1,"from":T0,"to":T0,"type":"cancel","reason":"재량휴업","created":1}]
  T.evaluate("s=>{localStorage.setItem('att-app-v2',s)}",json.dumps(st));T.reload();T.wait_for_timeout(400);T.click(".navb[data-v=tt]")
  print('errbar:',T.evaluate("(()=>{const e=document.getElementById('errBar');return e&&!e.hidden?e.innerText:''})()"),'tt hidden:',T.evaluate("document.getElementById('v-tt').hidden"),errs[:2]);
  T.wait_for_timeout(300);print('rows:',T.evaluate("[...document.querySelectorAll('#ttGrid tr')].map(r=>r.className).join(',')"),'week:',T.inner_text('#ttWeekTxt'));print('holiday pre cell:',T.evaluate("(document.querySelector('tr.prer.gen .lc[data-date=\""+T0+"\"]')||{}).innerText"))
  # pre-slot timetable: preMenu act section
  st['tt']['list'][0]['chg']=[];st['tt']['list'][0]['pre']=[{"id":"p1","name":"조례","start":"08:30","len":10,"clsId":""}]
  T.evaluate("s=>{localStorage.setItem('att-app-v2',s)}",json.dumps(st));T.reload();T.wait_for_timeout(400);T.click(".navb[data-v=tt]")
  T.click(f"tr.prer .lc[data-date='{T0}']");T.wait_for_timeout(150);print("preMenu act sec:",T.is_visible("#actQ"));T.click("#actQ [data-n='조례']");T.click("#actOk");T.wait_for_timeout(150)
  print("pre slot row:",T.inner_text("tr.prer").replace("\n"," "))
  b.close()
print(errs)
