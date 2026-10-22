import datetime
src=open('t60.py').read();exec(src.split("with sync_playwright() as p:")[0])
TD=datetime.date.today().isoformat()
S["tt"]={"list":[{"id":"t1","year":2026,"term":"2학기","start":"09:00","classMin":50,"breakMin":10,"lunchMin":60,"cells":{"0-1":{"subject":"물리","clsId":"c1","clsName":"","room":""}},"adj":{},"days":{},"chg":[]}],"active":"t1"}
def st(T):return json.loads(T.evaluate("localStorage.getItem('att-app-v2')"))
with sync_playwright() as p:
  b=p.chromium.launch();c=ctx(b,390);T=c.new_page();E=[];T.on("pageerror",lambda e:E.append(str(e)))
  T.goto("https://tl.test/index.html");T.evaluate("s=>{localStorage.clear();localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-view','tt');localStorage.setItem('att-app-lastver','9.9.9')}",json.dumps(S));T.reload();T.wait_for_timeout(500)
  T.click("#ttEditBtn");T.click("#preAdd");T.wait_for_timeout(200)
  T.click("#peName .chip:has-text('아침활동')");T.fill("#peS","08:20");T.fill("#peL","20");T.select_option("#peC","c1");T.click("#peOk");T.wait_for_timeout(200)
  T.evaluate("document.getElementById('ttSet').open=true");T.click("#ttPreAdd");T.click("#peName .chip:has-text('조례')");T.fill("#peS","08:40");T.fill("#peL","10");T.click("#peOk");T.wait_for_timeout(200)
  T.click("#ttEditBtn");T.wait_for_timeout(200)
  print("pre rows:",T.evaluate("[...document.querySelectorAll('tr.prer th')].map(x=>x.innerText.replace(/\\n/g,' '))"),"| list:",T.inner_text("#ttPreList").replace("\n"," / "))
  T.screenshot(path=SP+"/pre1.png")
  T.click(f"tr.prer .lc[data-date='{TD}']>>nth=0");T.wait_for_timeout(200);print("menu:",T.inner_text("#sheetBox")[:120].replace("\n"," | "))
  T.click("#pmEv");T.fill("#evTitle","아침 상담");T.click("#evOk");T.wait_for_timeout(200)
  T.click(f"tr.prer .lc[data-date='{TD}']>>nth=0");T.click("#pmAtt");T.wait_for_timeout(300)
  s=st(T);ses=s['list'][0]['data']['sessions'];print("session:",[(x['time'],x['label'],x.get('slot'),x.get('src')) for x in ses],"view att:",T.is_visible("#v-att"))
  print("ses chips:",T.inner_text("#sesSlots").replace("\n"," "))
  T.screenshot(path=SP+"/pre2.png")
  # move 아침활동 to 08:10
  T.click(".navb[data-v=tt]");T.click("tr.prer .tbtn.pre>>nth=0");T.fill("#peS","08:10");T.click("#peOk");T.wait_for_timeout(300)
  s=st(T);print("after move: ses",[x['time'] for x in s['list'][0]['data']['sessions']],"ev",[(e['title'],e['start'],e['end'],e.get('slot')) for e in s['events']])
  # cell attendance then change start time
  T.click(f"tr:not(.prer) .tc[data-d='0'][data-p='1']") if False else None
  T.evaluate("document.querySelector('.tc[data-d=\"0\"][data-p=\"1\"]').click()");T.wait_for_timeout(200);T.click("#cmAtt");T.wait_for_timeout(200)
  T.click(".navb[data-v=tt]");T.evaluate("document.getElementById('ttSet').open=true");T.fill("#ttStart","09:10");T.wait_for_timeout(900);T.click(".navb[data-v=att]");T.click(".navb[data-v=tt]");T.wait_for_timeout(300)
  s=st(T);print("after start change:",[(x['label'],x['time']) for x in s['list'][0]['data']['sessions']])
  # session chip select 조례
  T.click(".navb[data-v=att]");T.click(f"#tabs .tab>>nth=0");T.wait_for_timeout(100);T.evaluate("document.getElementById('sesInfo').open=true");T.click("#sesSlots [data-k^='x']>>nth=1");T.wait_for_timeout(200)
  s=st(T);print("chip pick:",[(x['label'],x['time'],x.get('slot')) for x in s['list'][0]['data']['sessions']])
  # obs lock
  T.click("#amode [data-m=obs]");T.click("#obsBar [data-k=a1]");T.click("#obsList [data-s='10101']");T.wait_for_timeout(200)
  T.click("#obsLockBtn");T.wait_for_timeout(100);print("lock txt:",T.inner_text("#obsLockTxt"))
  T.click("#obsBar [data-k=a2]");T.click("#obsList [data-s='10102']");T.wait_for_timeout(200);print("locked-click sheet:",T.inner_text("#sheetBox")[:80].replace("\n"," | "));T.click("#skNo")
  s=st(T);d=s['list'][0]['data'];print("obs:",[(r['sid'],r['tags']) for r in d['obs']],"lock:",list(d.get('obsLock',{}).keys()))
  T.click("#obsList [data-e='10101']");T.wait_for_timeout(200);print("sheet ro:",T.evaluate("document.getElementById('obMemo').readOnly"),T.is_hidden("#obOk"));T.click("#skNo")
  T.click("#obsLockBtn");T.wait_for_timeout(100);T.click("#obsBar [data-k=a2]");T.click("#obsList [data-s='10102']");T.wait_for_timeout(200)
  s=st(T);d=s['list'][0]['data'];print("after unlock:",[(r['sid'],r['tags']) for r in d['obs']],"lock:",d.get('obsLock'))
  T.screenshot(path=SP+"/pre3.png")
  b.close()
print(E)
