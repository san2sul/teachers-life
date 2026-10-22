src=open('audit2.py').read();exec(src.split("sizes=")[0])
import sys
dark=len(sys.argv)>1
with sync_playwright() as p:
  b=p.chromium.launch();c=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,service_workers="block",color_scheme="dark" if dark else "light");c.route("**/*",handler);T=c.new_page();T.on("pageerror",lambda e:errs.append(str(e)))
  T.goto("https://tl.test/index.html");T.wait_for_timeout(900)
  sh=lambda n:T.screenshot(path=f"{SP}/shot/wiz{'d' if dark else ''}_{n}.png")
  print("wizard shown:",T.is_visible(".wizw"));sh(0)
  T.click("#wzN");T.fill("#wzMe","김물리");sh(1);T.click("#wzN")
  sh(2);T.click("#wzY .chip[data-y='2026']");T.click("#wzT .chip[data-t='2학기']");T.click("#wzN")
  T.fill("#wzCls","1학년 3반");T.fill("#wzRos","1 김가람\n2번 이나래 010-1234-5678\n박다솜");T.wait_for_timeout(100);print("msg:",T.inner_text("#wzMsg"));sh(3)
  T.click("#wzSave");T.wait_for_timeout(200);print("after save chips:",T.inner_text(".wizcls"))
  T.fill("#wzCls","2학년 5반");T.fill("#wzRos","20501 최라온\n20502 정마루");T.click("#wzN");T.wait_for_timeout(200);sh(4)
  st=T.evaluate("JSON.parse(localStorage.getItem('att-app-v2'))")
  print("classes:",[(x['data']['cls'],x['data'].get('year'),x['data'].get('term'),[r[0] for r in x['data']['roster']],x['data']['phones']) for x in st['list']],"period",st.get('period'),"me",T.evaluate("localStorage.getItem('att-app-me')"))
  T.set_input_files("#wzTtIn",SP+"/ttimg/cap_nolines.png");T.wait_for_timeout(500)
  for i in range(60):
    if T.is_visible("text=올린 시간표 확인"):break
    T.wait_for_timeout(1000)
  print("review open:",T.is_visible("text=올린 시간표 확인"),"tt visible:",T.evaluate("!document.getElementById('v-tt').hidden"))
  print("setup flag:",bool(T.evaluate("localStorage.getItem('att-app-setup')")))
  T.reload();T.wait_for_timeout(600);print("wizard again after reload:",T.is_visible(".wizw"))
  T.evaluate("document.querySelector('.navb[data-v=set]').click()");T.click("#wizOpen");T.wait_for_timeout(200);print("reopen:",T.is_visible(".wizw"))
  T.click("#wzN");T.click("#wzN");T.click("#wzN");T.wait_for_timeout(100);sh("3b");T.click("#wzN");T.click("#wzN");T.wait_for_timeout(100);sh(5);print("done:",T.inner_text(".wizsum").replace("\n"," | "))
  b.close()
print(errs)
