exec(open('stress.py').read().split("js=json.dumps")[0])
import json
for e in SS["evals"]:
  for st in e["stu"]:st["sig"]={"at":1,"pts":[[1,2,3,4]]*40,"w":600,"hh":240,"h":0}
js=json.dumps(SS,ensure_ascii=False)
def lsinfo(T):return T.evaluate("(()=>{let n=0;for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);n+=(k.length+localStorage.getItem(k).length)}return {chars:n,keys:Object.keys(localStorage).sort()}})()")
def idbkeys(T):return T.evaluate("new Promise(r=>{const q=indexedDB.open('teachers-life-media');q.onsuccess=()=>{try{const t=q.result.transaction('m').objectStore('m').getAllKeys();t.onsuccess=()=>r(t.result.map(String))}catch(e){r([])}};q.onerror=()=>r('err')})")
with sync_playwright() as p:
  b=p.chromium.launch();c=ctx(b,390);T=c.new_page();E=[];T.on("pageerror",lambda e:E.append(str(e)))
  T.goto("https://tl.test/index.html")
  T.evaluate("([s])=>{localStorage.clear();localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-gbase',s.slice(0,300000));localStorage.setItem('att-app-undo',JSON.stringify({at:'2026-10-19T10:00:00Z',S:{list:[]}}));localStorage.setItem('att-app-prof:x@y.com','{\"S\":{}}');localStorage.setItem('att-app-view','set');localStorage.setItem('att-app-lastver','9.9.9')}",[js])
  print("before:",lsinfo(T)["chars"])
  T.reload();T.wait_for_timeout(3000)
  li=lsinfo(T);ks=idbkeys(T);print("after chars:",li["chars"],"keys:",[k for k in li["keys"] if k.startswith("att-app")]);print("idb:",len([k for k in ks if k.startswith("f:")]),"files",[k for k in ks if k.startswith("kv:")])
  T.evaluate("document.getElementById('d-bk').open=true");T.wait_for_timeout(500);print("meter:",T.inner_text("#stoMeter").replace("\n"," / "))
  print("undo btn:",T.evaluate("!document.getElementById('undoBtn').hidden"))
  T.reload();T.wait_for_timeout(1500)
  print("hydrated b64 len:",T.evaluate("new Promise(r=>setTimeout(()=>r(JSON.parse(localStorage.getItem('att-app-v2')).evals[0].file.b64.length),10))"),"| mem via backup:")
  with T.expect_download() as dl:T.evaluate("document.getElementById('backupFile').click()")
  bk=json.load(open(dl.value.path()));print("  backup eval b64 len:",len(bk["evals"][0]["file"]["b64"]),"| bknag/lastbackup:",T.evaluate("localStorage.getItem('att-app-lastbackup')!=null"))
  T.evaluate("document.getElementById('undoBtn').click()");T.wait_for_timeout(400);print("undo sheet:",T.inner_text("#sheetBox")[:60].replace("\n"," "))
  b.close()
print(E)
