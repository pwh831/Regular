"""공부 홈 요약 만들기.

루틴이 복습 플래너·영단어 시험·오답 코치의 db를 ArtifactData `out_dir`로 내려받은 뒤
  python3 aggregate.py <내려받은 폴더> <오늘 YYYY-MM-DD> <지금 HH:MM> > snapshot.json
으로 실행한다. 폴더 구조: planner/subjects, planner/items, vocab/sessions, vocab/settings,
vocab/progress, coach/mistakes (각 문서 = <id>.json, 내용은 문서 본문).
"""
import json, os, sys, datetime as dt

PLANNER = "https://claude.ai/artifact/AGrdmtMU9agaqqtpoBbqkV"
VOCAB = "https://claude.ai/artifact/StK4zvRCC7kfHcVPJtjmHD"
COACH = "https://claude.ai/artifact/ER7W1Mv79CCcMd9s6qR4f4"
# 플래너 과목 이름 → 오답 코치 과목 이름(같게 맞춰 둠)
ORDER = ["확통", "독서", "현윤", "경제", "지역이해", "일본어", "문학과 영상", "영어"]


def load(base, *parts):
    d = os.path.join(base, *parts)
    out = {}
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f.endswith(".json"):
                with open(os.path.join(d, f), encoding="utf-8") as fh:
                    out[f[:-5]] = json.load(fh)
    return out


def D(s):
    return dt.date.fromisoformat(s)


