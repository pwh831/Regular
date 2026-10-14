# 영단어 시험

Word Master 하이스트 Day 1–50(1500단어, 책 전체)을 보고 뜻을 고르는 5지선다 시험.

- 앱: https://claude.ai/artifact/StK4zvRCC7kfHcVPJtjmHD (본인만 열 수 있음)
- 날짜와 상관없이 진도대로: 다음 세트(Day 2개, 60문제)를 보고, 틀린 것만 다시 풀기를 반복해 다 맞히면 그 Day들이 끝나고 바로 다음 세트로 넘어감. 하루에 몇 세트든 가능
- 오답 보기는 같은 품사(뜻의 어미로 추정)에서 먼저 뽑음
- 오답 노트: 마지막으로 틀린 단어만 모음

## 데이터

단어와 뜻은 시판 단어장 내용이라 **이 공개 저장소에 넣지 않고** 앱의 비공개 db에만 둔다.

- `words/dayNN`: `{day, words: [{n, w, m}]}`
- `progress/main`: `{stats: {n: {c, x, last}}, best: {d1-2: 점수}, cleared: {Day: 끝낸 날짜}}` — 다음 세트는 `cleared`의 가장 큰 Day 다음
- `sessions/*`: 시험 기록
- `settings/main`: `{totalDays}` — 들어 있는 마지막 Day(지금 50) (`startDate`는 옛 날짜 일정의 흔적, 안 씀)

영단어는 복습 플래너에 넣지 않는다. 공부 홈이 `progress/main.cleared`로 다음 세트와 오늘 끝낸 Day 수를 보여 준다.

