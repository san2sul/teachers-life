import json,sys,time
src=open(SP+'/t60.py' if False else '__TL_WORK__/t60.py').read();exec(src.split("with sync_playwright() as p:")[0])
import random
ros=[[f"101{i:02d}",n] for i,n in enumerate(["김가람","이나래","박다솜","최라온","정마루","한바다","윤사랑","오아름"],1)]
S["list"]=[{"id":"c1","data":{"v":3,"cls":"1학년 1반","roster":ros,"phones":{r[0]:"010-1111-22%02d"%i for i,r in enumerate(ros)},"emails":{r[0]:f"s{i}@ex.com" for i,r in enumerate(ros)},"teachers":[{"id":"t1","subject":"국어","name":"김국어","phone":"010-2222-3333"}],"msg":"m","sessions":[{"id":"s1","date":"2026-10-16","period":2,"absent":["10102"],"late":[],"calls":{}}]}},
 {"id":"c2","data":{"v":3,"cls":"1학년 2반","roster":ros[:3],"phones":{},"emails":{},"teachers":[],"msg":"m","sessions":[]}}]
S["staff"]=[{"id":"st1","name":"정교감","role":"교감","dept":"교무부","phone":"010-9999-0000"}]
S["tt"]={"list":[{"id":"t1","year":2026,"term":"2학기","start":"09:00","classMin":50,"breakMin":10,"lunchMin":60,"cells":{"0-1":{"subject":"물리학Ⅱ 심화","clsId":"c1","clsName":"","room":"과학실험실2"},"1-3":{"subject":"통합과학","clsId":"c2","clsName":"","room":"본관 304"}},"adj":{},"days":{},"chg":[{"id":"g1","scope":"cell","d":2,"p":4,"from":"2026-10-14","to":"2026-10-23","type":"cancel","reason":"올린 시간표 (임시)","created":1}]}],"active":"t1"}
S["events"]=[{"id":"e1","date":"2026-10-18","start":"10:00","end":"10:50","cat":"학생 면담","title":"학부모 상담 아주 긴 제목이 들어가는 경우를 확인합니다","memo":"메모","clsId":"c1","alarm":10,"important":True,"done":False}]
def ev(i,title,signed):
  st=[]
  for j,r in enumerate(ros):
    st.append({"sid":r[0],"name":r[1],"email":f"s{j}@ex.com","row":j+2,"vals":["30","20","45"],"tok":"tk%d%d"%(i,j),"h":0,"sentAt":1 if j<6 else 0,"sig":None})
  return {"id":"ev%d"%i,"manual":True,"title":title,"year":2026,"term":"2학기","clsId":"c1","clsName":"1학년 1반","created":i,"due":"2026-10-25","reply":"t@gmail.com","note":"","cols":["과제 수행","발표","보고서"],"colIdx":[],"file":{"name":"x","b64":""},"table":None,"stu":st}
