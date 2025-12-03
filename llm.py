
#llm by Anushka Saxena 25ai06002
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Running on:", device)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32
).to(device)


emotion_state = "highly_anxious"
strategy = "EncourageWithHope"
plan_steps = ["GreetStudent", "AcknowledgeEmotion", "EncourageConfidence", "GiveNextStepSuggestion"]
language_mode = "mixed"
user_message = "I am tired yaar, kuch samajh nahi aa raha"

prompt = f"""<|system|>
You are a friendly emotional support mentor. Always reply briefly in helpful Hinglish (English + Hindi).
Acknowledge feelings, encourage hope, and give one small actionable step.
3 to 5 short sentences ONLY. No judging, no medical advice.

<|user|>
Student message: "{user_message}"
Emotion: {emotion_state}
Strategy: {strategy}
Plan: {", ".join(plan_steps)}
Language: {language_mode}

Now generate the reply.
<|assistant|>
"""

inputs = tokenizer(prompt, return_tensors="pt").to(device)

with torch.no_grad():
    output_ids = model.generate(
        inputs["input_ids"],
        max_new_tokens=100,
        do_sample=False,
        repetition_penalty=1.4,
        temperature=0.3  
    )

reply = tokenizer.decode(output_ids[0], skip_special_tokens=True)
reply = reply.split("<|assistant|>")[-1].strip()

print("\nAI Reply:", reply)
