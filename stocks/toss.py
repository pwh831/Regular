"""토스증권 Open API 주식 대시보드 (내 PC에서 실행).

토스 API는 브라우저에서 직접 부를 수 없고(CORS 없음), 허용 IP에 등록한 컴퓨터에서만 열린다.
그래서 이 스크립트가 내 PC에서 토큰을 들고 API를 부르고, 화면은 http://127.0.0.1:8765 로 띄운다.
파이썬 표준 라이브러리만 쓴다(설치할 것 없음).

  python toss.py          대시보드 실행 (브라우저가 열림)
  python toss.py check    연결 확인만 (토큰 · 시세 · 계좌)

키는 같은 폴더의 config.local.json 또는 환경변수 TOSS_CLIENT_ID / TOSS_CLIENT_SECRET 에 둔다.
config.local.json, .token.json, watchlist.json 은 .gitignore 로 저장소에 올라가지 않는다.
"""
import datetime as dt
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("TOSS_BASE", "https://openapi.tossinvest.com")
PORT = int(os.environ.get("TOSS_PORT", "8765"))
CONFIG = os.path.join(HERE, "config.local.json")
TOKEN_FILE = os.path.join(HERE, ".token.json")
WATCH_FILE = os.path.join(HERE, "watchlist.json")
DEFAULT_WATCH = ["005930"]

# 오류 코드 → 해결 방법
HINTS = {
    "ip-not-allowed": "이 컴퓨터의 공인 IP가 허용 IP에 없습니다. 토스증권 WTS 설정 > Open API > 허용 IP 관리에 등록하세요.",
    "access_denied": "이 컴퓨터의 공인 IP가 허용 IP에 없습니다. 토스증권 WTS 설정 > Open API > 허용 IP 관리에 등록하세요.",
    "invalid_client": "client_id 또는 client_secret이 틀렸습니다. WTS의 복사 버튼으로 다시 복사하세요(앞뒤 공백 주의).",
    "invalid_request": "client_id 또는 client_secret이 비어 있습니다. config.local.json을 확인하세요.",
    "token-revoked": "다른 곳에서 토큰을 새로 받아 이 토큰이 끊겼습니다. 토큰은 계정당 하나만 유효합니다.",
    "edge-rate-limit-exceeded": "호출이 너무 잦습니다. 잠시 뒤 다시 시도하세요.",
    "stock-not-found": "없는 종목 코드입니다. 국내는 6자리 코드(예: 005930), 미국은 티커(예: AAPL)입니다.",
}


class TossError(Exception):
    def __init__(self, status, code, message):
        super().__init__(f"{status} {code}: {message}")
        self.status, self.code, self.message = status, code, message

    def to_json(self):
        return {"status": self.status, "code": self.code, "message": self.message, "hint": HINTS.get(self.code, "")}


def load_json(path, default):
    try:
        with open(path, encoding="utf-8-sig") as f:  # 메모장이 붙이는 BOM 허용
            return json.load(f)
    except (OSError, ValueError):
        return default


