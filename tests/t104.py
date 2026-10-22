from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  b=p.chromium.launch();c=b.new_context();T=c.new_page();srv=[]
  T.on("request",lambda r:"mp3" in r.url and srv.append((r.headers.get("range"),r.is_navigation_request())))
  T.goto("http://localhost:8766/sign.html");T.evaluate("navigator.serviceWorker.register('sw.js').then(()=>navigator.serviceWorker.ready)");T.reload();T.wait_for_timeout(1000)
  print("controlled:",T.evaluate("!!navigator.serviceWorker.controller"))
  q="""async r=>{const x=await fetch('sounds/morning.mp3?v=1',{cache:'reload',headers:r?{Range:r}:{}});const bl=await x.blob();return [x.status,bl.size,x.headers.get('content-range')]}"""
  print("range first (not cached yet):",T.evaluate(q,"bytes=0-99"))
  print("range again:",T.evaluate(q,"bytes=5000-5999"),"full:",T.evaluate(q,None))
  c.set_offline(True)
  print("offline range:",T.evaluate(q,"bytes=1000-1999"))
  T.reload();T.wait_for_timeout(800)
  T.evaluate("()=>{const a=new Audio('sounds/morning.mp3');window.__o=a;a.muted=true;return a.play()}");T.wait_for_timeout(2000)
  print("offline <audio> plays:",T.evaluate("[!window.__o.paused,Math.round(window.__o.currentTime*10)/10,Math.round(window.__o.duration)]"))
  b.close()
