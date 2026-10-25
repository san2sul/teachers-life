/* 교사의 생활 — 학교 서류 양식(배경 그림 + 입력칸 · 서명란 · ○ 표시) 채워 그리기. 앱(index.html)이 필요할 때 불러옵니다. */
(function(){"use strict";
var esc=function(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]})};
var WD="일월화수목금토";
function pd(s){var m=/^(\d{4})-(\d{2})-(\d{2})/.exec(s||"");if(!m)return null;var d=new Date(+m[1],+m[2]-1,+m[3]);return{Y:String(+m[1]),YY:m[1].slice(2),M:String(+m[2]),D:String(+m[3]),W:WD[d.getDay()],md:(+m[2])+"."+(+m[3])}}
function pt(s){var m=/^(\d{1,2}):(\d{2})/.exec(s||"");return m?{H:String(+m[1]),M:m[2]}:null}
/* 학년 · 반 · 번: "1학년 2반" + 학번 10203 → 1, 2, 3 */
function gcn(cls,no){var g="",c="",n="";var m=/(\d+)\s*학년\s*(\d+)\s*반/.exec(cls||"");if(m){g=m[1];c=m[2]}else{m=/(\d+)\s*[-–]\s*(\d+)/.exec(cls||"");if(m){g=m[1];c=m[2]}}
  var x=String(no||"").replace(/\D/g,"");if(/^\d{5}$/.test(x)){if(!g)g=String(+x[0]);if(!c)c=String(+x.slice(1,3));n=String(+x.slice(3))}else if(/^\d{4}$/.test(x)){if(!g)g=x[0];if(!c)c=String(+x[1]);n=String(+x.slice(2))}else if(x)n=String(+x);return{g:g,c:c,n:n}}
function days(a,b){var x=pd(a),y=pd(b);if(!x||!y)return 0;var n=Math.round((new Date(b.slice(0,10)+"T00:00")-new Date(a.slice(0,10)+"T00:00"))/864e5)+1;return n>0?n:0}
function wdays(a,b){var n=days(a,b),c=0;if(!n||n>400)return n;var x=new Date(a.slice(0,10)+"T00:00");for(var i=0;i<n;i++){var w=x.getDay();if(w>0&&w<6)c++;x.setDate(x.getDate()+1)}return c}
/* 칸에 넣을 수 있는 값 목록 (편집기 단추) */
function fields(t){var F=(window.TLF&&window.TLF.FORMS[t])||{f:[]},G=[];
  G.push({g:"학생",L:[["name","이름"],["g","학년"],["c","반"],["n","번"],["gcn","1학년 1반 1번"],["sid","학번"],["cls","학년 · 반"]]});
  G.push({g:"보호자",L:[["pname","보호자 이름"],["prel","관계"],["ptel","보호자 전화"]]});
  G.push({g:"서명",sig:1,L:[["sigS","✍ 학생 서명"],["sigP","✍ 보호자 서명"]]});
  G.push({g:"작성한 날",L:[["at.Y","연"],["at.YY","연 (뒤 2자리)"],["at.M","월"],["at.D","일"],["at.full","날짜 전체"]]});
  var dl=F.f.filter(function(f){return f.type==="date"});
  dl.forEach(function(f){G.push({g:f.l.replace(/\s*\(.*\)$/,""),L:[[f.k+".Y","연"],[f.k+".YY","연 (뒤 2자리)"],[f.k+".M","월"],[f.k+".D","일"],[f.k+".W","요일"],[f.k+".md","월.일"]]})});
  if(dl.some(function(f){return f.k==="from"}))G.push({g:"기간",L:[["days","일수"],["wdays","평일 일수"],["period","기간 전체"]]});
  var tl=F.f.filter(function(f){return f.type==="time"});if(tl.length)G.push({g:"시각",L:[].concat.apply([],tl.map(function(f){return[[f.k+".H",f.l.replace(/^.*: /,"")+" 시"],[f.k+".M",f.l.replace(/^.*: /,"")+" 분"],[f.k,f.l.replace(/^.*: /,"")]]}))});
  G.push({g:"서류 내용",L:F.f.filter(function(f){return f.type!=="date"&&f.type!=="time"}).map(function(f){return[f.k,(f.type==="chk"?"✓ ":"")+short(f.l)]}).concat(t==="report"?[["_body","본문 (내용 + 느낀 점, 넘치면 별지로)"]]:[]).concat([["sch","학교 이름"],["schS","학교 이름 (끝의 ‘학교’ 빼고)"]])});
  var mk=[];F.f.forEach(function(f){if(f.type==="select")f.o.forEach(function(o){mk.push([f.k,o,short(f.l)+": "+o])});if(f.type==="chk")mk.push([f.k,"1",short(f.l)])});
  if(mk.length)G.push({g:"○ 표시 (고른 것에)",mark:1,L:mk});
  G.push({g:"그 밖",L:[["_white","⬜ 흰 가리개"],["_cont","별지: 이어 쓰기"],["_photo","별지: 사진 자리"]]});
  return G}
