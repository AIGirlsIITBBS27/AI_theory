# **README.md — Group 11**
### **Module 3: Planning the Next Few Conversation Steps using  Partial Order Planning**

---

## **Project Overview**

This is the implementation of **POP** for Module 3 of Group 11's project:
```text
├── pop_planner.py             # Main driver, STRIPS operators, and Planner logic
├── pop_outputs/               # Auto-generated folder for outputs
│   ├── plan_<emotion>.png     # Visual graph of the plan
│   └── plan_<emotion>.json    # Machine-readable plan data
└── README.md                
```
---

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

## **Author and Contributor**
Likhitha Malla\
21CS02009



