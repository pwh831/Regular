# 경제 지필고사

2학년 경제 지필고사 대비 앱. 선택형 15문항 중 수업 PPT에서 나오는 2~3문항과 서답형 4문항(5·5·10·10점)을 연습한다. 나머지 선택형은 학평·모평 기출이라 이 앱에서 다루지 않는다.

- 앱: https://claude.ai/artifact/SCy6xivPdPR8Vi6E4gj9Bs (본인만 열 수 있음)
- 문제 출제와 서답형 채점은 artifact의 `sample` 기능으로 보는 사람의 Claude 계정에 요청한다

## 탭

- 서답형: 고른 슬라이드로 서답형 4문항 생성. 1·2번 단답형 5점, 3·4번 서술형 10점. 채점은 선생님 방식(단답 부분 점수 없음, 서술은 "핵심 내용 중 N부분" 기준표). 종이 답안 사진도 받음
- 객관식: 슬라이드 세부(숫자·연도·인물·출처·사례)를 묻는 5지선다
- 암기: 암기 노트 PDF와 같은 240개 항목으로 바로 퀴즈(객관식·주관식·섞기, 단원·분류·중요도, 틀린 것 위주). 주관식 단답은 자동 채점, 목록형은 Claude 채점 또는 직접 인정
- 슬라이드: 쪽별 정리, 슬라이드마다 확인 문제 3개, "외웠어요" 진도
- 오답노트: 틀리거나 감점된 문항, 자주 틀린 슬라이드로 바로 가기

## 데이터 (artifact db)

수업 자료와 기출은 저작물이라 **이 공개 저장소에 넣지 않고** 앱의 비공개 db에만 둔다.

- `materials/all`: `{slides: [{page, unit, tb(교과서 쪽), title, text, prio, hot}], count}` 수업 PPT 전체(1~6.pdf 325장, 중복 합쳐 292장, 교과서 8~81쪽) 정리. `prio`는 직접 추린 30장, `hot`은 선생님이 "시험에 낼거야"라고 적은 슬라이드. 약 5만 자라 출제 때 전부 Claude에 보낸다
- `reference/style`: 선생님 출제 방식 분석, `reference/past-2025-1`: 작년 1회 고사 원문과 정답
- `exams/<id>`: `{kind: sd|mc, title, createdAt, sel, status, questions, answers, graded, mastered}`
- `progress/main`: `{studied: [쪽]}`
- `memo/all`: `{items: [{id, u(단원), c(분류), q, a, acc(인정 표기), s(슬라이드), p(중요도 0~2)}]}` 암기 항목. 암기 노트 PDF와 같은 원본(작업 폴더의 memo.py)에서 만든다
- `progress/memo`: `{stats: {id: {c, x, last}}}` 암기 퀴즈 기록

슬라이드를 더 받으면 `materials/all`의 `slides`에 추가하거나 `materials`에 문서를 더 넣는다(앱을 다시 발행할 필요 없음). `index.html`을 고친 뒤에는 같은 주소로 다시 발행한다.
