src=open('audit2.py').read();exec(src.split("sizes=")[0])
js=open("stressS.json").read()
CLK="(()=>{const fixed=new Date('2026-10-22T10:20:00+09:00').getTime();const D=Date;const off=fixed-D.now();class FD extends D{constructor(...a){if(!a.length)super(D.now()+off);else super(...a)}static now(){return D.now()+off}};window.Date=FD})()"
F=[]
def ok(c,m):print(("OK  " if c else "FAIL"),m);(None if c else F.append(m))
with sync_playwright() as p:
  b=p.chromium.launch()
  for W in (1440,390):
    c=b.new_context(viewport={"width":W,"height":900},service_workers="block");c.route("**/*",handler);T=c.new_page();T.on("pageerror",lambda e:errs.append(str(e)))
    T.add_init_script(CLK);T.add_init_script("try{localStorage.setItem('att-app-cheer',JSON.stringify({am:false,pm:false}))}catch(e){}")
    T.goto("https://tl.test/index.html");T.evaluate("s=>{localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-lastver','9.9.9');localStorage.setItem('att-app-setup','1')}",js);T.reload();T.wait_for_timeout(900)
    T.click(".navb[data-v=tt]");T.wait_for_timeout(300)
    ok(T.evaluate("document.querySelector('.ttg').dataset.tc")=="3",f"[{W}] today column marked (Thu)")
    ok(T.evaluate("!!document.querySelector('.tc.now')") and T.evaluate("!!document.querySelector('.ttg tr.live')"),f"[{W}] current lesson highlighted")
    vis=T.evaluate("getComputedStyle(document.getElementById('ttSide')).display")
    if W>=1100:
      ok(vis=="flex","panel shown on wide screen")
      ok(T.evaluate("document.querySelectorAll('#ttSide .tsl').length")>=4 and T.evaluate("!!document.querySelector('#ttSide .tsl.live')"),"panel lists today's lessons with live one")
      r=T.evaluate("(()=>{const a=document.querySelector('.ttg').getBoundingClientRect(),b=document.getElementById('ttSide').getBoundingClientRect(),h=document.getElementById('helpBtn').getBoundingClientRect();return [a.right<=b.left,h.right<=b.left]})()");ok(r[0] and r[1],"timetable and help button don't overlap panel")
      n=T.evaluate("document.querySelectorAll('#ttSide [data-ti]').length");T.click("#ttSide [data-ti] >> nth=0");T.wait_for_timeout(200);ok(T.evaluate("document.querySelectorAll('#ttSide [data-ti]').length")==n-1,"check off a to-do from panel")
      T.click("#ttSide .tsl.live");T.wait_for_timeout(300);ok(T.evaluate("!document.getElementById('v-att').hidden"),"tap lesson -> attendance")
      T.click(".navb[data-v=att]");ok(T.evaluate("getComputedStyle(document.getElementById('ttSide')).display")=="none" or T.evaluate("document.getElementById('v-tt').hidden"),"panel only on timetable view")
      T.set_viewport_size({"width":900,"height":900});T.click(".navb[data-v=tt]");T.wait_for_timeout(400);ok(T.evaluate("getComputedStyle(document.getElementById('ttSide')).display")=="none","panel hides when window narrows")
    else:
      ok(vis=="none","no panel on phone")
      ok(T.evaluate("document.documentElement.scrollWidth<=innerWidth+1"),"no horizontal scroll on phone")
    rad=T.evaluate("[...new Set([...document.querySelectorAll('main.view:not([hidden]) *')].filter(e=>e.offsetParent).map(e=>getComputedStyle(e).borderTopLeftRadius).filter(r=>r!=='0px'))]")
    print("   radii in use:",rad)
    wts=T.evaluate("[...new Set([...document.querySelectorAll('body *')].filter(e=>e.offsetParent&&e.childNodes.length&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())).map(e=>getComputedStyle(e).fontWeight))]");print("   weights in use:",wts)
    c.close()
  b.close()
print("fails",F);print(errs)
