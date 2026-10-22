import sys,datetime,copy
src=open('t60.py').read();exec(src.split("with sync_playwright() as p:")[0])
APPF=sys.argv[1] if len(sys.argv)>1 else None
d=copy.deepcopy(S);d["list"][0]["data"]["sessions"]=[{"id":"s1","date":datetime.date.today().isoformat(),"time":"09:00","label":"","p":{"10101":True},"lock":True,"lockAt":1760000000000}]
def h2(route,req):
  if APPF and req.url.endswith("/index.html"):return route.fulfill(path=APPF,content_type="text/html")
  return handler(route,req)
with sync_playwright() as p:
  b=p.chromium.launch()
  for view in ["att","set"]:
    c=b.new_context(viewport={"width":390,"height":844},service_workers="block");c.route("**/*",h2)
    T=c.new_page();E=[];T.on("pageerror",lambda e:E.append(str(e)))
    T.goto("https://tl.test/index.html");T.evaluate("([s,v])=>{localStorage.clear();localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-view',v)}",[json.dumps(d),view]);T.reload();T.wait_for_timeout(800)
    T.evaluate("document.querySelector('.navb[data-v=set]').click()");T.wait_for_timeout(300)
    print(view,"perY:",T.evaluate("document.getElementById('perY').options.length"),"gs:",T.evaluate("document.getElementById('gsBody').textContent.length"),"errbar:",T.evaluate("!!document.getElementById('errBar')&&!document.getElementById('errBar').hidden"),E[:2])
    c.close()
  b.close()
