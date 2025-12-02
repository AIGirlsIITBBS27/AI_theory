# graphplan.py
from parser import load_domain, load_problem
from itertools import product, combinations
from planning_graph import PlanningGraph, ActionObj
from itertools import product
import sys


def print_level_info(pg):
    L = len(pg.literal_levels)
    for i in range(L):
        print(f"\n=== Literal Level {i} ===")
        lits = sorted(pg.literal_levels[i])
        print("Literals:", lits)
        lm = pg.literal_mutex[i] if i < len(pg.literal_mutex) else set()
        if lm:
            print("Literal Mutex Pairs:")
            for p,q in sorted(lm):
                print(f"  {p}  <->  {q}")
        else:
            print("Literal Mutex Pairs: None or not computed for this level")

        if i < len(pg.action_levels):
            print(f"\n--- Action Level {i} ---")
            acts = pg.action_levels[i]
            print("Actions:", [a.name for a in acts])
            am = pg.action_mutex[i]
            if am:
                print("Action Mutex Pairs:")
                # only unique pairs once
                seen = set()
                for a,b in sorted(am):
                    if (b,a) in seen:
                        continue
                    seen.add((a,b))
                    print(f"  {a}  <->  {b}")
            else:
                print("Action Mutex Pairs: None")

def extract_solution(pg, goals, level, memo):
    key = (frozenset(goals), level)
    if key in memo:
        return None
    if level == 0:
        if goals.issubset(pg.literal_levels[0]):
            return []
        else:
            memo.add(key)
            return None

    actions = pg.action_levels[level - 1]
    amutex = pg.action_mutex[level - 1]

    supports = []
    for g in goals:
        s = [a for a in actions if g in a.post]
        supports.append(s)

    if any(len(s)==0 for s in supports):
        memo.add(key)
        return None

    for combo in product(*supports):
        action_set = set(combo)
        bad = False
        for a1 in action_set:
            for a2 in action_set:
                if a1 is a2:
                    continue
                if (a1.name, a2.name) in amutex:
                    bad = True
                    break
            if bad:
                break
        if bad:
            continue

        new_goals = set()
        for a in action_set:
            new_goals |= set(a.pre)

        subplan = extract_solution(pg, new_goals, level - 1, memo)
        if subplan is not None:
            step = [a.name for a in action_set]
            return subplan + [step]

    memo.add(key)
    return None

def graphplan(domain_path="domain.json", problem_path="problem.json", verbose=True):
    domain = load_domain(domain_path)
    init, goal = load_problem(problem_path)
    pg = PlanningGraph(init, domain)

    level = 0
    if verbose:
        print("Initial literals:", sorted(pg.literal_levels[0]))
        print("Goals:", sorted(goal))

    while True:
        if goal.issubset(pg.literal_levels[level]):
            all_non_mutex = True
            for p,q in combinations(sorted(goal), 2):
                if (p,q) in pg.literal_mutex[level]:
                    all_non_mutex = False
                    break
            if all_non_mutex:
                memo = set()
                plan = extract_solution(pg, goal, level, memo)
                if plan is not None:
                    if verbose:
                        print_level_info(pg)
                        print("\n=== Final Plan (from time 0 ...): ===")
                    return plan, pg
        if pg.levels_off():
            if verbose:
                print_level_info(pg)
                print("\nGraph leveled off - no solution.")
            return None, pg

        pg.expand()
        level += 1
        if verbose:
            print(f"\n--- Expanded to level {level} ---")

if __name__ == "__main__":
    plan, pg = graphplan("domain_2.json", "problem_2.json", verbose=True)

    output_file = "final_plan.txt"

    if plan is None:
        with open(output_file, "w") as f:
            f.write("FINAL: IMPOSSIBLE\n")
        print(f"\nFinal result written to {output_file}")
    else:
        with open(output_file, "w") as f:
            f.write("FINAL PLAN (each time-step):\n")
            for t, step in enumerate(plan):
                f.write(f"t={t}: {step}\n")

        print(f"\nFinal plan written to {output_file}")

