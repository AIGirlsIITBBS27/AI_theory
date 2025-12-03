# By ANUSHKA SAXENA 25AI06002 MTECH AI

import random

# Bayesian 
def infer_emotion(user_msg):
    msg = user_msg.lower()
    emotions = {
        "highly_anxious": 0.0,
        "low_motivation": 0.0,
        "slightly_stressed": 0.0,
        "overthinking": 0.0
    }

    if "tired" in msg or "nhi aa rha" in msg or "kuch" in msg:
        emotions["highly_anxious"] = 0.6
        emotions["low_motivation"] = 0.3
    elif "can't" in msg or "fail" or "mujhse nhi hoga" in msg:
        emotions["low_motivation"] = 0.7
    elif "mind" or "kya karu "in msg:
        emotions["overthinking"] = 0.65
    else:
        emotions["slightly_stressed"] = 0.55

    return emotions

def select_strategy(emotions):
    strategy = max(emotions, key=emotions.get)
    mapping = {
        "highly_anxious": "Encourage + Grounding",
        "low_motivation": "Confidence Boost",
        "slightly_stressed": "Calm Explain",
        "overthinking": "Small Focus Step"
    }
    return mapping[strategy]


# Planning
def plan_steps(strategy):
    return ["AcknowledgeEmotion", "AskClarification", "GiveNextStepSuggestion"]


# RL
def choose_action(strategy):
    actions = ["Encourage", "Explain", "Motivate", "GuideStep"]
    return random.choice(actions)


# llm 
def generate_reply(user_msg, emotions, action, steps):

    top_emotion = max(emotions, key=emotions.get)

    if top_emotion == "highly_anxious":
        return ("Yaar, pehle deep breath le, sab kuch ek hi moment mein fix nahi hota. "
        "Thoda slow down kar, tera dimaag abhi overload pe hai, isko break chahiye.​ "
        " Har cheez control mein rakhna possible nahi hota, and that’s totally okay. " 
         "Jo cheez aaj heavy lag rahi hai, woh time ke saath lighter ho jaYENGI."
)
    
    if top_emotion == "low_motivation":
        return ("Sun, aaj tujhe perfect nahi banna, bas thoda sa move karna hai. 
               "Sab log kabhi na kabhi stuck feel karte hain, you are not alone.
               "Tere andar already potential hai, bss thode focus ki need hai"
               "Even 10 percent effort bhi zero se zyada hota hai, "
               "ek brr aur try krte hai apn"
")
    
    if top_emotion == "overthinking":
        return ("Tu itna zyada future imagine kar raha hai ki present enjoy hi nahi kar paa raha. "
        "Jo cheez abhi tere saamne hai, bas usko handle kar, baaki cheezein naturally line mein aayengi.​
        "Ek kaam kr thoda walk le, music sun, ya kisi friend se randomly baat kr kar brain relax ho jayega"
)
    
    return ("Tu already kaafi accha kar raha hai, bas thodi consistency aur chahiye. "
    "Agar tu aise hi chota-chota effort daily rakhega na, "
    "toh slowly changes dekhne lgenge. "
    " Bas aise hi try karta reh, mistakes hongi pr wo tujhe better hi bnayegi.")


print("\nAI-Based Emotional Support Chat System")

user_msg = input("Student: ")

emotions = infer_emotion(user_msg)
strategy = select_strategy(emotions)
steps = plan_steps(strategy)
action = choose_action(strategy)
reply = generate_reply(user_msg, emotions, action, steps)

print("\nReply →", reply)

