import zipfile,re,openpyxl
src=open('t60.py').read();exec(src.split("with sync_playwright() as p:")[0])
def orient(path):
  z=zipfile.ZipFile(path);x=z.read("xl/worksheets/sheet1.xml").decode();m=re.search(r'orientation="(\w+)"',x);return m.group(1) if m else None
def info(path):
  ws=openpyxl.load_workbook(path).worksheets[0];return orient(path),ws.row_dimensions[1].height,ws["A1"].alignment.wrap_text,ws.row_dimensions[2].height
with sync_playwright() as p:
  b=p.chromium.launch();c=ctx(b,390);T=c.new_page();E=[];T.on("pageerror",lambda e:E.append(str(e)))
  T.add_init_script("window.print=()=>{}")
  T.goto("https://tl.test/index.html");T.evaluate("s=>{localStorage.clear();localStorage.setItem('att-app-v2',s);localStorage.setItem('att-app-lastver','9.9.9');localStorage.setItem('att-app-me','홍길동')}",json.dumps(S));T.reload();T.wait_for_timeout(500)
  T.click(".navb[data-v=stat]");T.click("#stabs .chip[data-t=eval]")
  outs={}
  for name,title,items in [("long","2026학년도 현장체험학습 사전 안전교육 이수 확인서",""),("wide","수행평가 전표","1차, 2차, 3차, 4차, 5차, 6차, 7차, 8차, 9차, 총점, 의견")]:
    T.click("#evTpl");T.wait_for_timeout(200);T.fill("#tpT",title);T.fill("#tpI",items)
    with T.expect_download() as d:T.click("#tpOk")
    pth=SP+f"/o_{name}.xlsx";d.value.save_as(pth);outs[name]=pth;print(name,"orient,h1,wrap,h2:",info(pth))
  # manual agree eval with long title, then signed export with orientation landscape forced
  T.click("#evNew");T.click("#kdChips [data-kd=agree]");T.fill("#mnT","2026학년도 과학실 안전 수칙 준수 및 실험 보고서 작성 서약서");T.fill("#mnR","t@gmail.com");T.click("#mnOk");T.wait_for_timeout(300)
  T.click("#evXl");T.wait_for_timeout(200);print("orient note:",T.inner_text("#eoOrN"))
  with T.expect_download() as d:T.click("#eoOk")
  pth=SP+"/o_signed.xlsx";d.value.save_as(pth);outs["signed"]=pth;print("signed auto:",info(pth))
  T.click("#evXl");T.wait_for_timeout(200);T.click("#eoOr [data-or=landscape]")
  with T.expect_download() as d:T.click("#eoOk")
  pth=SP+"/o_signed2.xlsx";d.value.save_as(pth);print("signed landscape:",info(pth))
  T.click("#evPdf");T.wait_for_timeout(200);T.click("#eoOk");T.wait_for_timeout(500);print("pdf @page:",T.evaluate("document.getElementById('printPage').textContent"))
  T.locator(".ppage").screenshot(path=SP+"/o_pdf.png")
  b.close()
print(E)
