import json
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
import os

class Op:
    def __init__(self, name, pre, add, delete=None):
        self.name = name
        self.pre = set(pre)
        self.add = set(add)
        self.delete = set(delete) if delete else set()

    def __repr__(self):
        return f"Op({self.name})"

OPS = [
    Op("greet", pre=[], add=["greeted"]),
    Op("acknowledge", pre=["greeted"], add=["acknowledged"]),
    Op("comfort", pre=["acknowledged"], add=["comforted"]),
    Op("probe", pre=["acknowledged"], add=["clarified"]),
    Op("guide", pre=["clarified","acknowledged"], add=["guided"]),
    Op("boost_confidence", pre=["comforted"], add=["boosted_confidence"]),
    Op("boost_confidence_after_guide", pre=["guided"], add=["boosted_confidence"]),
    Op("validate", pre=["acknowledged"], add=["validated"]),
    Op("support", pre=["acknowledged"], add=["supported"]),
    Op("reassure", pre=["acknowledged"], add=["reassured"]),
    Op("encourage", pre=["acknowledged"], add=["encouraged"]),
    Op("motivate", pre=["acknowledged"], add=["motivated"]),
    Op("empower", pre=["acknowledged"], add=["empowered"]),
    Op("inspire", pre=["acknowledged"], add=["inspired"]),
    Op("connect", pre=["acknowledged"], add=["connected"]),
    Op("accept", pre=["acknowledged"], add=["accepted"]),
    Op("listen", pre=["greeted"], add=["listened"]),
    Op("understand", pre=["acknowledged"], add=["understood"]),
    Op("respect", pre=["acknowledged"], add=["respected"]),
    Op("value", pre=["acknowledged"], add=["valued"]),
    Op("appreciate", pre=["acknowledged"], add=["appreciated"]),
    Op("safe_action", pre=["acknowledged"], add=["safe"]),
]

EMOTION_GOALS = {
    "confused": ["clarified", "guided", "boosted_confidence"],
    "overwhelmed": ["acknowledged", "reassured", "comforted", "boosted_confidence"],
    "anxious": ["acknowledged", "reassured", "comforted", "boosted_confidence"],
    "stressed": ["acknowledged", "reassured", "comforted", "boosted_confidence"],
    "frustrated": ["acknowledged", "understood", "clarified"],
    "demotivated": ["encouraged", "motivated", "boosted_confidence"],
    "bored": ["guided", "inspired", "boosted_confidence"],
    "sad": ["acknowledged", "comforted", "supported", "validated", "boosted_confidence"],
    "happy": ["validated", "appreciated", "boosted_confidence"],
    "confident": ["validated", "appreciated", "boosted_confidence"],
    "excited": ["validated", "appreciated", "boosted_confidence"],
    "lonely": ["connected", "supported", "comforted", "valued"],
    "angry": ["acknowledged", "listened", "respected"],
    "discouraged": ["encouraged", "supported", "boosted_confidence"],
    "insecure": ["accepted", "reassured", "boosted_confidence"],
    "motivated": ["validated", "empowered", "supported"],
    "determined": ["validated", "empowered", "supported"],
    "focused": ["validated", "supported"],
    "curious": ["guided", "encouraged", "clarified"],
    "inspired": ["empowered", "motivated"],
    "thoughtful": ["validated", "listened"],
    "nostalgic": ["comforted", "connected"],
    "calm": ["validated", "safe"],
    "peaceful": ["validated", "safe"],
    "relaxed": ["validated", "safe"],
    "energized": ["guided", "encouraged"],
    "refreshed": ["guided", "encouraged"],
    "creative": ["validated", "empowered", "supported"],
    "playful": ["validated", "empowered", "supported"],
    "adventurous": ["validated", "empowered", "supported"],
    "grateful": ["validated", "connected"],
    "mindful": ["validated", "safe"],
    "hopeful": ["validated", "encouraged"]
}

