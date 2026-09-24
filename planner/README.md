# 복습 플래너

리리플래너처럼 에빙하우스 망각곡선 주기로 복습 날짜를 잡아 주는 공부 플래너.

- 앱: https://claude.ai/artifact/AGrdmtMU9agaqqtpoBbqkV (본인만 열 수 있음)
- 알림: 루틴 "복습 플래너 알림"이 매일 20:00 KST에 플래너 데이터를 읽어 Claude 앱으로 푸시

## 기능

- 공부한 내용을 적으면 복습 날짜 자동 생성 (기본 1·3·7·15·30일, 시험 직전 1·2·4·7일, 직접 입력)
- 과목별 시험일 → D-day 표시, 시험일 이후 복습은 자동 제외
- 쉬는 요일에 걸린 복습은 다음 날로 미룸
- 오늘 할 복습 / 밀린 복습 체크, 월간 캘린더
- 과목마다 퀴즈 링크 (지역이해, 일본어 회화)

## 데이터 (artifact db)

- `subjects/<id>`: `{name, color, examDate, quizUrl, order}`
- `items/<id>`: `{subjectId, title, studiedOn, reviews: [{day, date, done, doneAt}], createdAt}`
- `settings/main`: `{restDays: [0-6], notifyTimeKST}`

`index.html`을 고친 뒤에는 같은 주소로 다시 발행한다.
