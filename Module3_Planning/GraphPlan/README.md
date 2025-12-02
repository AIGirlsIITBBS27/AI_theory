# **README.md — Group 11**
### **Module 3: Planning the Next Few Conversation Steps using GraphPlan**

---

## **Project Overview**

This contains implementation of **GraphPlan** for Module 3 of Group 11's project:
```text
├── graphplan.py               # Main driver file that runs GraphPlan
├── planning_graph.py          # Planning graph construction + mutex logic
├── parser.py                  # JSON parser + literal normalization
├── domain.json                # Action definitions (preconditions, effects)
├── problem.json               # Initial state + goal definition
├── final_plan.txt             # Saved output plan after running GraphPlan
└── README.md                  
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

This loads `domain.json` and `problem.json`, builds the Planning Graph, performs backward plan extraction, and stores the output in:

```
final_plan.txt
```

---

## **Author and Contributor**
Justa Tirkey\
21CS02011






