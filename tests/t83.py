import openpyxl,zipfile,re
src=open('audit2.py').read();exec(src.split("sizes=")[0])
for st in S["evals"][0]["stu"][:4]:st["sig"]={"at":1760000000000,"pts":[[10,10,200,100,300,40]],"w":600,"hh":240,"h":0}
def run(mut,label):
  with sync_playwright() as p:
    b=p.chromium.launch();c=b.new_context(viewport={"width":390,"height":844},service_workers="block",accept_downloads=True);c.route("**/*",handler)
    T=c.new_page();E=[];T.on("pageerror",lambda e:E.append(str(e)))
    T.goto("https://tl.test/index.html");T.evaluate("s=>{localStorage.clear();localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-lastver','9.9.9');localStorage.setItem('att-app-me','홍')}",json.dumps(mut(S)));T.reload();T.wait_for_timeout(800)
    T.click(".navb[data-v=stat]");T.click("#stabs .chip[data-t=eval]");T.click("[data-ev=ev1]");T.wait_for_timeout(200)
    print(label,"detail:",T.inner_text("#evDetail")[:60].replace("\n"," "))
    T.click("#evXl");T.wait_for_timeout(300)
    with T.expect_download() as d:T.click("#eoOk")
    path=SP+"/m_"+label+".xlsx";d.value.save_as(path)
    z=zipfile.ZipFile(path);imgs=[n for n in z.namelist() if n.startswith("xl/media/")];dr=[n for n in z.namelist() if "drawings/drawing" in n and n.endswith(".xml")]
    rows=re.findall(r"<xdr:from><xdr:col>(\d+)</xdr:col><xdr:colOff>0</xdr:colOff><xdr:row>(\d+)</xdr:row>",z.read(dr[0]).decode()) if dr else []
    ws=openpyxl.load_workbook(path).worksheets[0]
    print("  images:",len(imgs),"anchors(col,row0):",rows[:5]);
    for r in ws.iter_rows(min_row=1,max_row=7,values_only=True):print("   ",[x for x in r if x not in (None,"")][:9])
    print("  ",E);b.close()
run(lambda s:s,"manual")
