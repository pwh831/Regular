# 경제 지필고사

시험 범위로 경제 지필고사(중간·기말) 모의고사를 만들고 채점해 주는 앱. 문제 출제와 서술형 채점은 Claude가 한다.

- 앱: https://claude.ai/artifact/SCy6xivPdPR8Vi6E4gj9Bs (본인만 열 수 있음)
- artifact의 `sample` 기능으로 보는 사람의 Claude 계정에 요청한다(처음 한 번 허용을 묻는다)

## 탭

- 모의고사: 단원(고등학교 「경제」 Ⅰ~Ⅴ) 선택, 범위 메모·학습지 붙여 넣기·사진 첨부, 객관식/서술형 문항 수와 난이도 선택 → 시험지 생성. 객관식은 바로 채점, 서술형은 채점 기준으로 부분 점수. 100점 환산, 다시 풀기
- 서술형: 문제와 내 답안(사진 가능)을 넣으면 예상 점수, 항목별 근거, 빠진 핵심어, 고쳐 쓴 모범 답안
- 오답노트: 제출한 시험의 틀린 문항을 단원별로 모음. "비슷한 문제 풀기"로 변형 문제, "이제 알아요"로 빼기
- 질문하기: 개념 질문 채팅 (대화는 이 브라우저 localStorage에만)

## 데이터 (artifact db)

- `exams/<id>`: `{title, createdAt, level, units, scope, status: draft|done, questions: [...], answers: {i: 선택 번호(0-4) | 서술 답}, graded: {i: {score, feedback, missing}}, mastered: [i], submittedAt}`
  - 객관식 `{type:"mc", unit, points, stem, data, box, choices[5], answer(0-4), explanation}`
  - 서술형 `{type:"essay", unit, points, stem, data, box, rubric:[{c,p}], modelAnswer}`

`index.html`을 고친 뒤에는 같은 주소로 다시 발행한다.