function short(l){l=String(l||"");return l.length>18?l.slice(0,17)+"…":l}
function label(t,it){if(it.k==="_white")return"가리개";var G=fields(t);for(var i=0;i<G.length;i++)for(var j=0;j<G[i].L.length;j++){var x=G[i].L[j];if(G[i].mark){if(it.ty==="m"&&x[0]===it.k&&x[1]===it.v)return"○ "+x[2]}else if(x[0]===it.k&&it.ty!=="m")return(G[i].g.length<8&&!/학생|보호자|서류|서명|그 밖/.test(G[i].g)?G[i].g+" ":"")+x[1]}return it.k}
/* 값 */
function ctx(rq,s){var d=s.d||{},cls=d.cls||rq.cls||"";return{rq:rq,s:s,d:d,cls:cls,gcn:gcn(cls,s.no||d.no)}}
function val(k,C){var d=C.d,s=C.s,F=(window.TLF&&window.TLF.FORMS[C.rq.t])||{f:[]};
  switch(k){case"name":return s.nm||d.nm||"";case"g":return C.gcn.g;case"c":return C.gcn.c;case"n":return C.gcn.n;
    case"gcn":return(C.gcn.g?C.gcn.g+"학년 ":"")+(C.gcn.c?C.gcn.c+"반 ":"")+(C.gcn.n?C.gcn.n+"번":"");case"sid":return s.no||d.no||"";case"cls":return C.cls;
    case"_body":return[d.content||"",d.feel?"[느낀 점 · 배운 점] "+d.feel:""].filter(Boolean).join("\n");case"pname":return d.pname||"";case"prel":return d.prel||"";case"ptel":return d.ptel||"";case"sch":return C.rq.sch||"";case"schS":return String(C.rq.sch||"").replace(/\s*학교$/,"");
    case"days":return d.from&&d.to?String(days(d.from,d.to)):"";case"wdays":return d.from&&d.to?String(wdays(d.from,d.to)):"";
    case"period":{var a=pd(d.from),b=pd(d.to);if(!a)return"";return a.Y+"년 "+a.M+"월 "+a.D+"일("+a.W+")"+(b&&d.to!==d.from?" ~ "+(b.Y!==a.Y?b.Y+"년 ":"")+b.M+"월 "+b.D+"일("+b.W+")":"")}}
  var m=/^(.+)\.(Y|YY|M|D|W|md|full|H)$/.exec(k);
  if(m){if(m[1]==="at"){var x=pd((s.at||"").slice(0,10));if(!x)return"";return m[2]==="full"?x.Y+"년 "+x.M+"월 "+x.D+"일":x[m[2]]}
    var f=F.f.find(function(y){return y.k===m[1]});if(f&&f.type==="time"){var q=pt(d[m[1]]);return q?q[m[2]==="M"?"M":"H"]||"":""}
    var z=pd(d[m[1]]);return z?z[m[2]]||"":""}
  var f2=F.f.find(function(y){return y.k===k});if(f2&&f2.type==="chk")return d[k]?"✓":"";
  return d[k]==null?"":String(d[k])}
