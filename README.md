
# **README - Group 11**
---

## **Module 1**
**Bayesian Network–Based Emotional State Classifier**
This project implements a **Bayesian Network (BN)** to classify user emotional–cognitive states using four linguistic signals:
- **neg** (negative sentiment)
- **hes** (hesitation)
- **fru** (frustration)
- **hing** (high-intensity negative cue)

The model predicts four states:
- **Slightly_Stressed**
- **Low_Motivation**
- **Highly_Anxious**
- **Overthinking**
## **Dataset Preparation**

Before building the Bayesian model, the original training dataset was downloaded and converted .txt file into a clean train_dataset_for_NN_model.csv.
   
**Run command**
```
python3 bayes_model.py
```
this loads an bn_cpts.json and all_predictions.csv
  1. **bn_cpts.json** – contains priors + CPTs (Conditional Probability Tables)  
  2. **all_predictions.csv** – contains the final emotional-state predictions

###  Workflow
```
train_dataset_for_NN_model.csv
↓
Signal Extraction (preprocess.py)
↓
CPT & Prior Calculation (from dataset statistics)
↓
bn_cpts.json (Bayesian model knowledge: priors + CPTs)
↓
Bayesian Inference (bayes_model.py)
↓
all_predictions.csv (final prediction results)
```
---

## **Module 2**
**Choosing the Best Reply Strategy using Search Algorithms**
The goal is to find use a uniformed search and one informed search to decide the next strategy.
Search Algorithm used:
  1.BFS- Uninformed search method
  2.A*- informed search

**Run command**
```
python3 search.py
```
In the current implementation, input emotion probabilities are hard-coded. However, in the full system these values will be produced by Module 1 using a Bayesian Network.
Module 2 uses these probabilities to evaluate and search for the most suitable reply strategy.
Among the implemented search methods, A* is the preferred algorithm because it is informed by emotional cost, making it more accurate and context-aware than BFS.


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
```
pip install numpy matplotlib
jupyter notebook RL_FINAL_1.ipynb
```

Inside the notebook:
1. Emotion states are loaded.
2. RL environment is created.
3. Q-learning agent is trained.
4. Training graphs are generated.
5. A test case is executed to check the agent’s final action.

output:
- Q-table after training.
- Reward-vs-episode graphs.
- Final chosen action for a test emotion (e.g., “boredom” or “anger”).
- Optional: saved file- `qtable.csv`.
  
## **Module 5**

# LLM BASED QUESTION ANSWERING

## Module Goal
To create an intelligent dialogue system that uses a large language model (LLM) to understand and respond based on the user’s emotional state, allowing more personalized and context-aware conversations.


## Overview
The dialogue system is built to seamlessly support Hinglish, combining Hindi and English in a conversational manner that feels natural to users.
```
├── dialogue_system.py
├── emotion_classifier.py
├── response_generator.py
├── config.yaml
├── requirements.txt
└── README.md
```

## **How to Run the Code**

### **Prerequisites**

- Python 3.8+
- Install required libraries:

### **Run Command**

```
pip install transformers
pip install torch

```
##  **How the System Works**

1. **User Input →** Hinglish sentence  
2. **Emotion Classifier →** Extracts signals, applies Bayesian model, final refinement using LLM  
3. **LLM Response Generator →** Creates personalized text based on predicted emotional state  
4. **Output →** Emotion-aware, meaningful Hinglish response

**Example:**

**User:**  
"Bhai, aaj mann nahi lag raha."

**Output:**  
Response → "Lagta hai energy thodi kam hai. Chalo, step by step start karte hain?"

              