S["evals"]=[ev(1,"1학기 수행평가 실험 보고서 (물리)",0),ev(2,"발표 평가",0)]
S["period"]={"year":2026,"term":"2학기"}
sizes=[(320,640),(360,740),(390,844),(430,932),(768,1024),(1024,768),(1440,900),(844,390)]
JS=r"""()=>{
const SEL='button,label.btn,input:not([type=checkbox]):not([type=radio]):not([type=file]),select,textarea,.chip,.card,.prow,.devinfo,.badge,.recbox,.ttdc,.evedbar,.abslist>div,.weekbar,.presets,.row2,.range,h2,.shlb';
const root=document.querySelector('#sheet:not([hidden]) #sheetBox')||document.querySelector('main.view:not([hidden])');
const els=[...root.querySelectorAll(SEL)].filter(e=>{if(e.closest('[hidden]'))return false;const r=e.getBoundingClientRect();if(r.width<2||r.height<2)return false;const cs=getComputedStyle(e);if(cs.visibility==='hidden'||cs.display==='none'||cs.position==='fixed')return false;if(e.closest('.ttgrid,table,.seg,.navb,.tabs,details>summary'))return false;if(e.closest('details:not([open])')&&!e.matches('details>summary'))return false;return true});
const clipped=e=>{let p=e.parentElement;const r=e.getBoundingClientRect();while(p&&p!==root){const cs=getComputedStyle(p);if(/auto|scroll|hidden/.test(cs.overflowY+cs.overflowX)){const q=p.getBoundingClientRect();if(r.bottom>q.bottom+1||r.top<q.top-1||r.right>q.right+1||r.left<q.left-1)return true}p=p.parentElement}return false};
const R=els.filter(e=>!clipped(e)).map(e=>{const r=e.getBoundingClientRect();return{e,x0:r.left,x1:r.right,y0:r.top+scrollY,y1:r.bottom+scrollY}});
const nm=e=>(e.id?'#'+e.id:(e.tagName.toLowerCase()+(e.classList[0]?'.'+e.classList[0]:'')))+(e.parentElement&&e.parentElement.id?'<#'+e.parentElement.id:'')+'"'+(e.textContent||e.value||'').trim().slice(0,14)+'"';
const out=[];
for(let i=0;i<R.length;i++)for(let j=i+1;j<R.length;j++){const a=R[i],b=R[j];if(a.e.contains(b.e)||b.e.contains(a.e))continue;if(a.e.parentElement===b.e.parentElement&&(a.e.matches('.prow,#verList>div,.abslist>div')))continue;
 const xi=Math.min(a.x1,b.x1)-Math.max(a.x0,b.x0),yi=Math.min(a.y1,b.y1)-Math.max(a.y0,b.y0);
 if(xi>1&&yi>1){out.push('OVERLAP '+nm(a.e)+' x '+nm(b.e)+' '+Math.round(yi));continue}
 if(xi>8){const g=a.y1<=b.y0?b.y0-a.y1:a.y0-b.y1;if(g>=-1&&g<5)out.push('TIGHT-V '+Math.round(g)+' '+nm(a.e)+' / '+nm(b.e))}
 else if(yi>8){const g=a.x1<=b.x0?b.x0-a.x1:a.x0-b.x1;if(g>=-1&&g<4)out.push('TIGHT-H '+Math.round(g)+' '+nm(a.e)+' | '+nm(b.e))}
}
return out}"""
def scenes(T):
  for v in ["tt","att","call","todo","set"]:
    yield v,f"document.querySelector('.navb[data-v={v}]').click();document.querySelectorAll('main.view:not([hidden]) details').forEach(d=>d.open=true)"
  for tab in ["eval","att"]:
    yield "stat-"+tab,f"document.querySelector('.navb[data-v=stat]').click();const b=document.querySelector('#stabs .chip[data-t={tab}]');b&&b.click();document.querySelectorAll('main.view:not([hidden]) details').forEach(d=>d.open=true)"
  yield "eval-edit","document.querySelector('.navb[data-v=stat]').click();document.querySelector('#stabs .chip[data-t=eval]').click();document.getElementById('evEdit').click()"
  yield "eval-detail","document.getElementById('evEdit').click();document.querySelector('[data-ev]').click()"
  yield "att-obs","document.querySelector('.navb[data-v=att]').click();const b=document.querySelector('[data-m=obs],#modeObs');b&&b.click()"
  yield "sheet-newterm","document.querySelector('.navb[data-v=set]').click();document.getElementById('perNew').click()"
  yield "sheet-event","document.querySelector('.navb[data-v=tt]').click();document.getElementById('agAdd').click()"
with sync_playwright() as p:
  b=p.chromium.launch();tot={}
  for w,h in sizes:
    c=b.new_context(viewport={"width":w,"height":h},service_workers="block");c.route("**/*",handler);T=c.new_page();T.on("pageerror",lambda e:errs.append(str(e)))
    T.goto("https://tl.test/index.html");T.evaluate("s=>{localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-lastver','9.9.9')}",json.dumps(S));T.reload();T.wait_for_timeout(400)
    for name,js in scenes(T):
      try:T.evaluate("()=>{document.getElementById('sheet').hidden=true;"+js+"}")
      except Exception as e:print("scene err",name,e);continue
      T.wait_for_timeout(150)
      r=T.evaluate(JS)
      for x in r:tot.setdefault((name,x),[]).append(w)
      if len(sys.argv)>1 and name in sys.argv[1:]:T.screenshot(path=f"{SP}/b_{w}_{name}.png",full_page=True)
    c.close()
  b.close()
for (n,x),ws in sorted(tot.items()):print(n,x,ws)
print("errs",errs)