/* 배경 위 칸 그리기. tp={w,h,items}, 단위: 가로 1000 */
function sigSVG(sg){if(!sg||!Array.isArray(sg.p)||!sg.p.length)return"";var W=+sg.w||600,H=+sg.h||240,xs=[],ys=[];sg.p.forEach(function(a){(a||[]).forEach(function(p){xs.push(+p[0]||0);ys.push(+p[1]||0)})});
  var x0=Math.max(0,Math.min.apply(null,xs)-10),y0=Math.max(0,Math.min.apply(null,ys)-10),x1=Math.min(W,Math.max.apply(null,xs)+10),y1=Math.min(H,Math.max.apply(null,ys)+10);
  return'<svg viewBox="'+x0+" "+y0+" "+Math.max(20,x1-x0)+" "+Math.max(10,y1-y0)+'" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg"><path d="'+sg.p.map(function(a){return(a||[]).map(function(p,i){return(i?"L":"M")+(+p[0]||0)+" "+(+p[1]||0)}).join("")+((a||[]).length===1?"l0.1 0":"")}).join("")+'" fill="none" stroke="#111" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>'}
function box(it,H,inner,cls,st){return'<div class="tsi '+(cls||"")+'" style="left:'+(it.x/10)+'%;top:'+(it.y/H*100)+'%;width:'+(it.w/10)+'%;height:'+(it.h/H*100)+'%;'+(st||"")+'">'+inner+'</div>'}
function pageHTML(tp,bg,C,o){o=o||{};var H=1000*tp.h/tp.w,out=[];
  (tp.items||[]).forEach(function(it,i){var fs="font-size:"+((it.fs||12)/10)+"cqw;";
    if(it.ty==="w"){out.push(box(it,H,"","tsw"));return}
    if(it.ty==="s"){var sg=C.s.sg&&C.s.sg[it.k==="sigS"?"st":"pa"];out.push(box(it,H,o.sample?'<span class="tss">'+(it.k==="sigS"?"학생 서명":"보호자 서명")+'</span>':sigSVG(sg),"tsg"));return}
    if(it.ty==="m"){var on=o.sample?true:String(C.d[it.k]||"")===String(it.v)||(it.v==="1"&&!!C.d[it.k]);if(!on)return;out.push(box(it,H,it.mk==="v"?'<span style="'+fs+'">✓</span>':"",it.mk==="v"?"tsv":"tsm"));return}
    if(it.k==="_photo"){out.push(box(it,H,o.photos||"","tsph"));return}
    var v=it.k==="_cont"?(o.cont||""):o.sample?sample(it.k,C):val(it.k,C);if(it.ty==="a"||it.k==="_cont")out.push(box(it,H,'<div class="tsa" data-k="'+esc(it.k)+'" data-fs="'+(it.fs||12)+'"'+(it.lh?' data-lh="'+it.lh+'"':"")+' style="'+fs+(it.lh?"line-height:"+(it.lh/10)+"cqw;":"")+'">'+esc(v)+'</div>',"tst"));
    else out.push(box(it,H,'<span class="tsx" data-fs="'+(it.fs||12)+'" style="'+fs+'">'+esc(v)+'</span>',"tst al"+(it.al||"c")))});
  return'<section class="tsp" style="aspect-ratio:'+tp.w+"/"+tp.h+'">'+(bg?'<img class="tsbg" src="'+bg+'" alt="">':"")+out.join("")+'</section>'}