def save_json(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def credentials():
    cfg = load_json(CONFIG, {})
    cid = (os.environ.get("TOSS_CLIENT_ID") or cfg.get("client_id") or "").strip()
    secret = (os.environ.get("TOSS_CLIENT_SECRET") or cfg.get("client_secret") or "").strip()
    if not cid or not secret or cid.startswith("여기에") or secret.startswith("여기에"):
        raise TossError(0, "no-credentials", f"키가 없습니다. {CONFIG} 에 client_id와 client_secret을 넣으세요.")
    return cid, secret


def _request(method, path, params=None, headers=None, form=None):
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = urllib.parse.urlencode(form).encode() if form else None
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    if form:
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = load_body(e)
        err = body.get("error")
        if isinstance(err, dict):  # 공통 에러 envelope
            raise TossError(e.code, err.get("code", ""), err.get("message", "")) from None
        if isinstance(err, str):  # OAuth2 형식
            raise TossError(e.code, err, body.get("error_description", "")) from None
        raise TossError(e.code, "http-error", str(body)[:200]) from None
    except urllib.error.URLError as e:
        raise TossError(0, "network", str(e.reason)) from None


def load_body(e):
    try:
        return json.loads(e.read().decode("utf-8"))
    except ValueError:
        return {}


class Client:
    """토큰은 계정당 하나만 유효하므로 파일에 캐시해 두고 만료 직전에만 새로 받는다."""

    def __init__(self):
        self.lock = threading.Lock()
        self.token = load_json(TOKEN_FILE, {})
        self.account_seq = None

    def _token(self, force=False):
        with self.lock:
            if not force and self.token.get("access_token") and self.token.get("expires_at", 0) > time.time() + 300:
                return self.token["access_token"]
            cid, secret = credentials()
            r = _request("POST", "/oauth2/token", form={
                "grant_type": "client_credentials", "client_id": cid, "client_secret": secret})
            self.token = {"access_token": r["access_token"], "expires_at": time.time() + int(r.get("expires_in", 86400))}
            save_json(TOKEN_FILE, self.token)
            return self.token["access_token"]

    def get(self, path, params=None, account=False):
        for attempt in (0, 1):
            headers = {"Authorization": "Bearer " + self._token(force=attempt == 1)}
            if account:
                headers["X-Tossinvest-Account"] = str(self.account())
            try:
                return _request("GET", path, params, headers)["result"]
            except TossError as e:
                if attempt == 0 and e.code in ("expired-token", "invalid-token"):
                    continue  # 한 번만 새 토큰으로 재시도
                raise

    def account(self):
        if self.account_seq is None:
            accounts = self.get("/api/v1/accounts")
            if not accounts:
                raise TossError(404, "account-not-found", "계좌가 없습니다.")
            self.account_seq = accounts[0]["accountSeq"]
        return self.account_seq


def prev_close(candles, price_ts, usd):
    """일봉에서 전일 종가를 찾는다. 최신 봉이 현재 거래일이면 그 앞 봉의 종가."""
    if not candles:
        return None
    if not price_ts:
        return candles[1]["closePrice"] if len(candles) > 1 else None
    now = dt.datetime.fromisoformat(price_ts)
    start = dt.datetime.fromisoformat(candles[0]["timestamp"])
    # 국내 일봉은 KST 자정, 미국 일봉은 뉴욕 자정 기준이고 미국 거래일은 뉴욕 전일 20:00에 시작
    if usd:
        start -= dt.timedelta(hours=4)
    in_latest = start <= now < start + dt.timedelta(hours=24)
    if in_latest:
        return candles[1]["closePrice"] if len(candles) > 1 else None
    return candles[0]["closePrice"]


def quotes(client, symbols):
    if not symbols:
        return []
    joined = ",".join(symbols)
    prices = {p["symbol"]: p for p in client.get("/api/v1/prices", {"symbols": joined})}
    names = {s["symbol"]: s for s in client.get("/api/v1/stocks", {"symbols": joined})}
    out = []
    for sym in symbols:
        p, info = prices.get(sym), names.get(sym, {})
        row = {"symbol": sym, "name": info.get("name") or sym, "market": info.get("market", ""),
               "currency": (p or info).get("currency", ""), "price": None, "prevClose": None,
               "change": None, "rate": None, "time": None}
        if p:
            row["price"], row["time"] = p["lastPrice"], p.get("timestamp")
            try:
                c = client.get("/api/v1/candles", {"symbol": sym, "interval": "1d", "count": 2})
                pc = prev_close(c.get("candles", []), p.get("timestamp"), row["currency"] == "USD")
            except TossError:
                pc = None
            if pc:
                last, base = float(p["lastPrice"]), float(pc)
                row["prevClose"], row["change"] = pc, last - base
                row["rate"] = (last - base) / base if base else None
        out.append(row)
    return out


def watchlist():
    w = load_json(WATCH_FILE, None)
    return w if isinstance(w, list) else list(DEFAULT_WATCH)


def clean_symbol(s):
    s = (s or "").strip().upper()
    if not s or len(s) > 12 or not all(ch.isalnum() or ch in ".-" for ch in s):
        return None
    return s


CLIENT = Client()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, body, ctype="application/json; charset=utf-8"):
        data = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def guarded(self, fn):
        try:
            self.send(200, fn())
        except TossError as e:
            self.send(502, {"error": e.to_json()})

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/":
            with open(os.path.join(HERE, "dashboard.html"), "rb") as f:
                self.send(200, f.read(), "text/html; charset=utf-8")
        elif path == "/api/quotes":
            self.guarded(lambda: {"watchlist": watchlist(), "quotes": quotes(CLIENT, watchlist()),
                                  "fetchedAt": dt.datetime.now().isoformat(timespec="seconds")})
        elif path == "/api/holdings":
            self.guarded(lambda: CLIENT.get("/api/v1/holdings", account=True))
        else:
            self.send(404, {"error": {"code": "not-found", "message": path}})

    def do_POST(self):
        # 다른 사이트가 이 로컬 서버로 요청을 보내지 못하게 같은 출처만 허용
        origin = self.headers.get("Origin", "")
        if origin and origin not in (f"http://127.0.0.1:{PORT}", f"http://localhost:{PORT}"):
            return self.send(403, {"error": {"code": "forbidden", "message": "origin"}})
        if urllib.parse.urlparse(self.path).path != "/api/watchlist":
            return self.send(404, {"error": {"code": "not-found", "message": self.path}})
        n = int(self.headers.get("Content-Length") or 0)
        body = json.loads(self.rfile.read(min(n, 10000)) or b"{}")
        sym, w = clean_symbol(body.get("symbol")), watchlist()
        if not sym:
            return self.send(400, {"error": {"code": "invalid-symbol", "message": "종목 코드 형식이 아닙니다."}})
        if body.get("action") == "remove":
            w = [s for s in w if s != sym]
        elif sym not in w:
            try:
                CLIENT.get("/api/v1/stocks", {"symbols": sym})
            except TossError as e:
                return self.send(400, {"error": e.to_json()})
            w.append(sym)
        save_json(WATCH_FILE, w[:50])
        self.send(200, {"watchlist": w[:50]})


def check():
    print("토큰 발급...", end=" ")
    CLIENT._token()
    print("OK")
    for q in quotes(CLIENT, watchlist()):
        rate = f"{q['rate'] * 100:+.2f}%" if q["rate"] is not None else "-"
        print(f"  {q['name']} ({q['symbol']}): {q['price']} {q['currency']}  {rate}")
    h = CLIENT.get("/api/v1/holdings", account=True)
    print(f"계좌 OK: 보유 {len(h.get('items', []))}종목")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        try:
            check()
        except TossError as e:
            print("\n실패:", e)
            if HINTS.get(e.code):
                print("해결:", HINTS[e.code])
            sys.exit(1)
        return
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    url = f"http://127.0.0.1:{PORT}"
    print(f"주식 대시보드: {url}  (끄려면 Ctrl+C)")
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
