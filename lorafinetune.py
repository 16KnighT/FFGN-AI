# lora_finetune.py
import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model


# -----------------------------
# 1. Config
# -----------------------------
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T"  # change to your base model
DATA_PATH = "conversation_pairs.jsonl"                # path to your JSONL
OUTPUT_DIR = "./lora_finetuned"
MAX_LENGTH = 512
BATCH_SIZE = 4
GRAD_ACCUM = 4
EPOCHS = 3
LEARNING_RATE = 3e-4

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16
)

# -----------------------------
# 2. Load model & tokenizer
# -----------------------------
print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    dtype=torch.float16,
    quantization_config=bnb_config
)


# Make sure tokenizer has pad token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# -----------------------------
# 3. Apply LoRA
# -----------------------------
print("Applying LoRA...")
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],  # for LLaMA models
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

# -----------------------------
# 4. Load & tokenize dataset
# -----------------------------
print("Loading dataset...")
dataset = load_dataset("json", data_files=DATA_PATH)

def tokenize(example):
    prompt = example["prompt"]
    completion = example.get("response") or example.get("completion")
    full_text = f"{prompt}\n{completion}"
    tokenized = tokenizer(
        full_text,
        truncation=True,
        max_length=MAX_LENGTH,
        padding="max_length"
    )
    # labels for causal LM are the same as input_ids
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

print("Tokenizing dataset...")
dataset = dataset.map(tokenize, remove_columns=["prompt", "response"])

# -----------------------------
# 5. Training
# -----------------------------
print("Starting training...")
training_args = TrainingArguments(
    per_device_train_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=GRAD_ACCUM,
    learning_rate=LEARNING_RATE,
    num_train_epochs=EPOCHS,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch",
    output_dir=OUTPUT_DIR,
    save_total_limit=2
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"]
)

trainer.train()
trainer.save_model(OUTPUT_DIR)
print("LoRA fine-tuning complete! Model saved to", OUTPUT_DIR)
