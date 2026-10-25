# 교사의 생활 - 자동 점검 (업데이트 전에 한 번 돌려 보세요)
#   준비(처음 한 번): pip install playwright pillow openpyxl  →  python -m playwright install chromium
#   실행: 저장소 폴더에서  python tests/run_all.py          (몇 개만:  python tests/run_all.py t105 t112)
# 인터넷(구글 등)에 실제로 접속하지 않습니다. 구글 로그인·드라이브는 가짜(흉내)로 시험합니다.
import gzip, os, re, shutil, subprocess, sys, time, socket, http.server, threading, functools, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.abspath(os.path.join(HERE, ".."))          # tests 폴더의 바로 위 = 앱 폴더 (index.html 이 있는 곳)
WORK = os.path.join(HERE, "_work")                       # 시험 중 만들어지는 파일 (지워도 됨)
ALL = ["t48", "t49", "t50", "t60", "t70", "t73", "t74", "t76", "t77", "t78", "t79", "t80", "t81", "t82", "t83", "t84",
       "t85", "t86", "t87", "t88", "t89", "t90", "t91", "t92", "t93", "t94", "t95", "t96", "t97", "t98", "t100", "t101",
       "t102", "t104", "t105", "t106", "t107", "t108", "t109", "t111", "t112", "t113", "t114", "t115", "t116", "t117", "t118", "t119", "t120", "t121", "t122", "t123", "t124", "t125", "t126", "t127", "t128", "t129", "t130", "t131", "t132", "t133", "t134", "t135", "t136", "t137", "t138", "t141", "t142", "t145", "t146", "t147", "t148", "t149", "t150", "t151"]
NOTE = {"t48": "공유 코드 주고받기", "t49": "설치·서비스워커", "t50": "두 기기 동기화", "t60": "학생 서명 메일", "t70": "시간표 올리기",
        "t73": "평가 삭제·되돌리기", "t74": "결석 연락", "t76": "로그인 만료", "t77": "설정 화면", "t78": "적용 기간",
        "t79": "관찰 기록 잠금", "t80": "사진·녹음 기록", "t81": "새 버전 알림", "t82": "큰 자료·저장 공간", "t83": "서명 현황",
        "t84": "뒤로 가기", "t85": "전표 올리기", "t86": "인쇄·PDF", "t87": "오류 표시줄", "t88": "처음 설정 안내",
        "t89": "시간표 편집", "t90": "엑셀 내보내기", "t91": "관찰 항목 가져오기", "t92": "화면 겹침", "t93": "학사일정 파일",
        "t94": "학사일정 양식", "t95": "학교 묶음 나눠 주기", "t96": "안내 페이지", "t97": "1교시 전·점심·방과 후 활동",
        "t98": "출석 동시 체크", "t100": "메일 형식", "t101": "휴강·결강 통계", "t102": "응원 메시지·음악", "t104": "음악 오프라인",
        "t105": "출석 격자·오늘 탭", "t106": "학년도 보관", "t107": "넓은 화면 패널", "t108": "악성 코드 차단",
        "t109": "망가진 파일 불러오기", "t111": "출석 체크 자동 연결", "t112": "하루 보기·글꼴", "t113": "밀어서 삭제·숫자 칸", "t114": "학교 관리 1단계", "t115": "학교 묶음 배포·받기", "t116": "배포 두 방식·받은 정보 관리", "t117": "명단 갱신 배포", "t118": "배포 기록·담당자 인계", "t119": "학생 인계 카드", "t120": "앱 바로가기·오늘 화면", "t121": "수업 알림·방학 인사·최성보", "t122": "짧은 메모·하루 인사·알림 방식", "t123": "메모 보기·관찰에서 쓰기", "t124": "항목별 모아 보기", "t125": "수행평가·과제 점검", "t126": "평가·과제 공통·연동", "t127": "미참여·미제출 연락", "t128": "글쓰기", "t129": "오후 음악", "t130": "글쓰기 취소·삭제", "t131": "창 닫기·스크롤·빠른 업데이트", "t132": "밀어서 수정·보관·삭제", "t133": "출석→평가·과제 동기화", "t134": "평가한 수업 시간", "t135": "미참여 유형", "t136": "글쓰기 꾸미기·표·도화지·수식", "t137": "문단·간격·내보내기·웹 공유", "t138": "포스트잇·링크 카드", "t141": "교직원 정보·참석자 찾기·직접 보내기", "t142": "받는 사람 찾기·링크 단추", "t145": "기기 화면 폭 맞춤", "t146": "공유 잠금·유효 기간·저장 확인·백업 검사", "t147": "출결 구분·나이스 요약·전체 백업·학번 변경", "t148": "지금 수업·결석 연락·3일 보기", "t149": "시간표 예외·동명이인", "t150": "글쓰기 도구 묶음·기능 찾기", "t151": "학부모 연락처"}

