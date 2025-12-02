# parser.py
import json

def normalize_literal(raw):
    """Normalize literal forms to canonical form: 'P' or '¬P' (string).
       Accepts raw like 'not P', 'not_P', '!P', '¬P', or 'P'.
    """
    if not isinstance(raw, str):
        raise ValueError("Literal must be a string")
    s = raw.strip()
    # forms: "not X", "not_X", "!X", "¬X"
    if s.startswith("not ") or s.startswith("not_"):
        name = s.split(" ", 1)[-1] if " " in s else s.split("_", 1)[-1]
        return f"¬{name}"
    if s.startswith("!"):
        return f"¬{s[1:].strip()}"
    if s.startswith("¬"):
        return s
    return s

def load_domain(path):
    with open(path, "r") as f:
        data = json.load(f)
    actions = []
    for a in data.get("actions", []):
        name = a["name"]
        pre = [normalize_literal(x) for x in a.get("pre", [])]
        post = [normalize_literal(x) for x in a.get("post", [])]
        actions.append({
            "name": name,
            "pre": pre,
            "post": post
        })
    return actions

def load_problem(path):
    with open(path, "r") as f:
        data = json.load(f)
    init = [normalize_literal(x) for x in data.get("initial_state", [])]
    goal = [normalize_literal(x) for x in data.get("goal", [])]
    return set(init), set(goal)
