src=open('audit2.py').read();exec(src.split("sizes=")[0])
import sys
F=SP+"/acf/"
def run(T,fname=None,text=None,past=True,shot=None):
  T.click(".navb[data-v=tt]");T.evaluate("document.getElementById('ttChg').open=true");T.click("#acUp")
  if fname:T.set_input_files("#acIn",F+fname)
  else:T.fill("#acTxt",text);T.click("#acRead")
  for i in range(90):
    if T.is_visible("#acList") or "skip" in (T.inner_html("#acMsg") if T.is_visible("#acMsg") else ""):break
    T.wait_for_timeout(500)
  if not T.is_visible("#acList"):print("  FAIL msg:",T.inner_text("#acMsg"));T.click("#skNo");return None
  if past and T.is_visible("#acPast"):T.check("#acPast")
  rows=T.evaluate("[...document.querySelectorAll('#acList .acrow')].map(r=>r.querySelector('.acd').innerText.replace(/\\n/g,'')+' | '+r.querySelector('[data-t]').value+' | '+r.querySelector('select').selectedOptions[0].text)")
  for r in rows:print("   ",r)
  print("  sum:",T.inner_text("#acSum"))
  if shot:T.screenshot(path=SP+"/shot/"+shot)
  return rows
with sync_playwright() as p:
  b=p.chromium.launch();c=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,service_workers="block");c.route("**/*",handler);T=c.new_page();T.on("pageerror",lambda e:errs.append(str(e)))
  T.goto("https://tl.test/index.html");T.evaluate("s=>{localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-lastver','9.9.9');localStorage.setItem('att-app-me','김물리');localStorage.setItem('att-app-setup','1')}",json.dumps(S));T.reload();T.wait_for_timeout(500)
  for f in ["cal_grid.xlsx","cal_cols.xlsx","cal_list.xlsx","cal.pdf","cal.png"]:
    print("==",f);r=run(T,f,shot="ac_"+f.split('.')[0]+"_"+f.split('.')[1]+".png")
    if r is not None:T.click("#skNo") if T.is_visible("#skNo") else T.evaluate("document.getElementById('sheet').hidden=true")
  print("== paste");run(T,text="10.28.(수) ~ 10.30.(금) 2학기 2차 지필평가\n11월 13일 개교기념일\n12.24 단축수업\n3-4교시 수업 공개\n11/5 학부모 상담주간")
  # apply
  T.click("#acOk");T.wait_for_timeout(300);print("toast:",T.evaluate("(document.querySelector('.toast')||{}).textContent"))
  st=T.evaluate("JSON.parse(localStorage.getItem('att-app-v2'))")
  for t in st['tt']['list']:print("tt",t['year'],t['term'],"chg day:",[(x['from'],x['to'],x['reason']) for x in t['chg'] if x['scope']=='day'],"days:",{k:(v['classMin'],v['note']) for k,v in t['days'].items()})
  print("events:",[(e['date'],e['title'],e['cat']) for e in st['events'] if e['id'].startswith('ac')])
  # reimport same → no duplicates
  run(T,text="10.28.(수) ~ 10.30.(금) 2학기 2차 지필평가\n11/5 학부모 상담주간",past=True);T.click("#acOk");T.wait_for_timeout(200)
  st=T.evaluate("JSON.parse(localStorage.getItem('att-app-v2'))");t=st['tt']['list'][0]
  print("after reimport chg:",len([x for x in t['chg'] if x['scope']=='day']),"events ac:",len([e for e in st['events'] if e['id'].startswith('ac')]))
  # timetable view shows cancel on 10/28 week
  T.click(".navb[data-v=tt]");T.evaluate("()=>{}")
  b.close()
print(errs)