function sample(k,C){var S={name:"홍길동",g:"1",c:"2",n:"3",gcn:"1학년 2반 3번",sid:"10203",cls:"1학년 2반",pname:"홍보호",prel:"모",ptel:"010-1234-5678",sch:"○○학교",days:"3",wdays:"3",period:"2026년 11월 2일(월) ~ 11월 4일(수)"};
  if(S[k]!=null)return S[k];var m=/\.(Y|YY|M|D|W|md|full|H)$/.exec(k);if(m)return{Y:"2026",YY:"26",M:"11",D:"2",W:"월",md:"11.2",full:"2026년 11월 2일",H:"9"}[m[1]];if(/\.M$/.test(k))return"30";var v=val(k,C);return v||"("+short(label(C.rq.t,{k:k}))+")"}
/* 그린 뒤 넘치는 글자 줄이기 · 이어 쓰기 나누기 (화면에 붙인 뒤 부름) */
function fit(root){root.querySelectorAll(".tsx").forEach(function(el){var p=el.parentNode,fs=+el.dataset.fs,n=0;el.style.fontSize=(fs/10)+"cqw";while(el.scrollWidth>p.clientWidth+1&&n<30&&fs>3){fs*=.92;el.style.fontSize=(fs/10)+"cqw";n++}});
  root.querySelectorAll(".tsa").forEach(function(el){if(el.dataset.lh)return;var p=el.parentNode,fs=+el.dataset.fs,n=0;while(el.scrollHeight>p.clientHeight+1&&n<30&&fs>3){fs*=.92;el.style.fontSize=(fs/10)+"cqw";n++}})}
/* 줄 칸(이어 쓰기) 하나에 들어가는 만큼만 남기고 나머지를 돌려줌 */
function cut(el,text){var p=el.parentNode;el.textContent=text;if(el.scrollHeight<=p.clientHeight+1)return"";var lo=0,hi=text.length;while(lo<hi){var mid=(lo+hi+1)>>1;el.textContent=text.slice(0,mid);if(el.scrollHeight<=p.clientHeight+1)lo=mid;else hi=mid-1}
  var k=lo,sp=text.lastIndexOf(" ",lo),nl=text.lastIndexOf("\n",lo);var b=Math.max(sp,nl);if(b>lo-12&&b>0)k=b;el.textContent=text.slice(0,k);return text.slice(k).replace(/^[ \n]/,"")}
/* 서류 전체: main 양식 + (있으면) 별지 양식으로 이어 쓰기 · 사진 */
function render(root,o){var C=ctx(o.rq,o.s),parts=[],main=o.main,att=o.att;root.innerHTML='<style>'+css+'</style>';
  var add=function(tp,bg,po){var w=document.createElement("div");w.innerHTML=pageHTML(tp,bg,C,po);var pg=w.firstChild;root.appendChild(pg);parts.push(pg);return pg};
  var p1=add(main,o.mainBg,{sample:o.sample});fit(p1);
  var rest="";if(!o.sample)p1.querySelectorAll(".tst .tsa[data-lh]").forEach(function(el){if(el.dataset.k==="_cont")return;var t=val(el.dataset.k,C);var r=cut(el,t);if(r)rest+=(rest?"\n":"")+r});
  var imgs=(o.imgs||[]),i=0;
  if(att){while(rest){var pg=add(att,o.attBg,{cont:" "});fit(pg);var el=pg.querySelector(".tsa");if(!el){break}var r2=cut(el,rest);if(r2.length>=rest.length)break;rest=r2}
    var hasPh=(att.items||[]).some(function(x){return x.k==="_photo"});
    while(i<imgs.length){var two=imgs.slice(i,i+2);i+=2;var ph=two.map(function(x){return'<figure><img src="'+x.u+'" alt=""><figcaption>'+esc(x.n||"")+'</figcaption></figure>'}).join("");
      if(hasPh){var g=add(att,o.attBg,{photos:ph});fit(g);g.querySelectorAll(".tsa").forEach(function(e){e.textContent=""})}else plain(ph)}}
  else while(i<imgs.length){plain('<figure><img src="'+imgs[i].u+'" alt=""><figcaption>'+esc(imgs[i].n||"")+'</figcaption></figure>');i++}
  function plain(ph){var w=document.createElement("div");w.innerHTML='<section class="tsp tsplain" style="aspect-ratio:210/297"><h3>붙임 · 증빙 자료</h3><div class="tsph">'+ph+'</div></section>';root.appendChild(w.firstChild)}
  if(rest&&!att){var w=document.createElement("div");w.innerHTML='<section class="tsp tsplain" style="aspect-ratio:210/297"><h3>이어서</h3><div class="tsrest"></div></section>';root.appendChild(w.firstChild);root.lastChild.querySelector(".tsrest").textContent=rest}
  return root}
