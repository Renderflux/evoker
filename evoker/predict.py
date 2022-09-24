import random
import os
import random
import sys
from transformers import (
    AutoTokenizer, AutoModelForCausalLM,
    TextDataset, DataCollatorForLanguageModeling,
    Trainer, TrainingArguments
)
import datasets

EPOCHS = 10
END_TOKEN = "<|endoftext|>"
TRAINING_DATA_PATH = "evoker/data/prompts.txt"
SCRAMBED_PATH = "evoker/data/scrambled.txt"

datasets.disable_caching()

tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
model = AutoModelForCausalLM.from_pretrained(os.getenv("TRANSFORMER_MODEL", "kaj/evoker"))

def predict(
    prompt,
    amount = 1,
    max_length = 50,
    min_length = 10,
    temperature = 1.6,
    top_k = 150,
    top_p = 0.9,
):
    encoded_prompt = tokenizer(prompt, add_special_tokens=False, return_tensors="pt").input_ids
    encoded_prompt = encoded_prompt.to(model.device)

    output_sequences = model.generate(
        input_ids=encoded_prompt,
        max_length=max_length,
        min_length=min_length,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        do_sample=True,
        num_return_sequences=amount,
        pad_token_id=tokenizer.eos_token_id # gets rid of warning
    )

    predicted = []
    for generated_sequence in output_sequences:
        generated_sequence = generated_sequence.tolist()
        text = tokenizer.decode(generated_sequence, clean_up_tokenization_spaces=True, skip_special_tokens=True)
        predicted.append(text.strip().replace("\n", " ").replace("/", ","))

    return predicted

if __name__ == "__main__":
    predict(" ".join(sys.argv[1:]))