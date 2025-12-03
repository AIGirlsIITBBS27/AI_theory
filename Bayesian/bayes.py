#Anjali Kashide
!pip install pandas chardet

import pandas as pd
import requests, io, chardet


url = "https://kristina.machova.website.tuke.sk/useful/DATA%20for%20EMOTION%20DETECTION/train%20dataset%20for%20NN%20model.txt"
r = requests.get(url)
r.raise_for_status()

enc = chardet.detect(r.content)
encoding = enc['encoding']
print("Detected encoding:", encoding)


data_preview = r.text.splitlines()[:10]
print("File preview:")
for line in data_preview:
    print(line)

df = pd.read_csv(io.StringIO(r.text), sep=";", header=None, encoding=encoding)


df.columns = ["Text", "Emotion"]

df.to_csv("train_dataset_for_NN_model.csv", index=False)
print(" Saved as train_dataset_for_NN_model.csv")
df.head()

from google.colab import files

files.download('train_dataset_for_NN_model.csv')

from google.colab import files

files.download('/content/student_emotion_bn_dataset.csv')

# 1) Install / import
!pip install -q graphviz
import re, math, json
from collections import Counter, defaultdict
import pandas as pd
import numpy as np
from IPython.display import display, HTML
import matplotlib.pyplot as plt
import networkx as nx
import graphviz
from google.colab import files
print('/content/train_dataset_for_NN_model.csv')
uploaded = files.upload()

if len(uploaded)==0:
    raise SystemExit("No file uploaded. Re-run the cell and upload your CSV.")
csv_fname = list(uploaded.keys())[0]
print("Loaded:", csv_fname)

df = pd.read_csv(csv_fname).dropna(subset=['Text']).reset_index(drop=True)
print("Dataset rows:", len(df))
display(df.head())


NEG_WORDS = set([
    "stressed","stress","anxious","anxiety","sad","depressed","upset","worry","worried","hate",
    "angry","frustrat","panic","panicking","scared","afraid","lonely","tired","lost","hopeless",
    "can't","cant","can't","failure","failed","fail"
])
HINDI_WORDS = set(["yaar","bahut","nahi","kya","acha","achha","yaarr","kal","pata","problem","naam","mera","tum","kuch","nahi","hoot","nhi"])

hesitation_patterns = [
    r"\.\.\.",
    r"\buh+\b",
    r"\bum+\b",
    r"(.)\1{2,}",
]

frustration_patterns = [
    r"!!!+",
    r"\b(fuck|shit|damn|crap)\b",
    r"\b(can't|cant|cannot|won't|wont)\b",
    r"\bwhy\b.*\bnot\b",
    r"\bnot fair\b",
]


def has_negative(text):
    t = text.lower()

    for w in NEG_WORDS:
        if re.search(r"\b" + re.escape(w) + r"\b", t):
            return True
    return False

def has_hesitation(text):
    t = text.lower()
    for p in hesitation_patterns:
        if re.search(p, t):
            return True
    return False

def has_frustration(text):
    t = text.lower()
    for p in frustration_patterns:
        if re.search(p, t):
            return True

    if t.count('!') >= 2:
        return True
    return False

def has_hinglish(text):
    t = text.lower()

    tokens = re.findall(r"\w+", t)
    for w in HINDI_WORDS:
        if w in tokens:
            return True
    return False


df['neg'] = df['Text'].astype(str).apply(has_negative)
df['hes'] = df['Text'].astype(str).apply(has_hesitation)
df['fru'] = df['Text'].astype(str).apply(has_frustration)
df['hing'] = df['Text'].astype(str).apply(has_hinglish)

print("Signal prevalences:")
display(df[['neg','hes','fru','hing']].mean().round(4))


map_to_state = {
    'fear': 'Highly_Anxious',
    'anger': 'Highly_Anxious',
    'sadness': 'Low_Motivation',
    'joy': 'Slightly_Stressed',
    'surprise': 'Overthinking',
    'love': 'Overthinking'
}


if 'Emotion' not in df.columns:
    raise SystemExit("CSV must have an 'Emotion' column. Modify file or column name accordingly.")
