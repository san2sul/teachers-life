# 큰 자료(평가 전표 파일 b64 포함) 시나리오 - t82가 사용 (재구성)
src=open('audit2.py').read();exec(src.split("sizes=")[0])
import copy,base64,os
SS=copy.deepcopy(S)
blob=base64.b64encode(os.urandom(90000)).decode()
SS["evals"]=[]
for i in range(1,31):
  e=ev(i,f"수행평가 {i}",0);e["file"]={"name":f"평가{i}.xlsx","b64":blob};SS["evals"].append(e)
js=json.dumps(SS,ensure_ascii=False)
print("SS chars",len(js))
