# 영단어 시험

Word Master 하이스트 Day 1–14(420단어)를 보고 뜻을 고르는 5지선다 시험.

- 앱: https://claude.ai/artifact/StK4zvRCC7kfHcVPJtjmHD (본인만 열 수 있음)
- 하루 2 Day씩(60문제), 시작일은 앱에서 바꿀 수 있음
- 오답 보기는 같은 품사(뜻의 어미로 추정)에서 먼저 뽑음
- 오답 노트: 마지막으로 틀린 단어만 모음

## 데이터

단어와 뜻은 시판 단어장 내용이라 **이 공개 저장소에 넣지 않고** 앱의 비공개 db에만 둔다.

- `words/dayNN`: `{day, words: [{n, w, m}]}`
- `progress/main`: `{stats: {n: {c, x, last}}, best: {d1-2: 점수}}`
- `sessions/*`: 시험 기록
- `settings/main`: `{startDate}`

복습 플래너에는 과목 "영어 단어"와 Day 두 개 묶음마다 첫 학습(0일) + 1·3·7·15·30일 복습이 잡혀 있다.