def main(base, today, now):
    t = D(today)
    subjects = load(base, "planner", "subjects")
    items = load(base, "planner", "items")
    sessions = load(base, "vocab", "sessions")
    vset = load(base, "vocab", "settings").get("main", {})
    vprog = load(base, "vocab", "progress").get("main", {})
    mistakes = load(base, "coach", "mistakes")

    subj_by_id = {k: v for k, v in subjects.items()}
    todo, done_today, planned_today = [], 0, 0
    lates = {}
    color_by_name = {v.get('name'): v.get('color') for v in subjects.values()}
    per = {}  # 과목 이름 → 통계

    def S(name):
        return per.setdefault(name, {"due7": 0, "done7": 0, "overdue": 0, "mistakesOpen": 0, "mistakesDue": 0})

    week = {(t - dt.timedelta(days=i)).isoformat(): {"planned": 0, "done": 0} for i in range(6, -1, -1)}

    for iid, it in items.items():
        sj = subj_by_id.get(it.get("subjectId"), {})
        name = sj.get("name", "기타")
        url = sj.get("quizUrl") or PLANNER
        for i, r in enumerate(it.get("reviews") or []):
            d, done = r.get("date"), bool(r.get("done"))
            if not d:
                continue
            if d in week:
                week[d]["planned"] += 1
                if done:
                    week[d]["done"] += 1
            if d <= today and D(d) > t - dt.timedelta(days=7):
                S(name)["due7"] += 1
                if done:
                    S(name)["done7"] += 1
            if d == today:
                planned_today += 1
                if done:
                    done_today += 1
            if done or d > today:
                continue
            first = r.get("day") == 0
            late = (t - D(d)).days
            if late > 0:
                S(name)["overdue"] += 1
                lates.setdefault(iid, {"subject": name, "color": sj.get("color"), "title": it.get("title", ""), "url": url,
                                       "app": "퀴즈" if sj.get("quizUrl") else "플래너", "n": 0, "max": 0})
                lates[iid]["n"] += 1
                lates[iid]["max"] = max(lates[iid]["max"], late)
                continue
            base0 = (it.get("reviews") or [{}])[0].get("day") == 0
            todo.append({
                "group": "first" if first else "review",
                "subject": name, "color": sj.get("color"),
                "title": it.get("title", ""),
                "detail": "첫 학습" if first else f"{i if base0 else i + 1}회차 복습",
                "url": url, "app": "퀴즈" if sj.get("quizUrl") else "플래너",
            })

    for x in lates.values():  # 한 항목의 밀린 복습은 한 줄로
        todo.append({"group": "overdue", "subject": x["subject"], "color": x["color"], "title": x["title"],
                     "detail": f"밀린 복습 {x['n']}번 · 최대 {x['max']}일", "url": x["url"], "app": x["app"]})

    m_open = m_due = 0
    causes = {}
    for mid, m in mistakes.items():
        rs = m.get("retries") or []
        nxt = next((r for r in rs if not r.get("result")), None)
        name = m.get("subject", "기타")
        if nxt:
            m_open += 1
            S(name)["mistakesOpen"] += 1
            if nxt.get("date", "9999") <= today:
                m_due += 1
                S(name)["mistakesDue"] += 1
                todo.append({"group": "mistake", "subject": name, "color": color_by_name.get(name),
                             "title": (m.get("unit") or "오답 다시 풀기"), "detail": "오답 다시 풀기",
                             "url": COACH, "app": "오답 코치"})
        if D(m.get("date", today)) > t - dt.timedelta(days=14):
            causes[m.get("cause")] = causes.get(m.get("cause"), 0) + 1
    cause_name = {"concept": "개념을 몰라서", "confuse": "헷갈려서", "careless": "계산·실수", "time": "시간 부족", "misread": "문제를 잘못 읽음"}
    top_cause = max(causes, key=causes.get) if causes else None

    # 영단어
    vt = None
    if vset.get("startDate"):
        k = (t - D(vset["startDate"])).days
        if 0 <= k < 7:
            vt = [2 * k + 1, 2 * k + 2]
    best = None
    s7 = 0
    for s in sessions.values():
        if s.get("date") and D(s["date"]) > t - dt.timedelta(days=7):
            s7 += 1
        if vt and s.get("date") == today and not s.get("quit") and s.get("total"):
            days = s.get("days") or []
            if all(d in days for d in vt):
                pct = round(s["right"] / s["total"] * 100)
                best = pct if best is None else max(best, pct)
    stats = vprog.get("stats") or {}
    seen = [v for v in stats.values() if v.get("last") is not None]
    overall = round(sum(1 for v in seen if v.get("last")) / len(seen) * 100) if seen else None
    if vt:  # 오늘 영단어 첫 학습은 시험 앱 항목 하나로 보여 준다
        tag = f"Day {vt[0]}–{vt[1]}"
        todo[:] = [x for x in todo if not (x["group"] == "first" and x["title"].endswith(tag))]
    if vt and (best is None or best < 90):
        todo.insert(0, {"group": "first", "subject": "영어", "color": color_by_name.get("영어"),
                        "title": f"영단어 시험 Day {vt[0]} · {vt[1]}",
                        "detail": "60문제" if best is None else f"오늘 최고 {best}점 · 90점 필요",
                        "url": VOCAB, "app": "영단어"})

    exams, subs = [], []
    names = sorted(subjects.values(), key=lambda s: (ORDER.index(s["name"]) if s.get("name") in ORDER else 99, s.get("order", 0)))
    for sj in names:
        name = sj.get("name")
        ex = sj.get("examDate")
        dday = (D(ex) - t).days if ex else None
        if ex and dday >= 0:
            exams.append({"subject": name, "date": ex, "dday": dday, "color": sj.get("color")})
        st = per.get(name, {})
        subs.append({"name": name, "color": sj.get("color"), "examDate": ex, "dday": dday,
                     "url": sj.get("quizUrl"), "due7": st.get("due7", 0), "done7": st.get("done7", 0),
                     "overdue": st.get("overdue", 0), "mistakesOpen": st.get("mistakesOpen", 0),
                     "mistakesDue": st.get("mistakesDue", 0)})
    exams.sort(key=lambda e: e["dday"])
    order = {"first": 0, "review": 1, "mistake": 2, "overdue": 3}
    todo.sort(key=lambda x: order.get(x["group"], 9))

    return {
        "generatedAt": dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "kstDate": today, "kstTime": now,
        "todo": todo, "doneToday": done_today, "plannedToday": planned_today,
        "exams": exams, "subjects": subs,
        "week": [{"date": k, **v} for k, v in week.items()],
        "vocab": {"today": vt, "todayBest": best, "overall": overall, "sessions7": s7, "url": VOCAB},
        "coach": {"open": m_open, "due": m_due, "topCause": cause_name.get(top_cause), "url": COACH},
        "plannerUrl": PLANNER,
    }


if __name__ == "__main__":
    print(json.dumps(main(sys.argv[1], sys.argv[2], sys.argv[3]), ensure_ascii=False))