var css=[".tss,.tsx,.tsa{font-family:\"NanumGothic\",\"Malgun Gothic\",sans-serif;color:#000}",
".tsp{position:relative;width:100%;max-width:794px;margin:0 auto 14px;background:#fff;container-type:inline-size;overflow:hidden;box-shadow:0 1px 6px rgba(0,0,0,.18);-webkit-print-color-adjust:exact;print-color-adjust:exact}",
".tsbg{position:absolute;inset:0;width:100%;height:100%;display:block;user-select:none;pointer-events:none}",
".tsi{position:absolute;box-sizing:border-box}.tst{display:flex;align-items:center;overflow:hidden}.tst.alc{justify-content:center}.tst.all{justify-content:flex-start}.tst.alr{justify-content:flex-end}",
".tsx{white-space:nowrap;line-height:1}.tsa{white-space:pre-wrap;word-break:keep-all;overflow-wrap:anywhere;line-height:1.35;align-self:flex-start;width:100%;max-height:100%}",
".tsw{background:#fff}.tsm{border:.18cqw solid #000;border-radius:50%}.tsv{display:flex;align-items:center;justify-content:center;font-weight:700}",
".tsg{display:flex;align-items:center;justify-content:center}.tsg svg{width:100%;height:100%}.tss{font-size:1.4cqw;color:#c0392b}",
".tsph{background:#fff;display:flex;flex-direction:column;gap:2%;padding:1%;box-sizing:border-box}.tsph figure{flex:1;margin:0;display:flex;flex-direction:column;min-height:0;align-items:center}.tsph img{flex:1;min-height:0;max-width:100%;object-fit:contain}.tsph figcaption{font-size:1.6cqw}",
".tsplain{padding:6%;box-sizing:border-box}.tsplain h3{font-size:2.4cqw;margin:0 0 2%}.tsplain .tsph{position:absolute;inset:10% 6% 5% 6%}.tsrest{white-space:pre-wrap;font-size:2cqw;line-height:1.7}",
"@page tsheet{size:A4;margin:0}",
"@media print{.tsp{page:tsheet;box-shadow:none;margin:0;max-width:none;width:210mm;break-after:page;page-break-after:always}.tsp:last-child{break-after:auto}}"].join("\n");
/* 기본 제공: 갈매고등학교 양식 (보내 주신 PDF, A4 595×841pt 기준 좌표) */
var PT=1000/595;
function P(w,h,list){return{w:w,h:h,items:list.map(function(a){var it={ty:a[0],k:a[1],x:a[2]*PT,y:a[3]*PT,w:(a[4]-a[2])*PT,h:(a[5]-a[3])*PT};var o=a[6]||{};if(o.fs)it.fs=o.fs*PT;else if(it.ty==="t"||it.ty==="a")it.fs=10*PT;if(o.al)it.al=o.al;if(o.v!=null)it.v=o.v;if(o.mk)it.mk=o.mk;if(o.lh)it.lh=o.lh*PT;return it})}}
var GALMAE={name:"갈매고등학교",pages:{
 absence:{main:P(1653,2337,[
   ["m","kind",77,97,115,118,{v:"질병"}],["m","kind",138,97,210,118,{v:"출석인정"}],
   ["m","ak",247,97,285,118,{v:"결석"}],["m","ak",308,97,345,118,{v:"조퇴"}],["m","ak",368,97,406,118,{v:"결과"}],["m","ak",429,97,466,118,{v:"지각"}],
   ["m","ak",185,222,207,238,{v:"결석"}],["m","ak",217,222,241,238,{v:"조퇴"}],["m","ak",252,222,276,238,{v:"결과"}],["m","ak",286,222,308,238,{v:"지각"}],
   ["t","g",328,140,354,166,{fs:11}],["t","c",378,140,395,166,{fs:11}],["t","n",409,140,431,166,{fs:11}],["t","name",337,171,446,198,{fs:12}],
   ["t","from.Y",158,244,191,267,{fs:10,al:"r"}],["t","from.M",209,244,231,267],["t","from.D",253,244,274,267],["t","from.W",294,244,305,267],
   ["w","_white",331,247,355.5,265],["t","to.Y",320,244,355.3,267,{fs:10,al:"r"}],["t","to.M",374,244,395,267],["t","to.D",416,244,437,267],["t","to.W",459,244,474,267],
   ["a","reason",164,272,492,298,{fs:10}],
   ["t","at.Y",210,324,248,342,{al:"r"}],["t","at.M",262,324,289,342],["t","at.D",303,324,334,342],
   ["t","name",358,357,424,373,{fs:11}],["s","sigS",420,348,500,382],["t","pname",358,377,424,393,{fs:11}],["s","sigP",420,368,500,402],
   ["a","pop",92,518,500,618,{fs:10.5}]])},
 trip:{main:P(1653,2337,[
   ["t","name",128,123,226,143,{fs:11}],["w","_white",229,124,364,142],["t","gcn",229,123,364,143,{fs:10}],["t","sph",418,123,526,143,{fs:10}],
   ["t","from.YY",235,145,249,159,{fs:9}],["t","from.M",260,145,274,159,{fs:9}],["t","from.D",285,145,299,159,{fs:9}],["t","to.M",327,145,341,159,{fs:9}],["t","to.D",352,145,371,159,{fs:9}],
   ["t","days",446,160,466,177,{fs:9}],
   ["t","t1.H",250,178,270,193,{fs:9}],["t","t1.M",282,178,300,193,{fs:9}],["t","t2.H",319,178,333,193,{fs:9}],["t","t2.M",344,178,358,193,{fs:9}],
   ["m","rule",447,199,463,215,{v:"1"}],
      ["m","type",179,222,196,242,{v:"가족 여행",mk:"v",fs:10}],["m","type",261,222,278,242,{v:"친인척 방문",mk:"v",fs:10}],["m","type",354,222,371,242,{v:"답사 · 견학 활동",mk:"v",fs:10}],["m","type",422,222,440,242,{v:"체험활동",mk:"v",fs:10}],
   ["t","place",129,244,324,262,{fs:9.5}],["t","stay",393,244,526,262,{fs:9}],
   ["t","pname",129,263,234,279,{fs:9.5}],["t","prel",258,263,325,279,{fs:9.5}],["t","ptel",358,263,526,279,{fs:9.5}],
   ["t","gname",129,280,234,295,{fs:9.5}],["t","grel",258,280,325,295,{fs:9.5}],["t","gtel",358,280,526,295,{fs:9.5}],
   ["a","purpose",130,297,525,315,{fs:9}],["a","plan",131,318,525,419,{fs:9.5}],
   ["m","safe",499,421,515,436,{v:"1",mk:"v",fs:11}],
   ["t","at.YY",259,465,276,479,{fs:9}],["t","at.M",286,465,301,479,{fs:9}],["t","at.D",312,465,327,479,{fs:9}],
   ["t","pname",452,470,500,483,{fs:9}],["s","sigP",478,462,532,490],["t","name",452,486,500,499,{fs:9}],["s","sigS",478,478,532,506]])},
 report:{main:P(1653,2337,[
   ["t","name",129,146,224,168,{fs:11}],["t","g",364,146,390,168],["t","c",411,146,437,168],["t","n",448,146,474,168],
   ["t","from.YY",273,171,288,190,{fs:9}],["t","from.M",299,171,314,190,{fs:9}],["t","from.D",325,171,340,190,{fs:9}],["t","to.M",375,171,390,190,{fs:9}],["t","to.D",402,171,422,190,{fs:9}],["t","days",441,171,467,190,{fs:9}],
   ["w","_white",388,193,470,208],["t","t1",388,193,424,208,{fs:9}],["t","t2",434,193,470,208,{fs:9}],
   ["m","type",186,262,205,285,{v:"가족 여행",mk:"v",fs:10}],["m","type",277,262,296,285,{v:"친인척 방문",mk:"v",fs:10}],["m","type",381,262,400,285,{v:"답사 · 견학 활동",mk:"v",fs:10}],["m","type",457,262,476,285,{v:"체험활동",mk:"v",fs:10}],
   ["t","place",227,218,530,238,{fs:10,al:"l"}],["t","comp",227,240,530,259,{fs:10,al:"l"}],["t","title",131,288,530,312,{fs:11,al:"l"}],
   ["a","_body",68,338,528,619,{fs:10.5,lh:21.55}],
   ["t","at.YY",261,643,281,657,{fs:9}],["t","at.M",287,643,312,657,{fs:9}],["t","at.D",317,643,342,657,{fs:9}],
   ["t","pname",457,657,505,670,{fs:9}],["s","sigP",483,650,537,678],["t","name",457,671,505,684,{fs:9}],["s","sigS",483,664,537,692]]),
  att:P(1653,2337,[["t","name",121,94,243,120,{fs:11}],["t","g",380,94,399,120],["t","c",421,94,447,120],["t","n",458,94,483,120],
   ["a","_cont",68,123,528,704,{fs:10.5,lh:22.43}],["t","_photo",64,123,531,703]])},
 consent:{main:P(1653,2337,[
   ["t","schS",174,179,276,221,{fs:11}],["t","g",318,179,360,221,{fs:12}],["t","c",392,179,430,221,{fs:12}],["t","n",450,179,486,221,{fs:12}],
   ["t","name",174,224,300,268,{fs:12}],["t","sph",389,224,530,268,{fs:11}],["t","pname",174,272,300,316,{fs:12}],["t","ptel",389,272,530,316,{fs:11}],
   ["w","_white",163,345,194.8,363],["t","yr",150,343,194.5,364,{fs:12,al:"r"}],["t","sem",254,343,266,364,{fs:11}],["t","cha",318,343,330,364,{fs:11}],
   ["t","os.md",94,374,125,393,{fs:9}],["t","oe.md",132,374,163,393,{fs:9}],
   ["w","_white",214,494,246.3,512],["t","at.Y",205,493,245.5,512,{fs:12,al:"r"}],["t","at.M",264,493,304,512,{fs:12}],["t","at.D",324,493,364,512,{fs:12}],
   ["t","name",236,562,360,583,{fs:12}],["s","sigS",344,552,436,593],["t","pname",236,597,360,618,{fs:12}],["s","sigP",344,587,436,628]])}}};
/* 사진 자리는 _photo 를 t 칸으로 적었으니 종류만 맞춤, 빈 칸(0 크기) 정리, 결과보고서 본문은 내용 + 느낀 점 */
Object.keys(GALMAE.pages).forEach(function(t){var pg=GALMAE.pages[t];["main","att"].forEach(function(k){if(pg[k])pg[k].items=pg[k].items.filter(function(it){return it.w>0&&it.h>0})})});
window.TLS={fields:fields,label:label,val:val,ctx:ctx,gcn:gcn,render:render,fit:fit,pageHTML:pageHTML,css:css,GALMAE:GALMAE};
})();
