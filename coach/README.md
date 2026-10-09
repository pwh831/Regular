# 오답 코치

틀린 문제를 사진·원인과 함께 남기면, 다시 풀기 일정을 잡고 Claude가 반복 패턴과 과목 성격에 맞는 공부법을 골라 주는 오답 노트.

- 앱: https://claude.ai/artifact/ER7W1Mv79CCcMd9s6qR4f4 (본인만 열 수 있음)
- 기능: `db`(기록), `assets`(문제 사진), `sample`(앱 안에서 Claude에게 분석 요청 — 보는 사람의 Claude 사용량을 씀)

## 흐름

1. 기록하기: 사진(선택), 과목(확통·독서·현윤·경제·지역이해·일본어·문학과 영상·영어 중 하나), 단원, 출처, 틀린 이유(개념 / 헷갈림 / 실수 / 시간 / 잘못 읽음), 정답·핵심, 메모
2. 다시 풀기: 1·3·7일 뒤. "또 틀렸어요"면 다음 날 한 번 더(최대 8번)
3. 분석·공부법: 기간별 원인·과목 막대, 원인별 기본 처방(Claude 없이도 보임), Claude 패턴 분석(JSON 결과 저장)
4. 문제 하나 분석: 사진과 메모로 원인·다시 볼 개념·공부법·체크 한 줄

## 데이터

- `mistakes/*`: `{subject, unit, source, date, cause, key, note, imageId, retries: [{date, result, doneAt}], ai, createdAt}`
- `analyses/*`: `{at, rangeLabel, count, result: {summary, patterns, methods, week}}`

아침(6:30)·저녁(8:00) 복습 알림 루틴이 `mistakes`를 읽어서 그날 다시 풀 오답 개수를 함께 알려 준다(읽기만 함).
