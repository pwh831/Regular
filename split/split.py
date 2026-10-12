"""분량 나누기 알고리즘 (index.html의 splitPlan과 같은 규칙).

단위(units)를 문제 하나하나(또는 '한 번에' 단위는 통째로)로 펼친 뒤, 누적 노력량을
공부하는 날 수로 똑같이 나눈다. 문제 i는 자기 노력량의 가운데가 들어가는 날에 배정된다.
"""
import math, datetime as dt


def study_dates(start, rest, n=None, end=None):
    d, out = dt.date.fromisoformat(start), []
    endd = dt.date.fromisoformat(end) if end else None
    while (n is None or len(out) < n) and (endd is None or d <= endd):
        if (d.isoweekday() % 7) not in rest:  # 0=일 ... 6=토
            out.append(d.isoformat())
        d += dt.timedelta(days=1)
    return out


def split(units, dates):
    atoms = []
    for ui, u in enumerate(units):
        w = u.get("weight", 1)
        if u.get("whole"):
            atoms.append((ui, 1, u["count"], u["count"] * w))
        else:
            atoms += [(ui, p, p, w) for p in range(1, u["count"] + 1)]
    total, n = sum(a[3] for a in atoms), len(dates)
    days = [{"date": d, "parts": [], "effort": 0, "done": False, "doneAt": None} for d in dates]
    cum = 0
    for ui, a, b, e in atoms:
        k = min(n - 1, int((cum + e / 2) / total * n))
        cum += e
        day = days[k]
        day["effort"] += e
        last = day["parts"][-1] if day["parts"] else None
        if last and last["unit"] == ui and last["to"] == a - 1 and not units[ui].get("whole"):
            last["to"] = b
        else:
            day["parts"].append({"unit": ui, "from": a, "to": b})
    # 새 단원을 1~4문제만 맛보고 끝나는 날이 없게, 그 조각은 다음 날 첫머리로 넘긴다
    for k in range(len(days) - 1):
        last, nxt = (days[k]["parts"] or [None])[-1], days[k + 1]["parts"]
        if (last and len(days[k]["parts"]) > 1 and not units[last["unit"]].get("whole") and last["from"] == 1
                and last["to"] - last["from"] + 1 < 5 and nxt and nxt[0]["unit"] == last["unit"]):
            days[k]["parts"].pop()
            w = units[last["unit"]].get("weight", 1) * (last["to"] - last["from"] + 1)
            days[k]["effort"] -= w
            days[k + 1]["effort"] += w
            nxt[0]["from"] = last["from"]
    for d in days:
        d["effort"] = round(d["effort"], 1)
    return [d for d in days if d["parts"]]


def plan_daily(units, start, rest, per_day):
    total = sum(u["count"] * u.get("weight", 1) for u in units)
    return split(units, study_dates(start, rest, n=math.ceil(total / per_day)))
