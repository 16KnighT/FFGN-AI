import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

SYSTEM_PROMPT = (
    "Do not repeat the user's message. "
    "Reply conversationally.\n"
)

base_model = "TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T"   # or whatever base you fine-tuned
lora_path = "./lora_finetuned"         # your LoRA output from training

print("Loading tokenizer…")
tokenizer = AutoTokenizer.from_pretrained(base_model)

print("Loading base model…")
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    dtype=torch.float16,
    device_map="auto"
)

print("Applying LoRA weights…")
model = PeftModel.from_pretrained(model, lora_path)
model = model.merge_and_unload()  # optional but faster

print("Ready! Starting CLI chat.\n")

history = ""

# Chat loop
while True:
    user = input("You: ")
    if user.strip().lower() in {"exit", "quit"}:
        break

    prompt = "Niamh: " + user + "\n"
    history += prompt

    inputs = tokenizer(history, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=300,
        temperature=0.7,
        top_p=0.9,
        do_sample=True
    )

    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    bot_reply = text[len(history):].split("\n")[0]

    print(bot_reply)

    history += bot_reply + "\n"
