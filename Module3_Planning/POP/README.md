# 📘 POP Planner Module

## ⭐ Overview
This module implements a **Partial Order Planner (POP)** designed to generate conversational strategies for an emotion-aware mentoring chatbot.

Unlike linear planners that force a strict step-by-step sequence (e.g., Step 1 → Step 2 → Step 3), this POP algorithm creates a **flexible plan** (a Directed Acyclic Graph). It identifies the necessary conversational moves to address a student's emotion (e.g., "confused", "sad") while leaving the execution order flexible where strict dependencies do not exist.

### ❓ Why POP Instead of GraphPlan?
While algorithms like **GraphPlan** are efficient at finding the shortest path in a state-space, **POP (Partial Order Planning)** is superior for conversational agents for three key reasons:

1.  **Least Commitment Strategy:** POP only adds ordering constraints when absolutely necessary (e.g., you *must* "greet" before you "acknowledge"). If two actions (like "guide" and "boost confidence") do not depend on each other, POP leaves them unordered.
2.  **Execution Flexibility:** In a real conversation, the user might interrupt or shift topics. A partial order allows the chatbot to execute available steps in whatever order feels most natural dynamically, rather than breaking a rigid linear chain.
3.  **Plan Space Search:** POP searches through the space of *plans* (refining a plan), whereas GraphPlan searches through the space of *states*. This allows POP to easily explain *why* a step exists via **causal links** (e.g., "I am probing because I need to clarify the user's confusion").

---

# 📂 Module Structure

The project currently consists of a single self-contained script and an auto-generated output folder:

```text
.
├── pop_planner.py          # Main logic: Operators, Planner, and Visualization
└── pop_outputs/            # Generated output folder (created on run)
    ├── plan_confused.png   # Visual graph of the plan
    ├── plan_confused.json  # Machine-readable plan data
    └── ...
```

🧩 How It Works1. STRIPS-Style OperatorsThe planner uses a simplified STRIPS definition with no delete effects (monotonic logic). This ensures that once a conversational goal is achieved (e.g., greeted), it is not undone by subsequent actions.Preconditions (pre): What must be true before this action can happen.Add Effects (add): What becomes true after this action.2. Emotion-to-Goal MappingThe planner receives an emotion input and looks up the required final states (Goals).EmotionGoals (End State)Confusedclarified, guided, boosted_confidenceSadacknowledged, comforted, supported, validatedAngryacknowledged, listened, respected3. The Algorithm (Goal Regression)Start: Initialize with a Finish operator containing the emotion's goals.Open Goals: Identify preconditions that are not yet met.Search: Find an operator (Producer) that adds the required effect.Link: Create a Causal Link from the Producer to the Consumer.Order: Add ordering constraints (Start < Producer < Finish).Transitive Reduction: Simplifies the final graph by removing redundant edges for cleaner visualization.🚀 Installation & Usage1. Install DependenciesYou need networkx for graph logic and matplotlib for rendering the plan visualization.Bashpip install networkx matplotlib
2. Run the PlannerExecute the script directly from your terminal:Bashpython pop_planner.py
3. Input EmotionsWhen prompted, enter one or more emotions separated by commas.Example Input:PlaintextEnter emotions (comma-separated). Example:
confused, sad, angry

Emotions: confused, anxious
📦 Output InterpretationFor every emotion processed, the script generates two files in the pop_outputs/ directory.1. Visualization (.png)A visual representation of the Directed Acyclic Graph (DAG).Green Node: Start State.Red Node: Finish (Goals Met).Blue Nodes: Conversational Actions.Arrows: Ordering constraints (Action A must happen before Action B).2. Plan Data (.json)A machine-readable file useful for integrating with the chatbot backend.steps: List of all actions selected.ordering: Constraints formatted as [before_step, after_step].causal_links: Explanations formatted as [producer, requirement, consumer].Example JSON Snippet:JSON{
  "steps": ["Start", "greet", "acknowledge", "probe", "Finish"],
  "ordering": [
    ["Start", "greet"],
    ["greet", "acknowledge"],
    ["acknowledge", "probe"]
  ],
  "causal_links": [
    ["greet", "greeted", "acknowledge"],
    ["acknowledge", "acknowledged", "probe"]
  ]
}
🛠️ Extending the PlannerAdding New ActionsTo add new conversational moves, open pop_planner.py, locate the OPS list, and append a new Op:PythonOPS = [
    # ... existing ops ...
    Op("tell_joke", pre=["acknowledged"], add=["humor_injected"]),
]
Adding New EmotionsTo support new emotions, update the EMOTION_GOALS dictionary in pop_planner.py:PythonEMOTION_GOALS = {
    # ... existing emotions ...
    "bored": ["humor_injected", "engaged"]
}
