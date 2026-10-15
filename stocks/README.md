# 내 주식

토스증권 Open API로 내 계좌(평가금액·수익률·종목별 손익)와 관심 종목 시세(전일 종가 대비 등락)를 보는 대시보드. 내 PC에서 실행한다.

## 왜 PC에서 돌리나

- 토스 API는 브라우저에서 직접 부를 수 없다(CORS 없음). 그래서 다른 공부 앱처럼 artifact로는 못 만든다
- 허용 IP에 등록한 컴퓨터에서만 호출된다. 클라우드 루틴은 IP가 바뀌어 막힌다
- Client Secret은 화면 코드에 넣으면 안 된다. 이 스크립트가 PC 안에서만 들고 있다

## 처음 한 번 설정

1. 토스증권 웹(WTS)에 로그인 → 설정 > Open API → `client_id`, `client_secret` 발급
2. 같은 화면 아래 **허용 IP 관리**에 이 PC의 공인 IP 등록 (네이버에 "내 IP"로 검색하면 나온다)
3. 이 폴더의 `config.example.json`을 복사해 `config.local.json`으로 저장하고 두 값을 넣는다 (WTS의 복사 버튼으로, 앞뒤 공백 없이)
4. 파이썬 3.9 이상 설치 (python.org, 설치할 때 "Add to PATH" 체크)

`config.local.json`, 토큰 캐시 `.token.json`, 관심 종목 `watchlist.json`은 `.gitignore`로 저장소에 올라가지 않는다. 키를 채팅이나 저장소에 붙여넣지 않는다.

## 실행

```
python toss.py check   # 연결 확인: 토큰 · 시세 · 계좌
python toss.py         # 대시보드 → http://127.0.0.1:8765 이 열림 (끄기: Ctrl+C)
```

- 관심 종목: 6자리 코드(삼성전자 005930, KODEX 200 069500) 또는 미국 티커(AAPL). 화면에서 추가·삭제
- 시세는 30초, 계좌는 2분마다 갱신
- 주문 기능은 넣지 않았다(조회 전용)

## 문제 해결

| 화면 메시지 | 원인 |
|---|---|
| 허용 IP에 없습니다 | 집 공유기 IP가 바뀌었거나 다른 곳(학교·카페)에서 실행. WTS에서 지금 IP를 다시 등록 |
| client_id 또는 client_secret이 틀렸습니다 | 다시 복사해서 `config.local.json`에 넣기 |
| 다른 곳에서 토큰을 새로 받아 … 끊겼습니다 | 토큰은 계정당 하나만 유효. 다른 PC나 프로그램에서 같은 키를 쓰지 않기 |

## 구조

- `toss.py`: 토큰 발급·캐시(만료 5분 전까지 재사용), API 호출, `127.0.0.1`에만 뜨는 로컬 서버. 표준 라이브러리만 사용
- `dashboard.html`: 화면. `/api/quotes`, `/api/holdings`, `/api/watchlist`(POST)만 부른다
- 등락률: 현재가(`/api/v1/prices`)와 일봉 2개(`/api/v1/candles`)의 전일 종가로 계산
- 다른 주소 `TOSS_BASE`, 포트 `TOSS_PORT` 환경변수로 바꿀 수 있다

토스 API로 받은 데이터는 본인 투자 목적으로만 쓰고 다른 사람에게 공유하지 않는다(토스증권 이용 정책).
