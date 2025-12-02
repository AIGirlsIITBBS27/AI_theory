# **README.md — Group 11 (Module: GraphPlan Planning)**
### **Module 3: Planning the Next Few Conversation Steps using GraphPlan**

---

## **Project Overview**

This repository contains implementation of **GraphPlan** for Module 3 of Group 11's project:
```text
├── graphplan.py               # Main driver file that runs GraphPlan  :contentReference[oaicite:0]{index=0}
├── planning_graph.py          # Planning graph construction + mutex logic  :contentReference[oaicite:1]{index=1}
├── parser.py                  # JSON parser + literal normalization  :contentReference[oaicite:2]{index=2}
├── domain_2.json              # Action definitions (preconditions, effects)  :contentReference[oaicite:3]{index=3}
├── problem_2.json             # Initial state + goal definition  :contentReference[oaicite:4]{index=4}
├── final_plan.txt             # Saved output plan after running GraphPlan  :contentReference[oaicite:5]{index=5}
└── README.md                  # (this file)
```
---

## **How to Run the Code**

### **Prerequisites**

* Python 3.8+
* No external libraries required (pure Python)

### **Run Command**

```
python3 graphplan.py
```

This loads `domain_2.json` and `problem_2.json`, builds the Planning Graph, performs backward plan extraction, and stores the output in:

```
final_plan.txt
```

---

## **Author and Contributor**
Justa Tirkey\
21CS02011



