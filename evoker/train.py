import random
import os
import random
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

def train(epochs: int = EPOCHS):
    with open(TRAINING_DATA_PATH) as infile:
        all_prompts = infile.read().strip().split("\n")

    if not all_prompts:
        raise Exception("Read 0 prompts from prompt file")

    # scramble the prompts so the model doesn't learn association between lines
    with open(SCRAMBED_PATH, "w+") as fp:
        for _ in range(4):
            random.shuffle(all_prompts)
            fp.write(END_TOKEN.join(all_prompts) + END_TOKEN)

    # quick and dirty workaround to blow away the cache for now
    # TODO: upgrade to huggingface datasets lib. TextDataset is deprecated

    # only do this on linux
    if os.name == "posix":
        os.system("rm /cached_lm_GPT2TokenizerFast")
        os.system("rm -rf /output/")

    tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
    model = AutoModelForCausalLM.from_pretrained("distilgpt2")
    train_dataset = TextDataset(tokenizer=tokenizer, file_path=SCRAMBED_PATH, block_size=tokenizer.model_max_length)
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    training_args = TrainingArguments(
        output_dir='./output',
        overwrite_output_dir=True,
        num_train_epochs=epochs,
        per_device_train_batch_size=1,
        prediction_loss_only=True,
        logging_steps=100,
        save_steps=0,
        seed=random.randint(0, 2**32-1),
    )

    trainer = Trainer(
        model=model,
        tokenizer=tokenizer,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
    )

    trainer.train()
    model.save_pretrained("./model")

if __name__ == "__main__":
    train()