/* 교사의 생활 — 학생 서류(결석신고서 · 현장체험학습 신청서 · 결과보고서) 양식과 서류 그리기. 앱(index.html)과 form.html이 함께 씁니다. */
(function(){"use strict";
var esc=function(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]})};
var REL=["부","모","조부","조모","기타 보호자"];
var FORMS={
  absence:{ti:"결석신고서",ic:"🏥",ev:"진료확인서 · 처방전 · 의사 소견서 등 증빙 서류",evReq:true,ok:"위와 같이 결석하였기에 증빙 서류를 첨부하여 신고합니다.",
    f:[{k:"kind",l:"결석 구분",type:"select",o:["질병결석","출석인정결석","기타결석","미인정결석"],req:1},
       {k:"from",l:"결석 시작일",type:"date",req:1},{k:"to",l:"결석 끝난 날",type:"date",req:1},
       {k:"reason",l:"결석 사유",type:"area",req:1,ph:"예: 감기 몸살로 고열이 나서 병원 진료를 받고 집에서 쉼"},
       {k:"doc",l:"증빙 서류 종류",type:"select",o:["진료확인서","처방전","의사 소견서","진단서","입원 · 퇴원 확인서","학부모 확인서","기타","없음"],req:1}]},
  trip:{ti:"교외체험학습 신청서",ic:"🧳",ev:"체험학습 계획서 · 일정표 등 (선택)",evReq:false,ok:"위와 같이 교외체험학습을 신청합니다.",
    f:[{k:"from",l:"체험학습 시작일",type:"date",req:1},{k:"to",l:"체험학습 끝나는 날",type:"date",req:1},
       {k:"type",l:"체험학습 형태",type:"select",o:["가족 동반 여행","친인척 방문","고적 답사 · 문화 탐방","견학 활동","체험 활동","진로 탐색","기타"],req:1},
       {k:"place",l:"목적지 (장소)",type:"text",req:1,ph:"예: 경주 불국사 · 석굴암"},
       {k:"purpose",l:"체험학습 목적",type:"area",req:1,ph:"예: 신라의 역사 유적을 직접 보고 역사 수업 내용을 깊이 이해하기"},
       {k:"plan",l:"세부 계획 (일정)",type:"area",req:0,ph:"예: 1일차 불국사 · 석굴암 / 2일차 국립경주박물관 · 대릉원"},
       {k:"gname",l:"인솔 보호자 이름",type:"text",req:1},{k:"grel",l:"인솔 보호자 관계",type:"select",o:REL,req:1},{k:"gtel",l:"인솔 보호자 연락처",type:"tel",req:1}]},
  report:{ti:"교외체험학습 결과보고서",ic:"📸",ev:"체험 사진 · 입장권 · 영수증 등 증빙 자료",evReq:true,ok:"위와 같이 교외체험학습 결과를 보고합니다.",
    f:[{k:"from",l:"체험학습 시작일",type:"date",req:1},{k:"to",l:"체험학습 끝난 날",type:"date",req:1},
       {k:"place",l:"다녀온 곳 (장소)",type:"text",req:1},
       {k:"content",l:"체험 내용",type:"area",req:1,ph:"날짜별로 무엇을 보고 배우고 했는지 적어 주세요"},
       {k:"feel",l:"느낀 점 · 배운 점",type:"area",req:1}]}};
function days(a,b){if(!/^\d{4}-\d{2}-\d{2}$/.test(a||"")||!/^\d{4}-\d{2}-\d{2}$/.test(b||""))return 0;var x=new Date(a+"T00:00"),y=new Date(b+"T00:00");var n=Math.round((y-x)/864e5)+1;return n>0?n:0}
function wdays(a,b){var n=days(a,b),c=0;if(!n||n>400)return n;var x=new Date(a+"T00:00");for(var i=0;i<n;i++){var w=x.getDay();if(w>0&&w<6)c++;x.setDate(x.getDate()+1)}return c}
function kday(s){if(!/^\d{4}-\d{2}-\d{2}/.test(s||""))return"";var d=new Date(s.slice(0,10)+"T00:00");return d.getFullYear()+"년 "+(d.getMonth()+1)+"월 "+d.getDate()+"일 ("+"일월화수목금토"[d.getDay()]+")"}
/* 서명: [[x,y],...] 획들 (가로 600 · 세로 240 기준) */
function sigSVG(sg){if(!sg||!Array.isArray(sg.p)||!sg.p.length)return'<span class="tfnosig">(서명 없음)</span>';var W=+sg.w||600,H=+sg.h||240;
  return'<svg class="tfsig" viewBox="0 0 '+W+' '+H+'" xmlns="http://www.w3.org/2000/svg"><path d="'+sg.p.map(function(a){return(a||[]).map(function(p,i){return(i?"L":"M")+(+p[0]||0)+" "+(+p[1]||0)}).join("")+((a||[]).length===1?"l0.1 0":"")}).join("")+'" fill="none" stroke="#111" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'}
