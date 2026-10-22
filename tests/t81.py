src=open('t60.py').read();exec(src.split("with sync_playwright() as p:")[0])
NEWV={"v":None}
def h2(route,req):
  if "manifest.webmanifest" in req.url and NEWV["v"]:
    m=json.load(open(APP+"/manifest.webmanifest"));m["version"]=NEWV["v"];return route.fulfill(json=m)
  return handler(route,req)
with sync_playwright() as p:
  b=p.chromium.launch();c=ctx(b,390);c.unroute("**/*");c.route("**/*",h2);T=c.new_page();E=[];T.on("pageerror",lambda e:E.append(str(e)))
  T.goto("https://tl.test/index.html");T.evaluate("s=>{localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-lastver','9.9.9');localStorage.setItem('att-app-view','set')}",json.dumps(S));T.reload();T.wait_for_timeout(3200)
  print("bar same ver:",T.evaluate("[...document.querySelectorAll('.newbar')].map(b=>b.innerText)"))
  T.evaluate("document.getElementById('updChk').click()");T.wait_for_timeout(600);print("manual:",T.inner_text("#updMsg"))
  NEWV["v"]="9.0.0";T.reload();T.wait_for_timeout(3200)
  print("bar new:",T.evaluate("[...document.querySelectorAll('.newbar')].map(b=>b.innerText.replace(/\\n/g,' '))"))
  T.click(".newbar .go");T.wait_for_timeout(1500);print("url after:",T.url,"data kept:",bool(T.evaluate("localStorage.getItem('att-app-v2')")))
  b.close()
print(E)
