/* 교사의 생활 — 글 보여 주기(웹 공유 페이지 · 발표 · 인쇄 · 파일 내보내기)에 쓰는 그리기 도구. 앱(index.html)과 view.html이 함께 씁니다. */
(function(){"use strict";
var esc=function(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]})};
var SH="0 1px 3px rgba(0,0,0,.45)";
/* 허용한 꾸밈만 남기기 (링크로 받은 글은 믿지 않음) */
function san(html){var t=document.createElement("template");t.innerHTML=String(html||"");var out=document.createElement("div");
  var okCol=function(v){return/^(#[0-9a-f]{3,8}|rgba?\(\s*[\d.]+\s*,\s*[\d.]+\s*,\s*[\d.]+\s*(,\s*[\d.]+\s*)?\))$/i.test(String(v||"").trim())};
  var TAG={B:"b",STRONG:"b",I:"i",EM:"i",U:"u",S:"s",STRIKE:"s",DEL:"s",SUB:"sub",SUP:"sup"};
  var walk=function(src,dst){Array.prototype.slice.call(src.childNodes).forEach(function(n){if(n.nodeType===3){dst.appendChild(document.createTextNode(n.nodeValue));return}if(n.nodeType!==1)return;var tg=n.tagName;
    if(tg==="BR"){dst.appendChild(document.createElement("br"));return}
    if(n.classList.contains("wmath")&&n.hasAttribute("data-tex")){var m=document.createElement("span");m.className="wmath";m.setAttribute("data-tex",String(n.getAttribute("data-tex")).slice(0,2000));dst.appendChild(m);return}
    if(/^(SCRIPT|STYLE|TEMPLATE|IFRAME|OBJECT|EMBED|SVG|svg|MATH|IMG|VIDEO|AUDIO|TABLE|FORM|INPUT|BUTTON)$/.test(tg))return;
    var outer=null,inner=null;var push=function(e){if(!outer){outer=inner=e}else{inner.appendChild(e);inner=e}};
    if(TAG[tg])push(document.createElement(TAG[tg]));
    if(tg==="A"){var h=String(n.getAttribute("href")||"").trim();if(/^(https?:|mailto:|tel:)/i.test(h)){var a=document.createElement("a");a.setAttribute("href",h.slice(0,2000));a.setAttribute("target","_blank");a.setAttribute("rel","noopener noreferrer");push(a)}}
    var st=n.style||{},css=[];var c=tg==="FONT"?n.getAttribute("color"):st.color,bg=st.backgroundColor,sh=st.textShadow;
    if(c&&okCol(c))css.push("color:"+c);if(bg&&okCol(bg))css.push("background-color:"+bg);if(sh&&sh!=="none")css.push("text-shadow:"+SH);
    if(/^(0\.8|0\.9|1\.2|1\.5|2)em$/.test(st.fontSize||""))css.push("font-size:"+st.fontSize);if(/^(-0\.05|0\.05|0\.1|0\.2)em$/.test(st.letterSpacing||""))css.push("letter-spacing:"+st.letterSpacing);
    var ff=String(st.fontFamily||"").replace(/["']/g,"");if(/^(serif|monospace)$/.test(ff))css.push("font-family:"+ff);
    if(css.length){var sp=document.createElement("span");sp.setAttribute("style",css.join(";"));push(sp)}
    if((tg==="DIV"||tg==="P"||tg==="LI")&&dst.childNodes.length&&dst.lastChild.nodeName!=="BR")dst.appendChild(document.createElement("br"));
    if(outer){walk(n,inner);if(outer.textContent||outer.querySelector("br,.wmath"))dst.appendChild(outer)}else walk(n,dst)})};
  walk(t.content,out);return out.innerHTML}
var okC=function(c,d){return/^#[0-9a-f]{3,8}$/i.test(String(c||""))?c:d};
var num=function(v,d){v=+v;return isFinite(v)?Math.round(v*10)/10:d};
function head(x1,y1,x2,y2,w){var a=Math.atan2(y2-y1,x2-x1),L=Math.max(16,w*4),s=Math.PI/7;return x2+","+y2+" "+(x2-L*Math.cos(a-s))+","+(y2-L*Math.sin(a-s))+" "+(x2-L*Math.cos(a+s))+","+(y2-L*Math.sin(a+s))}
function svgItem(it){var c=okC(it.c,"#1d2621"),w=num(it.w,6),f=it.f?okC(it.f,"none"):"none",s="";
  if(it.k==="pen"){var d=(it.pts||[]).map(function(p,j){return(j?"L":"M")+num(p[0],0)+" "+num(p[1],0)}).join("");s='<path d="'+d+'" fill="none" stroke="'+c+'" stroke-width="'+w+'" stroke-linecap="round" stroke-linejoin="round"/>'}
  else if(it.k==="line"||it.k==="arrow"){var x1=num(it.x1,0),y1=num(it.y1,0),x2=num(it.x2,0),y2=num(it.y2,0);s='<line x1="'+x1+'" y1="'+y1+'" x2="'+x2+'" y2="'+y2+'" stroke="'+c+'" stroke-width="'+w+'" stroke-linecap="round"/>'+(it.k==="arrow"?'<polygon points="'+head(x1,y1,x2,y2,w)+'" fill="'+c+'"/>':"")}
  else if(it.k==="rect")s='<rect x="'+num(it.x,0)+'" y="'+num(it.y,0)+'" width="'+num(it.w2,0)+'" height="'+num(it.h,0)+'" rx="6" fill="'+f+'" stroke="'+c+'" stroke-width="'+w+'"/>';
  else if(it.k==="ell")s='<ellipse cx="'+(num(it.x,0)+num(it.w2,0)/2)+'" cy="'+(num(it.y,0)+num(it.h,0)/2)+'" rx="'+Math.abs(num(it.w2,0)/2)+'" ry="'+Math.abs(num(it.h,0)/2)+'" fill="'+f+'" stroke="'+c+'" stroke-width="'+w+'"/>';
  else if(it.k==="text"||it.k==="note"){var nt=it.k==="note",bg=nt?okC(it.f,"#fff3a3"):(it.f?f:"");
    s='<foreignObject x="'+num(it.x,0)+'" y="'+num(it.y,0)+'" width="'+num(it.w2,200)+'" height="'+Math.max(num(it.h,40),20)+'"><div xmlns="http://www.w3.org/1999/xhtml" class="wdtx'+(nt?" wnote":"")+'" style="font-size:'+num(it.fs,34)+'px;color:'+c+';'+(bg?"background:"+bg+";":"")+(it.b?"border:2px solid "+okC(it.b,"#1d2621")+";":"")+(nt?"min-height:"+Math.max(num(it.h,40),20)+"px;":"")+'">'+esc(it.t||"")+'</div></foreignObject>'}
  return'<g class="wdi">'+s+'</g>'}
function drawSVG(b){var h=num(b.h,500);return'<svg class="wvsvg" viewBox="0 0 1000 '+h+'" preserveAspectRatio="xMidYMin meet" style="aspect-ratio:1000/'+h+'" xmlns="http://www.w3.org/2000/svg">'+(b.items||[]).map(svgItem).join("")+'</svg>'}
function txt(b){return b.h?san(b.h):esc(b.x||"").replace(/\n/g,"<br>")}
function bstyle(s){s=s||{};var o=[];if(s.lh)o.push("line-height:"+num(s.lh,1.6));if(s.al&&/^(left|center|right|justify)$/.test(s.al))o.push("text-align:"+s.al);if(s.fs)o.push("font-size:"+num(s.fs,1)+"em");
  if(/^(serif|monospace)$/.test(s.ff||""))o.push("font-family:"+s.ff);if(s.fi)o.push("text-indent:"+num(s.fi,0)+"em");if(/^-?0?\.\d+em$/.test(s.ls||""))o.push("letter-spacing:"+s.ls);
  if(s.sb!=null)o.push("margin-top:"+num(s.sb,0)+"px");if(s.sa!=null)o.push("margin-bottom:"+num(s.sa,0)+"px");if(s.ind)o.push("margin-left:"+(num(s.ind,0)*1.5)+"em");return o.length?' style="'+o.join(";")+'"':""}
var KL={stu:"학생 기록",meet:"회의 기록",day:"일상 기록",free:"자유 글",lesson:"수업자료",board:"화이트보드",notes:"포스트잇",survey:"설문"};
function when(at){var m=/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})/.exec(at||"");return m?(+m[1])+"년 "+(+m[2])+"월 "+(+m[3])+"일 "+m[4]+":"+m[5]:""}
function blocksHTML(L,o){o=o||{};var out=[],i=0;
  while(i<L.length){var b=L[i];
    if(b.t==="pi"){var ps=[],PC=["#fff3a8","#ffd6e0","#d6e8fb","#d9f2d0","#ffe0b8","#e7dcf7"];while(i<L.length&&L[i].t==="pi"){var c=PC.indexOf(L[i].pc)>=0?L[i].pc:PC[0];ps.push("<div class=\"wvpi\" style=\"background:"+c+"\">"+(txt(L[i])||"&nbsp;")+"</div>");i++}out.push("<div class=\"wvpis\">"+ps.join("")+"</div>");continue}
    if(b.t==="ul"||b.t==="ol"){var tg=b.t,items=[];while(i<L.length&&L[i].t===tg){items.push("<li"+bstyle(L[i].s)+">"+txt(L[i])+"</li>");i++}out.push("<"+tg+">"+items.join("")+"</"+tg+">");continue}
    var st=bstyle(b.s);
    if(b.t==="h1")out.push("<h2 class=\"wvh1\""+st+">"+txt(b)+"</h2>");
    else if(b.t==="h2")out.push("<h3 class=\"wvh2\""+st+">"+txt(b)+"</h3>");
    else if(b.t==="todo")out.push("<div class=\"wvtodo"+(b.c?" done":"")+"\""+st+"><span>"+(b.c?"☑":"☐")+"</span><span>"+txt(b)+"</span></div>");
    else if(b.t==="quote")out.push("<blockquote"+st+">"+txt(b)+"</blockquote>");
    else if(b.t==="call")out.push("<div class=\"wvcall\""+st+"><span>💡</span><div>"+txt(b)+"</div></div>");
    else if(b.t==="hr")out.push("<hr>");
    else if(b.t==="math")out.push("<div class=\"wmathb\" data-tex=\""+esc(b.tex||"")+"\"></div>");
    else if(b.t==="bm"){var u=String(b.u||"");if(!/^https?:\/\//i.test(u))u="";var hst="";try{hst=new URL(u).hostname.replace(/^www\./,"")}catch(e){}out.push((u?"<a class=\"wvbm\" href=\""+esc(u)+"\" target=\"_blank\" rel=\"noopener noreferrer\">":"<div class=\"wvbm\">")+"<span class=\"wvbmi\">🔗</span><span class=\"wvbmt\"><b>"+esc(b.ti||hst||u||"링크")+"</b><small>"+esc(hst||u)+"</small>"+(b.n?"<i>"+esc(b.n)+"</i>":"")+"</span>"+(u?"</a>":"</div>"))}
    else if(b.t==="table"){var bc=okC(b.bc,"");out.push("<div class=\"wvtw\"><table class=\"wvtbl\""+(bc?" style=\"--wtb:"+bc+"\"":"")+">"+(b.rows||[]).map(function(rw,ri){return"<tr>"+rw.map(function(cv,ci){var hd=(b.hd&&ri===0)||(b.hc&&ci===0),g=(b.bg||{})[ri+","+ci];return"<"+(hd?"th":"td")+(okC(g,"")?" style=\"background:"+g+"\"":"")+">"+esc(cv)+"</"+(hd?"th":"td")+">"}).join("")+"</tr>"}).join("")+"</table></div>")}
    else if(b.t==="img"){var al=(b.s||{}).al;out.push("<figure class=\"wvfig\" style=\"width:"+(num(b.w,100))+"%;"+(al==="left"?"margin-left:0;":al==="right"?"margin-right:0;":"")+"\"><img alt=\""+esc(b.cap||"그림")+"\""+(b.src&&/^data:image\//.test(b.src)?" src=\""+b.src+"\"":"")+(b.m?" data-wimg=\""+esc(b.m)+"\"":"")+">"+(b.cap?"<figcaption>"+esc(b.cap)+"</figcaption>":"")+"</figure>")}
    else if(b.t==="draw")out.push("<div class=\"wvdraw\">"+(o.drawPng&&o.drawPng[b.id]?"<img src=\""+o.drawPng[b.id]+"\" alt=\"그림\">":drawSVG(b))+"</div>");
    else out.push("<p class=\"wvp\""+st+">"+(txt(b)||"&nbsp;")+"</p>");
    i++}
  return out.join("\n")}
function render(r,o){o=o||{};var st=r.st||{},h=[];
  var title=r.k==="stu"?((r.stus||[]).filter(function(s){return s.name||s.sid}).map(function(s){return s.name||s.sid}).join(", ")||"학생 기록"):r.k==="meet"?((r.meet&&r.meet.name)||"회의 기록"):(r.title||o.title||KL[r.k]||"글");
  if(o.head!==false){h.push("<header class=\"wvhd\"><div class=\"wvk\">"+esc(KL[r.k]||"글")+"</div><h1>"+esc(title)+"</h1>");var meta=[];if(r.at)meta.push(when(r.at));if(r.place)meta.push("장소: "+esc(r.place));
    if(r.k==="meet"&&r.meet){var who=(r.meet.who||[]).join(", ");if(r.meet.cnt||who)meta.push("참석: "+esc([r.meet.cnt?r.meet.cnt+"명":"",who].filter(Boolean).join(" · ")))}
    if(r.k==="stu"&&o.private!==true)(r.stus||[]).filter(function(s){return s.name||s.sid}).forEach(function(s){meta.push("학생: "+esc([s.sid,s.name].filter(Boolean).join(" ")))});
    if(meta.length)h.push("<div class=\"wvmeta\">"+meta.join(" · ")+"</div>");h.push("</header>")}
  if(Array.isArray(r.cols)&&Array.isArray(r.notes)){h.push("<div class=\"wvnotes\">"+r.cols.map(function(c){return"<section><h3>"+esc(c.t)+"</h3>"+r.notes.filter(function(n){return n.col===c.id}).map(function(n){return"<div class=\"wvnote\" style=\"background:"+okC(n.c,"#fff3a3")+"\">"+esc(n.t)+"</div>"}).join("")+"</section>"}).join("")+"</div>")}
  h.push("<div class=\"wvbody\" style=\"--wlh:"+num(st.lh,1.6)+";--wpg:"+(st.pg!=null?num(st.pg,2):2)+"px;--wfs:"+num(st.fs,1)+";"+(/^(serif|monospace)$/.test(st.ff||"")?"font-family:"+st.ff+";":"")+"\">"+blocksHTML(r.blocks||[],o)+"</div>");
  return h.join("\n")}
/* 발표 쪽 나누기: 구분선(―) 또는 큰 제목(H1)마다 */
function slides(blocks,mode){var L=[],cur=[];(blocks||[]).forEach(function(b){if(b.t==="hr"){if(cur.length)L.push(cur);cur=[];return}if(mode!=="hr"&&b.t==="h1"&&cur.length){L.push(cur);cur=[]}cur.push(b)});if(cur.length)L.push(cur);return L.length?L:[[]]}
function paintMath(root,k){k=k||window.katex;var L=root.querySelectorAll(".wmath[data-tex],.wmathb[data-tex]");if(!L.length)return;
  for(var i=0;i<L.length;i++){var el=L[i];if(!k){el.textContent="$"+el.getAttribute("data-tex")+"$";continue}try{k.render(el.getAttribute("data-tex")||"",el,{throwOnError:false,displayMode:el.classList.contains("wmathb"),output:"html",strict:"ignore"})}catch(e){el.textContent=el.getAttribute("data-tex")}}}
var css=[
".wv{font-family:\"NanumGothic\",system-ui,-apple-system,sans-serif;color:#1d2621;line-height:1.6;word-break:keep-all;overflow-wrap:anywhere}",
".wvhd{margin:0 0 18px;padding-bottom:12px;border-bottom:2px solid #24476b}.wvhd h1{font-size:1.6em;margin:2px 0 6px;line-height:1.3}.wvk{font-size:.8em;font-weight:700;color:#24476b}.wvmeta{font-size:.85em;color:#5b665f}",
".wvbody{font-size:calc(1em * var(--wfs,1))}.wvbody>*{margin:0 0 var(--wpg,2px)}.wvbody p,.wvbody li,.wvbody blockquote,.wvtodo,.wvcall{line-height:var(--wlh,1.6)}",
".wvh1{font-size:1.4em;margin:18px 0 8px!important;line-height:1.3}.wvh2{font-size:1.15em;margin:14px 0 6px!important;line-height:1.35}",
".wvbody ul,.wvbody ol{padding-left:1.6em}.wvbody blockquote{border-left:4px solid #c9d1cb;margin-left:0;padding-left:12px;color:#5b665f}",
".wvtodo{display:flex;gap:8px}.wvtodo.done span:last-child{text-decoration:line-through;color:#8a8f8c}.wvcall{display:flex;gap:10px;background:#fff6d6;border-radius:10px;padding:10px 12px}",
".wvtw{overflow-x:auto;margin:10px 0}.wvtbl{--wtb:#c9d1cb;border-collapse:collapse;min-width:60%}.wvtbl td,.wvtbl th{border:1px solid var(--wtb);padding:6px 10px;vertical-align:top;white-space:pre-wrap;text-align:left}.wvtbl th{background:#eef1ee}",
".wvfig{margin:12px auto;max-width:100%}.wvfig img{width:100%;height:auto;border-radius:8px}.wvfig figcaption{text-align:center;font-size:.85em;color:#5b665f;margin-top:4px}",
".wvdraw{margin:10px 0;border:1px solid #e3e8e3;border-radius:10px;overflow:hidden;background:#fff}.wvdraw svg,.wvdraw img{display:block;width:100%;height:auto}",
".wdtx{white-space:pre-wrap;word-break:break-word;line-height:1.35;padding:6px 8px;border-radius:6px;font-family:inherit}.wnote{box-shadow:0 3px 8px rgba(0,0,0,.18);border-radius:4px;padding:10px 12px}foreignObject{overflow:visible}",
".wmathb{text-align:center;overflow-x:auto;padding:6px 0}.wv a{color:#1f6fb2}",
".wvpis{display:flex;flex-wrap:wrap;gap:12px;margin:10px 0}.wvpi{flex:0 1 200px;min-height:90px;padding:12px 14px;border-radius:4px;box-shadow:0 3px 8px rgba(0,0,0,.18);color:#1d2621;line-height:1.45;white-space:pre-wrap;transform:rotate(-.6deg)}.wvpi:nth-child(even){transform:rotate(.7deg)}",
".wvbm{display:flex;gap:10px;align-items:center;border:1px solid #dfe5e0;border-radius:12px;padding:10px 12px;margin:8px 0;text-decoration:none;color:inherit;background:#fbfcfb}.wvbmi{font-size:1.3em}.wvbmt{display:flex;flex-direction:column;min-width:0}.wvbmt b{color:#1f6fb2;overflow-wrap:anywhere}.wvbmt small{color:#5b665f;overflow-wrap:anywhere}.wvbmt i{font-style:normal;font-size:.9em;color:#3b4740}",
".wvbody sub,.wvbody sup{font-size:.72em;line-height:0}",
".wvnotes{display:flex;gap:12px;flex-wrap:wrap;align-items:flex-start}.wvnotes section{flex:1 1 220px;display:flex;flex-direction:column;gap:8px}.wvnotes h3{margin:0;font-size:1.05em}.wvnote{border-radius:6px;padding:10px 12px;white-space:pre-wrap;box-shadow:0 2px 6px rgba(0,0,0,.12)}"].join("\n");

/* 발표(전체 화면): 구분선 · 큰 제목마다 한 쪽, ◀ ▶ · 화살표 키 · 밀기로 넘김 */
function present(r,o){o=o||{};var S=slides(r.blocks,o.mode),i=Math.max(0,Math.min(S.length-1,o.start||0)),fs=1;try{fs=+localStorage.getItem("tl-pres-fs")||1}catch(e){}
  var ov=document.createElement("div");ov.className="wvpres";ov.setAttribute("role","dialog");ov.setAttribute("aria-label","발표");
  ov.innerHTML='<style>'+pcss+'</style><div class="wvps"><div class="wvpc wv"></div></div><div class="wvpbar"><button type="button" data-p="x" aria-label="발표 끝내기">✕</button><button type="button" data-p="fs-" aria-label="글자 작게">가−</button><button type="button" data-p="fs+" aria-label="글자 크게">가＋</button><button type="button" data-p="full" aria-label="전체 화면">⛶</button><span class="wvpn" aria-live="polite"></span><button type="button" data-p="prev" aria-label="이전 쪽">◀</button><button type="button" data-p="next" aria-label="다음 쪽">▶</button></div>';
  document.body.appendChild(ov);var c=ov.querySelector(".wvpc"),n=ov.querySelector(".wvpn"),sc=ov.querySelector(".wvps");
  function show(){ov.style.setProperty("--pf",fs);var head="";if(i===0&&o.title!==false){var t=document.createElement("div");t.innerHTML=render({k:r.k,title:r.title,at:"",blocks:[]},{title:o.titleText});var h1=t.querySelector("h1");if(h1&&h1.textContent)head='<div class="wvptitle">'+esc(h1.textContent)+'</div>'}
    c.innerHTML=head+blocksHTML(S[i],o);if(o.fillImg)o.fillImg(c);if(window.katex)paintMath(c);else if(o.loadMath)o.loadMath().then(function(){paintMath(c)}).catch(function(){paintMath(c,null)});n.textContent=(i+1)+" / "+S.length;sc.scrollTop=0;
    ov.querySelector("[data-p=prev]").disabled=i===0;ov.querySelector("[data-p=next]").disabled=i===S.length-1}
  function go(d){var j=Math.max(0,Math.min(S.length-1,i+d));if(j!==i){i=j;show()}}
  function close(){document.removeEventListener("keydown",key,true);try{if(document.fullscreenElement)document.exitFullscreen()}catch(e){}ov.remove();if(o.onClose)o.onClose()}
  function key(e){if(e.key==="ArrowRight"||e.key==="PageDown"||e.key===" "){e.preventDefault();go(1)}else if(e.key==="ArrowLeft"||e.key==="PageUp"){e.preventDefault();go(-1)}else if(e.key==="Home"){i=0;show()}else if(e.key==="End"){i=S.length-1;show()}else if(e.key==="Escape"){e.preventDefault();e.stopPropagation();close()}}
  document.addEventListener("keydown",key,true);ov._close=close;
  ov.querySelectorAll("[data-p]").forEach(function(b){b.onclick=function(){var p=b.dataset.p;if(p==="x")return close();if(p==="prev")return go(-1);if(p==="next")return go(1);
    if(p==="fs+"||p==="fs-"){fs=Math.max(.6,Math.min(2.4,Math.round((fs+(p==="fs+"?.15:-.15))*100)/100));try{localStorage.setItem("tl-pres-fs",fs)}catch(e){}return show()}
    if(p==="full"){try{if(document.fullscreenElement)document.exitFullscreen();else ov.requestFullscreen&&ov.requestFullscreen()}catch(e){}}}});
  var x0=null,y0=0;sc.addEventListener("pointerdown",function(e){x0=e.clientX;y0=e.clientY});sc.addEventListener("pointerup",function(e){if(x0==null)return;var dx=e.clientX-x0,dy=e.clientY-y0;x0=null;if(Math.abs(dx)>60&&Math.abs(dx)>Math.abs(dy)*1.5)go(dx<0?1:-1)});
  show();return{close:close,go:go}}
var pcss=[".wvpres{position:fixed;inset:0;z-index:300;background:#fff;color:#1d2621;display:flex;flex-direction:column}",
".wvps{flex:1;overflow:auto;padding:clamp(16px,4vw,56px);touch-action:pan-y}",
".wvpc{max-width:1100px;margin:0 auto;font-size:calc(var(--pf,1) * clamp(18px,2.4vw,38px));word-break:keep-all;overflow-wrap:anywhere}.wvpc img,.wvpc video,.wvpc svg{max-width:100%;height:auto}.wvpc pre{white-space:pre-wrap}",
".wvpc .wvh1{font-size:1.6em}.wvpc .wvh2{font-size:1.25em}.wvptitle{font-size:1.9em;font-weight:700;color:#24476b;margin:0 0 .5em;line-height:1.25}",
".wvpbar{display:flex;align-items:center;gap:6px;padding:8px 10px calc(8px + env(safe-area-inset-bottom,0px));border-top:1px solid #e3e8e3;background:#f6f8f6}",
".wvpbar button{min-width:46px;min-height:44px;border:1px solid #dde3de;border-radius:10px;background:#fff;color:#1d2621;font:inherit;font-size:1rem;cursor:pointer}.wvpbar button:disabled{opacity:.35}",
".wvpbar .wvpn{flex:1;text-align:center;font-weight:700;color:#5b665f}"].join("\n");
window.WRV={present:present,esc:esc,san:san,render:render,blocksHTML:blocksHTML,drawSVG:drawSVG,svgItem:svgItem,slides:slides,paintMath:paintMath,css:css,KL:KL};
})();
