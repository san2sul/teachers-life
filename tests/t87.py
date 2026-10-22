src=open('audit2.py').read();exec(src.split("sizes=")[0])
with sync_playwright() as p:
  b=p.chromium.launch();c=b.new_context(viewport={"width":390,"height":844},service_workers="block");c.route("**/*",handler);T=c.new_page();T.on("pageerror",lambda e:errs.append(str(e)))
  T.goto("https://tl.test/index.html");T.evaluate("s=>{localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-lastver','9.9.9')}",json.dumps(S));T.reload();T.wait_for_timeout(400)
  print("tipboxes per view:",T.evaluate("[...document.querySelectorAll('main.view')].map(m=>m.id+':'+m.querySelectorAll('.tipbox').length).join(' ')"))
  print("d-me open (no name):",T.evaluate("document.getElementById('d-me').open"))
  T.click(".navb[data-v=tt]");box=T.locator("#v-tt .tipbox:visible").first
  print("hidden before:",box.locator(".tipc").is_visible());box.locator(".tipq").click();print("visible after click:",box.locator(".tipc").is_visible())
  T.click(".navb[data-v=set]");T.evaluate("document.getElementById('d-ui').open=true");T.click("[data-ui=tip] .chip[data-v=open]")
  T.click(".navb[data-v=att]");print("att tip visible w/ pref:",T.locator("#v-att .tipbox:visible .tipc").first.is_visible(),T.evaluate("document.documentElement.dataset.tip"))
  T.reload();T.wait_for_timeout(300);print("after reload attr:",T.evaluate("document.documentElement.dataset.tip"))
  print("errbar:",T.evaluate("(()=>{const b=document.getElementById('errBar');return b&&!b.hidden?b.innerText:''})()"))
  b.close()
print(errs)
