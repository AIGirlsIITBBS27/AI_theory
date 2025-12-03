
# **README - Group 11**
---
## **Module 1**
---
## **Module 2**
---
## **Module 3**

# **Using GraphPlan**
## **Overview**
This is the implementation of **GraphPlan** for Module 3 of Group 11's project:
```text
├── graphplan.py               # Main driver file that runs GraphPlan
├── planning_graph.py          # Planning graph construction + mutex logic
├── parser.py                  # JSON parser + literal normalization
├── domain.json                # Action definitions (preconditions, effects)
├── problem.json               # Initial state + goal definition
├── final_plan.txt             # Saved output plan after running GraphPlan
└── README.md                  
```

## **How to Run the Code**

### **Prerequisites**

* Python 3.8+
* No external libraries required (pure Python)

### **Run Command**

```
python3 graphplan.py
```

This loads `domain.json` and `problem.json`, builds the Planning Graph, performs backward plan extraction, and stores the output in:

```
final_plan.txt
```

---

# **Using Partial Order Planning**

## **Overview**
This is the implementation of **POP** for Module 3 of Group 11's project:
```text
├── pop_planner.py             # Main driver, STRIPS operators, and Planner logic
├── pop_outputs/               # Auto-generated folder for outputs
│   ├── plan_<emotion>.png     # Visual graph of the plan
│   └── plan_<emotion>.json    # Machine-readable plan data
└── README.md                
```

## **How to Run the Code**

### **Prerequisites**

* Python 3.8+
* External Libraries:
```Bash
pip install networkx matplotlib
```

### **Run Command**

```
python3 pop.py
```

#### Execution Steps
1. Run the script.
2. Enter the target emotions when prompted (e.g., confused, sad).
3. The script performs goal regression to build a valid plan.
4. Outputs are automatically saved in the pop_outputs/ directory:
    * PNG: A flowchart visualization of the conversation strategy.
    * JSON: The data structure containing steps, ordering constraints, and causal links.

---
## **Module 4**

# Using RL-Based Emotion Adaptive Tutor

## Module Goal
The aim of this module is:

> **To train a simple RL agent that learns how to choose better teaching actions depending on the student's emotional state.**
This makes the tutor more adaptive and personalized.

## Overview
This is the implementation of the **Reinforcement Learning (Q-Learning)** based emotion-adaptive module for our project.
```text
├── RL_FINAL_1.ipynb
├── q_table.csv # Saved Q-table after training (if generated)
└── README.md                 
```

## **How to Run the Code**

### **Prerequisites**
- Python 3.8+
- Install required libraries:

### **Run Command**
pip install numpy matplotlib
```
jupyter notebook RL_FINAL_1.ipynb
```

Inside the notebook:
1. Emotion states are loaded.
2. RL environment is created.
3. Q-learning agent is trained.
4. Training graphs are generated.
5. A test case is executed to check the agent’s final action.

```

output:
- Q-table after training.
- Reward-vs-episode graphs.
- Final chosen action for a test emotion (e.g., “boredom” or “anger”).
- Optional: saved file- `qtable.csv`.
---
## **Module 5**
---
