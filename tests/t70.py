import sys
src=open('t60.py').read();exec(src.split("with sync_playwright() as p:")[0])
S["list"]+= [{"id":"c2","data":{"v":3,"cls":"1학년 2반","roster":[["10201","최라"]],"phones":{},"emails":{},"teachers":[],"msg":"m","sessions":[]}},{"id":"c3","data":{"v":3,"cls":"1학년 3반","roster":[["10301","정마"]],"phones":{},"emails":{},"teachers":[],"msg":"m","sessions":[]}}]
def st(T):return json.loads(T.evaluate("localStorage.getItem('att-app-v2')"))
def up(T,f):
  T.set_input_files("#ttUpIn",SP+"/ttimg/"+f)
  T.wait_for_selector("#ttUpNext,#sheetBox h2:has-text('찾지')",timeout=120000);T.wait_for_timeout(200)
W=int(sys.argv[1]) if len(sys.argv)>1 else 390
with sync_playwright() as p:
  b=p.chromium.launch();c=ctx(b,W);T=c.new_page();T.on("pageerror",lambda e:errs.append(str(e)));T.on("console",lambda m:m.type=="error" and errs.append("c:"+m.text))
  T.goto("https://tl.test/index.html");T.evaluate("s=>{localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-view','tt');localStorage.setItem('att-app-lastver','9.9.9')}",json.dumps(S));T.reload();T.wait_for_timeout(500)
  T.screenshot(path=SP+"/u0.png")
  T.click(".navb[data-v=tt]");T.wait_for_timeout(200);print("empty visible:",T.is_visible("#ttUpBtn2"))
  up(T,"cap_phone.png")
  print("info:",T.inner_text("#ttUpInfo"))
  print("cells:",T.evaluate("[...document.querySelectorAll('.ttin')].filter(t=>t.value).map(t=>t.dataset.k+'='+t.value).join(' | ')"))
  T.screenshot(path=SP+"/u1.png")
  T.click("#ttUpNext");T.wait_for_timeout(200);print("decide:",T.inner_text("#sheetBox")[:300].replace("\n"," | "));T.screenshot(path=SP+"/u2.png")
  T.click("#ttDcOk");T.wait_for_timeout(300)
  s=st(T);t=s['tt']['list'][0];print("fixed cells:",{k:(v['subject'],v['clsName'],v['clsId']) for k,v in sorted(t['cells'].items())},"start",t['start'])
  T.screenshot(path=SP+"/u3.png")
  up(T,"cap_phone2.png");print("info2:",T.inner_text("#ttUpInfo"))
  T.click("#ttUpNext");T.wait_for_timeout(200);print("decide2:",T.inner_text("#sheetBox")[:700].replace("\n"," | "));T.screenshot(path=SP+"/u4.png",full_page=True)
  T.click("#ttDcOk");T.wait_for_timeout(300)
  s=st(T);t=s['tt']['list'][0];print("chg:",[(c['d'],c['p'],c['type'],c['subject'],c['clsName'],c['from'],c['to']) for c in t['chg']]);print("cells n",len(t['cells']))
  print("week:",T.inner_text("#ttWeekTxt"))
  T.screenshot(path=SP+"/u5.png")
  # re-upload same week: should say already applied
  up(T,"cap_phone2.png");T.click("#ttUpNext");T.wait_for_timeout(200);print("decide3:",T.inner_text("#sheetBox")[:300].replace("\n"," | "))
  b.close()
print(errs)