function fval(f,v){if(v==null||v==="")return"";if(f.type==="date")return kday(v);return String(v)}
/* 서류 한 장 (인쇄 · 파일 · 앱 보기 공통) */
function docHTML(rq,s,o){o=o||{};var F=FORMS[rq.t]||FORMS.absence,d=s.d||{},sch=rq.sch||"",at=s.at||new Date().toISOString();
  var h='<article class="tfdoc"><h1>'+esc(F.ti)+'</h1>'+(sch?'<div class="tfsch">'+esc(sch)+'</div>':"")+'<table class="tft"><tbody>';
  h+='<tr><th>학년 · 반</th><td>'+esc(rq.cls||d.cls||"")+'</td><th>번호 (학번)</th><td>'+esc(s.no||d.no||"")+'</td></tr><tr><th>이름</th><td colspan="3">'+esc(s.nm||d.nm||"")+'</td></tr>';
  var per=d.from&&d.to?kday(d.from)+" ~ "+kday(d.to)+" ("+days(d.from,d.to)+"일간 · 평일 "+wdays(d.from,d.to)+"일)":"";
  F.f.forEach(function(f){if(f.k==="from"||f.k==="to")return;h+='<tr><th>'+esc(f.l)+'</th><td colspan="3" class="'+(f.type==="area"?"tfa":"")+'">'+esc(fval(f,d[f.k])).replace(/\n/g,"<br>")+'</td></tr>'});
  if(per){var k=h.indexOf('</tr>',h.indexOf('<th>이름</th>'))+5;h=h.slice(0,k)+'<tr><th>기간</th><td colspan="3">'+esc(per)+'</td></tr>'+h.slice(k)}
  h+='<tr><th>보호자</th><td colspan="3">'+esc([d.pname,d.prel?"("+d.prel+")":"",d.ptel].filter(Boolean).join(" "))+'</td></tr>';
  var fl=s.files||[];h+='<tr><th>첨부</th><td colspan="3">'+(fl.length?fl.map(function(x,i){return esc((i+1)+". "+(x.name||"파일")+(x.size?" ("+Math.max(1,Math.round(x.size/1024))+"KB)":""))}).join("<br>"):"없음")+'</td></tr>';
  h+='</tbody></table><p class="tfok">'+esc(F.ok)+'</p><p class="tfdate">'+esc(kday(at))+'</p>';
  h+='<div class="tfsigs"><div><span>학생</span><b>'+esc(s.nm||d.nm||"")+'</b>'+sigSVG(s.sg&&s.sg.st)+'</div><div><span>보호자</span><b>'+esc(d.pname||"")+'</b>'+sigSVG(s.sg&&s.sg.pa)+'</div></div>';
  h+='<p class="tfto">'+esc(sch?sch+"장 귀하":"학교장 귀하")+'</p>';
  if(o.imgs){var im=fl.map(function(x){return o.imgs[x.id]?'<figure><img src="'+o.imgs[x.id]+'" alt="'+esc(x.name||"첨부")+'"><figcaption>'+esc(x.name||"")+'</figcaption></figure>':""}).join("");if(im)h+='<section class="tfatt"><h2>첨부 자료</h2>'+im+'</section>'}
  return h+'</article>'}
var css=[".tfdoc{max-width:760px;margin:0 auto;font-family:\"NanumGothic\",\"Malgun Gothic\",sans-serif;color:#111;background:#fff;padding:28px 24px;line-height:1.55}",
".tfdoc h1{text-align:center;font-size:1.7em;letter-spacing:.3em;margin:4px 0 6px}.tfsch{text-align:center;color:#555;margin-bottom:14px}",
".tft{width:100%;border-collapse:collapse;font-size:.95em}.tft th,.tft td{border:1px solid #333;padding:8px 10px;vertical-align:top;text-align:left}.tft th{background:#f1f3f1;white-space:nowrap;width:1%;font-weight:700}.tft td{min-width:5.5em;word-break:keep-all;overflow-wrap:anywhere}.tft td.tfa{min-height:80px;height:80px}",
".tfok{text-align:center;margin:22px 0 6px;font-weight:700}.tfdate{text-align:center;margin:0 0 14px}",
".tfsigs{display:flex;justify-content:flex-end;gap:18px;flex-wrap:wrap}.tfsigs>div{display:flex;align-items:center;gap:8px}.tfsigs span{color:#555}.tfsig{width:150px;height:60px;border-bottom:1px solid #999}.tfnosig{color:#c0392b}",
".tfto{text-align:center;font-size:1.2em;font-weight:700;margin-top:22px;letter-spacing:.1em}",
"@media (max-width:560px){.tfdoc{padding:16px 8px;font-size:.92em}.tft th,.tft td{padding:6px 6px}.tft td{min-width:4em}.tft th{white-space:normal;word-break:keep-all}}",
".tfatt{margin-top:26px;page-break-before:always}.tfatt h2{font-size:1.1em;border-bottom:2px solid #333;padding-bottom:4px}.tfatt figure{margin:12px 0}.tfatt img{max-width:100%;border:1px solid #ccc}.tfatt figcaption{font-size:.85em;color:#555}"].join("\n");
window.TLF={FORMS:FORMS,REL:REL,days:days,wdays:wdays,kday:kday,sigSVG:sigSVG,docHTML:docHTML,css:css,esc:esc};
})();