class POPPlanner:
    def __init__(self, ops):
        self.ops = ops

    def _find_op_by_add(self, fluent):
        for op in self.ops:
            if fluent in op.add:
                return op
        return None

    def _would_create_cycle(self, ordering, a, b, nodes):
        G = nx.DiGraph()
        G.add_nodes_from(nodes)
        G.add_edges_from(ordering)
        G.add_edge(a, b)
        return not nx.is_directed_acyclic_graph(G)

    def plan(self, init_state, goals, max_steps=100):
        Start = Op("Start", pre=[], add=list(init_state))
        Finish = Op("Finish", pre=goals, add=[])
        steps = [Start, Finish]
        ordering = set([(Start.name, Finish.name)])
        causal_links = []
        open_goals = deque([(Finish, g) for g in Finish.pre if g not in init_state])
        added = 0

        while open_goals and added < max_steps:
            consumer_step, req = open_goals.popleft()

            producer = None
            for s in steps:
                if req in s.add:
                    producer = s
                    break

            if producer is None:
                op_template = self._find_op_by_add(req)
                if op_template is None:
                    return None
                producer = Op(f"{op_template.name}_{added}", op_template.pre, op_template.add)
                steps.insert(-1, producer)
                added += 1
                ordering.add((Start.name, producer.name))
                ordering.add((producer.name, Finish.name))
                for p in producer.pre:
                    if p not in init_state:
                        open_goals.append((producer, p))

            causal_links.append((producer.name, req, consumer_step.name))
            ordering.add((producer.name, consumer_step.name))

        # prune unused steps and ordering
        used = {"Start", "Finish"}
        for p, f, c in causal_links:
            used.add(p); used.add(c)
        pruned_steps = [s for s in steps if s.name in used]
        pruned_ordering = {(a,b) for (a,b) in ordering if a in used and b in used}

        G = nx.DiGraph()
        G.add_nodes_from([s.name for s in pruned_steps])
        G.add_edges_from(pruned_ordering)
        if nx.is_directed_acyclic_graph(G):
            try:
                tr = nx.algorithms.dag.transitive_reduction(G)
                minimal_ordering = set(tr.edges())
            except:
                minimal_ordering = pruned_ordering
        else:
            minimal_ordering = pruned_ordering

        return {
            "steps": [s.name for s in pruned_steps],
            "ordering": minimal_ordering,
            "causal_links": causal_links
        }

def save_plan_json(plan, path):
    data = {
        "steps": plan["steps"],
        "ordering": [list(e) for e in plan["ordering"]],
        "causal_links": [list(cl) for cl in plan["causal_links"]]
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def visualize_plan(plan, path, title):
    G = nx.DiGraph()
    G.add_nodes_from(plan["steps"])
    G.add_edges_from(plan["ordering"])

    if not nx.is_directed_acyclic_graph(G):
        to_remove = []
        for u,v in G.edges():
            if (v,u) in G.edges():
                to_remove.append((v,u))
        G.remove_edges_from(to_remove)

    layers = list(nx.topological_generations(G))
    pos = {}
    y = 0
    for layer in layers:
        x_start = -1.2*(len(layer)-1)/2
        for i,node in enumerate(layer):
            pos[node] = (x_start + 1.2*i, -y)
        y += 2

    colors = []
    for node in G.nodes():
        if node=="Start":
            colors.append("green")
        elif node=="Finish":
            colors.append("red")
        else:
            colors.append("skyblue")

    plt.figure(figsize=(12,7))
    nx.draw(G, pos, with_labels=True, node_size=2600,
            node_color=colors, font_size=10, arrows=True)
    plt.title(title)
    plt.axis("off")
    plt.savefig(path, bbox_inches="tight")
    plt.close()

def main():
    planner = POPPlanner(OPS)

    print("\nEnter emotions (comma-separated). Example:")
    print("confused, sad, angry\n")

    user_input = input("Emotions: ").strip().lower()
    emotions = [e.strip() for e in user_input.split(",") if e.strip()]

    out_dir = "pop_outputs"
    os.makedirs(out_dir, exist_ok=True)

    for emotion in emotions:
        if emotion not in EMOTION_GOALS:
            print(f"\n Unknown emotion: {emotion}")
            continue

        print(f"\n===== Planning for emotion: {emotion} =====")
        goals = EMOTION_GOALS[emotion]

        plan = planner.plan(set(), goals)
        if plan is None:
            print("Plan failed\n")
            continue

        png_path = os.path.join(out_dir, f"plan_{emotion}.png")
        json_path = os.path.join(out_dir, f"plan_{emotion}.json")

        visualize_plan(plan, png_path, f"POP Plan for '{emotion}'")
        save_plan_json(plan, json_path)

        print("Steps:", plan["steps"])
        print("Ordering constraints:", plan["ordering"])
        print("Causal links:", plan["causal_links"])
        print("Saved:", png_path)
        print("Saved:", json_path)

if __name__ == "__main__":
    main()
