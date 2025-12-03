
"""

Module 2: Strategy Selection via Search (A*)

by Annesha Guha 25AI06015 MTECH-AI
"""


from collections import deque
from queue import PriorityQueue
from typing import Dict, List, Tuple, Optional


GRAPH: Dict[str, List[str]] = {
    "Start": [
        "ExplainCalmlyWithExample",
        "EncourageHope",
        "AskGuidingQuestion",
        "RemindProgress",
    ],
    "ExplainCalmlyWithExample": ["Goal"],
    "EncourageHope": ["Goal"],
    "AskGuidingQuestion": ["Goal"],
    "RemindProgress": ["Goal"],
    "Goal": []
}


emotion_probs: Dict[str, float] = {
    "SlightStress": 0.10,
    "HighAnxiety": 0.20,
    "Overthinking": 0.25,
    "LowMotivation": 0.45,
}

def detect_emotion(probabilities: Dict[str, float]) -> str:
    return max(probabilities, key=probabilities.get)

detected_emotion = detect_emotion(emotion_probs)


def costs_from_top_emotion(top_emotion: str) -> Dict[str, float]:
    table = {
        "LowMotivation": {
            "ExplainCalmlyWithExample": 3.0,
            "EncourageHope": 1.0,
            "AskGuidingQuestion": 4.0,
            "RemindProgress": 2.0,
        },
        "HighAnxiety": {
            "ExplainCalmlyWithExample": 1.0,
            "EncourageHope": 3.0,
            "AskGuidingQuestion": 3.0,
            "RemindProgress": 2.0,
        },
        "Overthinking": {
            "ExplainCalmlyWithExample": 2.0,
            "EncourageHope": 2.0,
            "AskGuidingQuestion": 3.0,
            "RemindProgress": 1.0,
        },
        "SlightStress": {
            "ExplainCalmlyWithExample": 2.0,
            "EncourageHope": 2.0,
            "AskGuidingQuestion": 2.0,
            "RemindProgress": 1.0,
        },
    }
    return table.get(top_emotion, {
        "ExplainCalmlyWithExample": 2.0,
        "EncourageHope": 2.0,
        "AskGuidingQuestion": 2.0,
        "RemindProgress": 2.0,
    })


STRATEGY_COSTS = costs_from_top_emotion(detected_emotion)


def bfs(graph: Dict[str, List[str]], start: str, goal: str) -> Optional[List[str]]:
    q = deque([(start, [start])])
    seen = {start}
    while q:
        node, path = q.popleft()
        if node == goal:
            return path
        for nbr in graph.get(node, []):
            if nbr not in seen:
                seen.add(nbr)
                q.append((nbr, path + [nbr]))
    return None


def edge_cost(u: str, v: str) -> float:
    """
    Edge costs:
      - Start -> Strategy: small uniform cost (1.0)
      - Strategy -> Goal: strategy-specific emotional cost
      - Others: 0 by default
    """
    if u == "Start" and v in STRATEGY_COSTS:
        return 1.0
    if v == "Goal" and u in STRATEGY_COSTS:
        return STRATEGY_COSTS[u]
    return 0.0

def heuristic(n: str) -> float:
    """
    Heuristic:
      - At 'Start': optimistic estimate = min strategy cost
      - At a Strategy node: h = its emotional cost to Goal
      - At Goal: 0
    """
    if n == "Start":
        return min(STRATEGY_COSTS.values())
    if n in STRATEGY_COSTS:
        return STRATEGY_COSTS[n]
    return 0.0

def a_star(graph: Dict[str, List[str]], start: str, goal: str) -> Tuple[Optional[List[str]], Optional[float]]:
    pq: PriorityQueue = PriorityQueue()
    pq.put((0.0, start, [start], 0.0))  # (f, node, path, g)
    visited = set()

    while not pq.empty():
        f, node, path, g = pq.get()
        if node == goal:
            return path, g
        if node in visited:
            continue
        visited.add(node)

        for nbr in graph.get(node, []):
            step = edge_cost(node, nbr)
            new_g = g + step
            new_f = new_g + heuristic(nbr)
            pq.put((new_f, nbr, path + [nbr], new_g))

    return None, None

goal_node = "Goal"

bfs_path = bfs(GRAPH, "Start", goal_node)
a_star_path, a_star_cost = a_star(GRAPH, "Start", goal_node)

bfs_selected = bfs_path[1] if bfs_path and len(bfs_path) > 1 else None
a_star_selected = a_star_path[1] if a_star_path and len(a_star_path) > 1 else None


print("--------- Module 2: Strategy Selection ---------\n")
print(f"Emotion probabilities (from BN): {emotion_probs}")
print(f"Detected emotion (argmax): {detected_emotion}\n")

print("BFS (uninformed) result:")
print(f"  Path: {bfs_path}")
print(f"  Selected next strategy: {bfs_selected}\n")

print("A* (informed by detected emotion) result:")
print(f"  Path: {a_star_path}")
print(f"  Total path cost: {a_star_cost}")
print(f"  Selected next strategy: {a_star_selected}\n")

print("Note:")
print("BFS ignores emotional costs and returns the first available strategy by graph order.")
print("A* uses emotion-aware costs to choose the most suitable next strategy for the current student.")