df['Emotion'] = df['Emotion'].astype(str).str.lower().str.strip()
df['State'] = df['Emotion'].map(map_to_state)
initial_len = len(df)
df = df.dropna(subset=['State']).reset_index(drop=True)
print(f"Dropped {initial_len - len(df)} rows due to unmapped emotion labels.")
print("State counts:")
display(df['State'].value_counts())


signals = ['neg','hes','fru','hing']
state_counts = df['State'].value_counts().to_dict()
state_priors = {s: state_counts.get(s,0)/len(df) for s in state_counts}

cpt = {}
for s in state_counts:
    sub = df[df['State']==s]
    probs = {}
    for sig in signals:
        probs[sig] = sub[sig].mean()
    cpt[s] = probs

print("\nLearned State priors (from dataset):")
display(pd.Series(state_priors).round(4))
print("\nLearned CPTs P(signal=True | state):")
display(pd.DataFrame(cpt).T.round(4))


def posterior_from_text(text, cpt, state_priors):

    obs = {
        'neg': has_negative(text),
        'hes': has_hesitation(text),
        'fru': has_frustration(text),
        'hing': has_hinglish(text)
    }
    unnorm = {}
    for s, prior in state_priors.items():

        p = prior if prior>0 else 1e-9
        for sig, val in obs.items():
            p_sig = cpt[s][sig]

            p_sig = np.clip(p_sig, 1e-6, 1-1e-6)
            p *= (p_sig if val else (1-p_sig))
        unnorm[s] = p
    Z = sum(unnorm.values())
    if Z == 0:

        return {s: 1/len(unnorm) for s in unnorm}
    post = {s: unnorm[s]/Z for s in unnorm}
    return {'observed_signals': obs, 'posterior': post}


print("\nBayesian Network structure (text):")
print("Parents (evidence nodes) -> Child (EmotionalState)")
print("neg, hes, fru, hing  -> EmotionalState")


G = nx.DiGraph()
G.add_nodes_from(['neg','hes','fru','hing','EmotionalState'])
for parent in ['neg','hes','fru','hing']:
    G.add_edge(parent, 'EmotionalState')

pos = {'neg':(-1,1),'hes':(-1,0),'fru':(-1,-1),'hing':(-1,-2),'EmotionalState':(1, -0.5)}
plt.figure(figsize=(6,4))
nx.draw(G, pos=pos, with_labels=True, node_size=2000, node_color='lightblue', arrowsize=20)
plt.title("BN Structure")
plt.axis('off')
plt.show()


test_message = "I'm really stressed about exams... can't sleep yaar, it's too much and I'm panicking."
print("\nTest message:")
print(test_message)

res = posterior_from_text(test_message, cpt, state_priors)
print("\nDetected signals for test message:")
display(res['observed_signals'])
print("\nPosterior probabilities P(State | observed signals):")
display(pd.Series(res['posterior']).sort_values(ascending=False).round(4))


print("\n--- BN CPTs (P(signal=True | state)) ---")
print(json.dumps(cpt, indent=2))
print("\n--- State priors (from dataset) ---")
print(json.dumps(state_priors, indent=2))


def infer_row(row):
    msg = row['Text']
    out = posterior_from_text(msg, cpt, state_priors)

    post = out['posterior']
    best_state = max(post, key=post.get)
    return pd.Series([best_state, post[best_state], json.dumps(out['observed_signals'])])

df_preds = df.copy()
df_preds[['PredictedState','PredProb','DetectedSignals']] = df_preds.apply(infer_row, axis=1)
print("\nSample predictions on dataset:")
display(df_preds[['Text','Emotion','State','PredictedState','PredProb']].head())


with open('bn_cpts.json', 'w') as f:
    json.dump({'priors': state_priors, 'cpt': cpt}, f, indent=2)


df_preds.to_csv('all_predictions.csv', index=False)

print("\nSaved 'bn_cpts.json' (for model parameters) and 'all_predictions.csv' (full dataset results) in the Colab working directory.")
print("You can download them using the Files panel or with the command below:")

from google.colab import files
files.download('all_predictions.csv')

from google.colab import files

files.download('/content/bn_cpts.json')

from google.colab import files

files.download('/content/sample_predictions.csv')

import pandas as pd
df = pd.read_csv('/content/train_dataset_for_NN_model.csv')
print(df.shape)
print(df.head())
