# 내신 단어 시험

학교 내신용 영어 단어를 **뜻을 보고 영어로 쓰는** 주관식 시험.

- 앱: https://claude.ai/artifact/1cWASszoP25Fq4VzMTiW5L (본인만 열 수 있음)
- 입력칸에 영어로 쓰고 Enter → 채점하고 바로 다음 단어. 입력칸은 계속 선택된 상태라 클릭할 필요가 없다
- 대소문자, 앞뒤 공백, 물결표(~), 끝의 마침표·쉼표, 앞의 the는 따지지 않는다
- 뜻이 같은 단어가 단원에 여럿이면(예: 통합하다 = integrate, incorporate) 그중 아무거나 정답
- 첫 글자·글자 수 힌트는 켜고 끌 수 있음(이 기기 브라우저에만 기억)
- 끝나면 틀린 것만 다시 풀기, 단원별 오답만 보기

## 데이터

단어장은 학원·학교 자료라 **이 공개 저장소에 넣지 않고** 앱의 비공개 db에만 둔다.

- `units/<id>`: `{title, order, source, words: [{n, w, m}]}` — 새 단원은 문서를 하나 더 넣으면 된다
- `progress/main`: `{stats: {"<unit>:<n>": {c, x, last}}, best: {<unit>: 점수}}`
- `sessions/*`: `{at, date, unit, label, right, total, quit}`
