# 분량 나누기

문제집·인강 분량을 하루 몫으로 나누고, 밀리면 남은 분량을 다시 나눠 주는 공부 계획표.

- 앱: https://claude.ai/artifact/QErpysS6X7mswxgv57EzeV (본인만 열 수 있음)
- 기능: `db`(계획), `sample`(목차·빠른 정답·강의 목록 사진이나 글에서 단원과 개수 뽑기)

## 나누는 규칙 (`split.py`와 `index.html`의 `split()`이 같음)

1. 단원을 문제(강) 하나씩으로 펼친다. "한 번에" 단원(단원 모의고사 등)은 통째로 한 덩어리.
2. 무게: 보통 1, 조금 무거움 1.5, 시험처럼 푸는 모의고사 2.5(10문항 = 보통 25문제 분량).
3. 전체 무게를 공부하는 날 수로 똑같이 나누고, 각 문제는 자기 무게의 가운데가 들어가는 날에 배정.
4. 새 단원을 1~4문제만 하고 끝나는 날은 그 조각을 다음 날로 넘긴다.
5. 공부하는 날 수: "하루 N개"면 ceil(전체 무게 / N), "날짜까지"면 시작~끝 사이 쉬는 요일을 뺀 날.

다시 나누기: 끝낸 날은 그대로 두고, 끝내지 않은 문제만 모아 오늘부터 다시 나눈다(끝나는 날 유지 = 하루 양이 늘어남, 하루 분량 유지 = 끝나는 날이 늦어짐).

## 데이터

- `plans/<id>`: `{title, kind: book|lecture, color, units: [{name, count, weight, whole}], startDate, restDays, mode: daily|end, perDay, endDate, days: [{date, parts: [{unit, from, to}], effort, done, doneAt}], createdAt}`

공부 홈 요약과 아침·저녁 알림 루틴이 `plans`를 읽어 그날 분량을 보여 준다(읽기만 함).
