# planning_graph.py
from itertools import combinations

class ActionObj:
    def __init__(self, name, pre, post, is_noop=False):
        self.name = name
        self.pre = frozenset(pre)
        self.post = frozenset(post)
        self.is_noop = is_noop

    def __repr__(self):
        return f"{self.name}"

class PlanningGraph:
    def __init__(self, init_literals, actions):
        # literal_levels: list of sets of canonical literals (strings)
        self.literal_levels = [set(init_literals)]
        # action_levels: list of lists of ActionObj
        self.action_levels = []
        # mutex sets:
        # action_mutex[i] is a set of (a1.name, a2.name) pairs (ordered tuples)
        self.action_mutex = []
        # literal_mutex[i] is a set of (p,q) pairs of literals (strings)
        self.literal_mutex = [set()]
        # master action templates from domain (list of dicts: name, pre, post)
        self.domain_actions = actions

    def expand(self):
        prev_literals = self.literal_levels[-1]
        # 1) A-level: actions whose preconditions are all satisfied
        level_actions = []
        for a in self.domain_actions:
            if set(a["pre"]).issubset(prev_literals):
                level_actions.append(ActionObj(a["name"], a["pre"], a["post"]))

        # 2) No-op actions for each literal present
        for lit in prev_literals:
            noop_name = f"NoOp({lit})"
            level_actions.append(ActionObj(noop_name, [lit], [lit], is_noop=True))

        self.action_levels.append(level_actions)

        # 3) Compute action mutexes for this level
        amutex = set()
        for a1, a2 in combinations(level_actions, 2):
            if self._action_mutex(a1, a2):
                amutex.add((a1.name, a2.name))
                amutex.add((a2.name, a1.name))
        self.action_mutex.append(amutex)

        # 4) L-level: union of all posts of actions in this level
        new_literals = set()
        for a in level_actions:
            new_literals |= set(a.post)
        self.literal_levels.append(new_literals)

        # 5) Compute literal mutexes for the new literal level
        lmutex = set()
        for p, q in combinations(sorted(new_literals), 2):
            if self._literal_mutex(p, q, level_actions, amutex):
                lmutex.add((p, q))
                lmutex.add((q, p))
        self.literal_mutex.append(lmutex)

    def _action_mutex(self, a1, a2):
        # 1) Inconsistent effects: one posts p and other posts ¬p
        for p in a1.post:
            if self._neg(p) in a2.post:
                return True
        for p in a2.post:
            if self._neg(p) in a1.post:
                return True

        # 2) Interference: one posts negation of other's pre (or vice versa)
        for p in a1.post:
            if self._neg(p) in a2.pre:
                return True
        for p in a2.post:
            if self._neg(p) in a1.pre:
                return True

        # 3) Competing needs: some pair of preconditions are mutex at prev literal level
        prev_lmutex = self.literal_mutex[-1]
        for p in a1.pre:
            for q in a2.pre:
                if (p, q) in prev_lmutex:
                    return True

        return False

    def _literal_mutex(self, p, q, actions_in_level, amutex):
        # 1) Negation mutex: p == ¬q
        if p == self._neg(q) or q == self._neg(p):
            return True

        # 2) Inconsistent support: every pair of supporters are mutex
        supporters_p = [a for a in actions_in_level if p in a.post]
        supporters_q = [a for a in actions_in_level if q in a.post]

        if not supporters_p or not supporters_q:
            # If either has no supporters at this level -> unreachable -> mutex
            return True

        for ap in supporters_p:
            for aq in supporters_q:
                if (ap.name, aq.name) not in amutex:
                    # found a supporting pair that is NOT mutex => p and q are not mutex
                    return False
        # all supporting pairs are mutex -> inconsistent support
        return True

    def levels_off(self):
        if len(self.literal_levels) < 2:
            return False
        return (self.literal_levels[-1] == self.literal_levels[-2]
                and self.literal_mutex[-1] == self.literal_mutex[-2])

    @staticmethod
    def _neg(lit):
        # lit is canonical like "P" or "¬P"; return negation in canonical form
        if lit.startswith("Not"):
            return lit[1:]
        else:
            return "Not" + lit
