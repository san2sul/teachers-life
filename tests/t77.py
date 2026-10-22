src=open('t60.py').read();exec(src.split("with sync_playwright() as p:")[0])
cases={"fresh":None,"legacy":json.dumps(S)}
with sync_playwright() as p:
  b=p.chromium.launch();dev=p.devices["iPhone 13"]
  for name,data in cases.items():
    c=b.new_context(**{k:v for k,v in dev.items() if k!="default_browser_type"},service_workers="block");c.route("**/*",handler)
    T=c.new_page();E=[];T.on("pageerror",lambda e:E.append(str(e)));T.on("console",lambda m:m.type=="error" and E.append("c:"+m.text))
    T.goto("https://tl.test/index.html")
    T.evaluate("s=>{localStorage.clear();if(s)localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-view','set')}",data);T.reload();T.wait_for_timeout(1000)
    print(name,"perY opts:",T.evaluate("document.getElementById('perY').options.length"),"| gsBody:",T.evaluate("document.getElementById('gsBody').textContent.length"),"| meTag:",T.inner_text("#meTag"),"|",E[:3])
    c.close()
  b.close()
