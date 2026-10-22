// 교사의 생활 (버전 5.36.2): 인터넷이 없어도 열리도록 앱 파일을 휴대폰에 저장합니다.
const CACHE = "attendance-app-5.36.2";
const FILES = ["./", "index.html", "config.js", "privacy.html", "sign.html", "help.html", "manifest.webmanifest", "icon-192.png", "icon-512.png", "icon-maskable-512.png", "apple-touch-icon.png", "NanumGothic-Regular.woff2", "NanumGothic-Bold.woff2", "vendor/qrcode.js"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
// 5.32.0: 음악 파일(mp3)은 통째로 받아 저장해 두고, 재생기가 부분(Range)을 달라고 하면 잘라서 줍니다. (아이폰 재생 + 오프라인 재생)
async function audioResponse(req) {
  const url = new URL(req.url); url.search = "";
  const cache = await caches.open(CACHE);
  let res = await cache.match(url.href);
  if (!res) {
    const net = await fetch(url.href, { credentials: "same-origin" });
    if (!net.ok || net.status !== 200) return net;
    await cache.put(url.href, net.clone()); res = net;
  }
  const range = req.headers.get("range");
  const type = res.headers.get("content-type") || "audio/mpeg";
  const blob = await res.blob();
  if (!range) return new Response(blob, { status: 200, headers: { "Content-Type": type, "Content-Length": String(blob.size), "Accept-Ranges": "bytes" } });
  const m = /bytes=(\d*)-(\d*)/.exec(range) || [];
  let start = m[1] ? +m[1] : 0, end = m[2] ? +m[2] : blob.size - 1;
  if (!m[1] && m[2]) { start = Math.max(0, blob.size - +m[2]); end = blob.size - 1; }
  end = Math.min(end, blob.size - 1);
  if (start > end) return new Response(null, { status: 416, headers: { "Content-Range": "bytes */" + blob.size } });
  return new Response(blob.slice(start, end + 1), { status: 206, headers: { "Content-Type": type, "Content-Length": String(end - start + 1), "Content-Range": `bytes ${start}-${end}/${blob.size}`, "Accept-Ranges": "bytes" } });
}
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET" || new URL(e.request.url).origin !== location.origin) return;
  if (/\.mp3$/.test(new URL(e.request.url).pathname)) { e.respondWith(audioResponse(e.request).catch(() => fetch(e.request))); return; }
  // 새 버전 확인(cache: no-store)은 저장된 파일 없이 바로 인터넷으로 확인합니다.
  if (e.request.cache === "no-store") return;
  // 새 버전이 있으면 받아 두고, 없거나 오프라인이면 저장된 파일을 씁니다.
  // 학교 등에서 주소가 막히거나 응답이 늦으면(4초) 저장된 앱으로 바로 엽니다. 차단 안내 화면은 저장하지 않습니다.
  e.respondWith((async () => {
    const cached = () => caches.match(e.request, { ignoreSearch: true }).then(r => r || (e.request.mode === "navigate" ? caches.match("index.html") : undefined));
    // 앱 화면(html)은 매번 새 버전이 있는지 서버에 물어봅니다 (브라우저 캐시에 오래된 화면이 남지 않게)
    const isPage = e.request.mode === "navigate" || /\.(html|js|webmanifest)$/.test(new URL(e.request.url).pathname);
    const net = (isPage ? fetch(e.request.url, { cache: "no-cache", credentials: "same-origin" }) : fetch(e.request)).then(async res => {
      const good = res.ok && !res.redirected && res.type === "basic";
      if (good) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); return res; }
      const c = await cached(); return c || res;
    });
    const have = await cached();
    if (!have) return net.catch(() => cached().then(r => r || Response.error()));
    const slow = new Promise(r => setTimeout(() => r(have), 4000));
    return Promise.race([net.catch(() => have), slow]);
  })());
});
// 알림을 누르면 앱을 엽니다.
self.addEventListener("notificationclick", e => {
  e.notification.close();
  e.waitUntil(self.clients.matchAll({ type: "window", includeUncontrolled: true }).then(list => {
    for (const c of list) { if ("focus" in c) return c.focus(); }
    return self.clients.openWindow("./");
  }));
});
