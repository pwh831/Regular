# 국어 변형 출제실

독서·문학 지문과 선생님 필기를 넣으면 내신 변형 문제를 만들고, 정답을 가린 채 따로 검수한 뒤 걸린 문항을 고쳐 주는 앱.
`prompts/README.md`의 출제 → 검수 → 수정 프롬프트를 자동으로 돌린다.

- 앱: https://claude.ai/artifact/9NWK2wCogbVtCb8M177dYJ (본인만 열 수 있음)
- Claude 호출은 artifact `sample` 기능을 쓴다. 보는 사람의 Claude 사용량을 쓰고, API 키는 필요 없다.

## 흐름

1. **출제**: 지문을 문장(시는 행)으로 나눠 앱이 직접 번호를 붙인다. 원문을 AI가 다시 쓰지 않아서 원문이 바뀌지 않는다. 선지마다 `fits`(적절/부적절)와 근거 번호를 받는다.
2. **검수**: 객관식 정답을 뺀 채 별도 호출로 검토 위원이 직접 푼다. 아래 중 하나라도 걸리면 수정 대상.
   - 검토 위원의 답이 출제 답과 다름
   - 다른 선지도 답이 될 여지가 있다고 함
   - 검토 위원 판정이 통과가 아님
   - 앱 자체 확인: 선지 5개, 발문("적절하지 않은 것" 등)과 `fits` 표시가 맞물려 답이 하나로 정해지는지, 근거 번호가 지문 범위 안인지
3. **수정**: 걸린 문항만 고치거나(출제자가 반박하면 해명을 남김) 새로 만든다.
4. **다시 검수**: 고친 문항만 한 번 더. 그래도 걸리면 `직접 확인`으로 표시하고 남은 지적을 보여 준다.

단계는 세트에 저장해서 멈추거나 창을 닫아도 이어서 할 수 있다. 필기 사진은 저장하지 않는다.

## 데이터 (artifact db)

- `sets/<id>`: `{title, kind, passage, byLine, units: [{t, p}], note, examples, cond: {mc, essay, level, must}, tier, stage, questions, attempts, hadImages, createdAt, doneAt}`
  - `stage`: `new` → `generated` → `reviewed` → `revised` → `done`
  - 문항 `st`: `pending`, `pass`(바로 통과), `flag`(수정 대기), `revised`, `fixed`(고쳐서 통과), `check`(직접 확인)
  - `attempts`: 최근 20번의 풀이 `{at, right, total, answers}`

`index.html`을 고친 뒤에는 같은 주소로 다시 발행한다.