def prepare():
    if os.path.isdir(WORK):
        shutil.rmtree(WORK)
    os.makedirs(os.path.join(WORK, "shot"))
    # 깃허브 웹 업로드는 한 번에 100개까지라서, 시험 파일들은 bundle.zip 하나에 묶어 둡니다
    B = os.path.join(HERE, "bundle.zip")
    if os.path.exists(B):
        with zipfile.ZipFile(B) as z:
            for n in z.namelist():
                if n.endswith("/"):
                    continue
                data = z.read(n)
                if n.endswith(".py") and "/" not in n:
                    data = data.decode("utf-8").replace("__TL_WORK__", WORK.replace("\\", "/")).replace("__TL_APP__", APP.replace("\\", "/")).encode("utf-8")
                    dest = os.path.join(WORK, n)
                elif n.startswith("fixtures/"):
                    dest = os.path.join(WORK, *n[len("fixtures/"):].split("/"))
                elif n.startswith("data/") and n.endswith(".gz"):
                    data = gzip.decompress(data)
                    dest = os.path.join(WORK, os.path.basename(n)[:-3])
                else:
                    continue
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, "wb") as f:
                    f.write(data)
        return
    for f in os.listdir(HERE):
        if f.endswith(".py") and f != "run_all.py":
            s = open(os.path.join(HERE, f), encoding="utf-8").read()
            s = s.replace("__TL_WORK__", WORK.replace("\\", "/")).replace("__TL_APP__", APP.replace("\\", "/"))
            open(os.path.join(WORK, f), "w", encoding="utf-8").write(s)
    fx = os.path.join(HERE, "fixtures")                 # 시험에 쓰는 예시 파일 (시간표 캡처 · 엑셀 전표 · 학사일정 PDF 등)
    if os.path.isdir(fx):
        shutil.copytree(fx, WORK, dirs_exist_ok=True)
    for f in os.listdir(os.path.join(HERE, "data")):
        if f.endswith(".gz"):
            with gzip.open(os.path.join(HERE, "data", f), "rb") as g, open(os.path.join(WORK, f[:-3]), "wb") as o:
                o.write(g.read())

def serve():
    """t48 · t49 · t104 는 진짜 서비스워커가 필요해서 이 컴퓨터 안에서만 앱을 엽니다 (localhost:8766)."""
    try:
        socket.create_connection(("127.0.0.1", 8766), timeout=0.5).close()
        return None
    except OSError:
        pass
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=APP)
    http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8766), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv

def judge(code, out):
    """실패: 프로그램 오류로 멈춤 · 'FAIL' 줄 · 마지막 줄의 오류 목록이 비어 있지 않음"""
    if code != 0 or "Traceback" in out:
        return False
    if re.search(r"^FAIL\b", out, re.M) or re.search(r"fails:? \[\s*'", out):
        return False
    lines = [l for l in out.strip().splitlines() if l.strip()]
    last = lines[-1] if lines else ""
    return not (re.search(r"errors?:\s*\[\s*'", last) or re.match(r"^\s*\['", last))

def main():
    names = [a for a in sys.argv[1:] if a in ALL] or ALL
    if not os.path.exists(os.path.join(APP, "index.html")):
        sys.exit("앱 폴더를 찾지 못했습니다. tests 폴더를 index.html 이 있는 폴더 안에 두세요.")
    prepare()
    srv = serve()
    bad = []
    t0 = time.time()
    for n in names:
        s = time.time()
        p = subprocess.run([sys.executable, n + ".py"], cwd=WORK, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
        out = p.stdout + p.stderr
        ok = judge(p.returncode, out)
        print(f"{'통과' if ok else '실패'}  {n:5} {NOTE.get(n, ''):18} {time.time() - s:5.1f}초")
        if not ok:
            bad.append(n)
            open(os.path.join(WORK, n + ".log"), "w", encoding="utf-8").write(out)
    print(f"\n{len(names) - len(bad)}/{len(names)} 통과 · {time.time() - t0:.0f}초")
    if bad:
        print("실패한 시험의 자세한 기록: tests/_work/<이름>.log  →", ", ".join(bad))
    if srv:
        srv.shutdown()
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
