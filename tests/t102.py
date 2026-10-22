src=open('audit2.py').read();exec(src.split("sizes=")[0])
import sys
def run(hhmm,label,extra=""):
  with sync_playwright() as p:
    b=p.chromium.launch();c=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,service_workers="block");c.route("**/*",handler);T=c.new_page();T.on("pageerror",lambda e:errs.append(str(e)))
    # fake clock: Wed 2026-10-21 at hh:mm
    T.add_init_script("(()=>{const fixed=new Date('2026-10-21T%s:00+09:00').getTime();const D=Date;const off=fixed-D.now();class FD extends D{constructor(...a){if(!a.length)super(D.now()+off);else super(...a)}static now(){return D.now()+off}};window.Date=FD})()"%hhmm)
    T.goto("https://tl.test/index.html");T.evaluate("s=>{localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-lastver','9.9.9');localStorage.setItem('att-app-me','김물리');localStorage.setItem('att-app-setup','1');localStorage.setItem('att-app-cheer','{}')"+extra+"}",json.dumps(S));T.reload();T.wait_for_timeout(2200)
    print(label,"popup:",T.is_visible(".cheer"),"|",T.inner_text(".cheer").replace("\n"," | ")[:260] if T.is_visible(".cheer") else "")
    if T.is_visible(".cheer"):
      T.screenshot(path=SP+f"/shot/cheer_{label}.png")
      T.click("[data-cplay]");T.wait_for_timeout(600);print("  playing:",T.evaluate("document.querySelector('[data-cplay]').classList.contains('playing')"))
      if T.is_visible("#chMood"):T.click("#chMood [data-m=tired]");print("  reply:",T.inner_text("#chRe"));T.fill("#chNote","민수가 처음 질문을 했다")
      T.click("#chGo");T.wait_for_timeout(200);print("  closed:",not T.is_visible(".cheer"),"music stopped:",T.evaluate("!document.querySelector('.cplay.playing')"))
      print("  diary:",T.evaluate("localStorage.getItem('att-app-diary')"))
      T.reload();T.wait_for_timeout(2200);print("  again same day popup:",T.is_visible(".cheer"))
    T.click(".navb[data-v=set]");T.evaluate("document.getElementById('d-cheer').open=true");T.wait_for_timeout(200)
    if label=="am":print("  settings:",T.inner_text("#cheerBody").replace("\n"," | ")[:300]);T.screenshot(path=SP+"/shot/cheer_set.png",full_page=True)
    b.close()
run("07:40","am");run("17:10","pm");run("10:00","off",";localStorage.setItem('att-app-cheer',JSON.stringify({am:false}))")
print(errs)
