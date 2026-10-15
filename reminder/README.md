# 수행평가 알림장

수행평가 마감일과 메모를 적어 두면 급한 순서로 보여 주는 리마인더.

- 앱: https://claude.ai/artifact/6iJZZVo4yQLSEoDhY3mHhM (본인만 열 수 있음)

## 기능

- 수행평가: 과목·할 일·마감일(시간 선택)·준비물 → D-day 순 정리 (마감 지남 / 오늘·3일 안 / 그 뒤)
- 완료 체크, 고치기, 지우기(두 번 눌러 확인), 과목별 거르기
- 앞으로 2주 달력에 마감과 메모 알림 표시
- 메모: 쪽지처럼 붙이기, 알려 줄 날 지정, 맨 위 고정

## 데이터 (artifact db)

- `tasks/<id>`: `{subject, title, due: "YYYY-MM-DD", time: "HH:MM"|null, note, done, doneAt, createdAt}`
- `memos/<id>`: `{text, remindOn: "YYYY-MM-DD"|null, pinned, createdAt}`

`index.html`을 고친 뒤에는 같은 주소로 다시 발행한다.
