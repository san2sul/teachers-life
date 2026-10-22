src=open('t50.py').read();exec(src.split("with sync_playwright() as p:")[0])
import datetime
T0=datetime.date.today().isoformat()
ros=[["10101","김가"],["10102","이나"],["10103","박다"]]
ST={"active":"c1","list":[{"id":"c1","data":{"v":3,"cls":"1학년 1반","roster":ros,"phones":{},"emails":{},"teachers":[],"msg":"m","sessions":[{"id":"s1","date":T0,"time":"09:00","label":"1교시","p":{}}]}}],"staff":[]}
DELAY="""(()=>{const of=window.fetch;window.__delay=0;window.fetch=async(...a)=>{const u=String(a[0]&&a[0].url||a[0]);if(window.__delay&&/alt=media/.test(u))await new Promise(r=>setTimeout(r,window.__delay));return of(...a)}})()"""
def toggles(pg):return pg.evaluate("[...document.querySelectorAll('#list .st')].map(r=>r.classList.contains('on')?1:0).join('')")
with sync_playwright() as p:
  b=p.chromium.launch()
  A=dev(b,"A",ST)
  A.evaluate("localStorage.setItem('att-app-setup','1')")
  A.evaluate("document.querySelectorAll('#v-set details').forEach(d=>d.open=true)");A.click("#gsLogin");A.wait_for_timeout(1500)
  B=dev(b,"Bphone");B.add_init_script(DELAY);B.reload();B.wait_for_timeout(400)
  if B.is_visible("#wzHave"):B.click("#wzHave")
  B.evaluate("document.querySelectorAll('#v-set details').forEach(d=>d.open=true)");B.click("#gsLogin");B.wait_for_timeout(1800)
  for X in (A,B):X.click(".navb[data-v=att]");X.wait_for_timeout(200)
  print("start A",toggles(A),"B",toggles(B))
  # 1) concurrent edits of same session on two devices
  A.click("#list .st >> nth=0");B.click("#list .st >> nth=1");A.wait_for_timeout(200)
  A.evaluate("document.querySelector('.navb[data-v=set]').click()");A.evaluate("document.getElementById('d-sync').open=true");A.click("#gsNow");A.wait_for_timeout(1200)
  B.evaluate("document.querySelector('.navb[data-v=set]').click()");B.evaluate("document.getElementById('d-sync').open=true");B.click("#gsNow");B.wait_for_timeout(1500)
  A.click("#gsNow");A.wait_for_timeout(1200)
  for X in (A,B):X.click(".navb[data-v=att]");X.wait_for_timeout(150)
  print("after merge A",toggles(A),"B",toggles(B),"(expect 110 both)")
  # 2) toggle during slow download on B
  A.click("#list .st >> nth=2");A.evaluate("document.querySelector('.navb[data-v=set]').click()");A.click("#gsNow");A.wait_for_timeout(1200);A.click(".navb[data-v=att]")
  B.evaluate("window.__delay=2500");B.evaluate("document.querySelector('.navb[data-v=set]').click()");B.click("#gsNow");B.wait_for_timeout(300)
  B.click(".navb[data-v=att]");B.click("#list .st >> nth=0");print("B toggled during download:",toggles(B))
  B.wait_for_timeout(3500);print("B after sync applied:",toggles(B),"(expect 011: A's 3rd on, B's 1st off)")
  B.evaluate("window.__delay=0");B.wait_for_timeout(4500)
  A.evaluate("document.querySelector('.navb[data-v=set]').click()");A.click("#gsNow");A.wait_for_timeout(1200);A.click(".navb[data-v=att]")
  print("final A",toggles(A),"B",toggles(B))
  b.close()
print(errs)
