src=open('t60.py').read();pre=src.split("with sync_playwright() as p:")[0]
pre=pre.replace("requestAccessToken:function(o){window.__lastReq=o;","requestAccessToken:function(o){window.__lastReq=o;window.__act=navigator.userActivation.isActive;")
exec(pre)
import json
Gst={"clientId":"123-test.apps.googleusercontent.com","on":True,"email":"t@gmail.com","name":"물리","token":"old","exp":1,"auto":True,"accts":[{"email":"t@gmail.com"}]}
def run(block):
  with sync_playwright() as p:
    b=p.chromium.launch();c=ctx(b,390)
    if block:c.route("**/gsi/client*",lambda r:r.abort())
    T=c.new_page();T.on("pageerror",lambda e:errs.append(str(e)))
    T.goto("https://tl.test/index.html");T.evaluate("([s,g])=>{localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-gsync',g);localStorage.setItem('att-app-lastver','9.9.9');localStorage.setItem('att-app-view','set')}",[json.dumps(S),json.dumps(Gst)]);T.reload();T.wait_for_timeout(1200)
    print("block" if block else "normal","| pill:",T.inner_text("#gsPill"),"| btn:",T.inner_text("#gsNow"))
    T.evaluate("document.querySelectorAll('#v-set details').forEach(d=>d.open=true)") or T.click("#gsNow");T.wait_for_timeout(800)
    print("  act:",T.evaluate("window.__act"),"| tag:",T.inner_text("#gsTag"),"| body:",T.inner_text("#gsBody")[:160].replace("\n"," / "))
    if block:
      T.evaluate("document.querySelectorAll('#v-set details').forEach(d=>d.open=true)") or T.click("#gsd") if False else None
      T.evaluate("document.querySelector('.gsfix').open=true");T.evaluate("document.querySelectorAll('#v-set details').forEach(d=>d.open=true)") or T.click("#gsReset");T.wait_for_timeout(300);print("  after reset:",T.inner_text("#gsNow"))
    else:
      print("  token ok:",T.evaluate("JSON.parse(localStorage.getItem('att-app-gsync')).token.startsWith('tok')"),"pill:",T.inner_text("#gsPill"))
    b.close()
run(False);run(True);print(errs)
