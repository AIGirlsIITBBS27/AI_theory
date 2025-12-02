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
