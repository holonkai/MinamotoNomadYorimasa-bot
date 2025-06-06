import praw
import re
from transformers import Trainer, TrainingArguments, AutoTokenizer, AutoModelForCausalLM
from datasets import load_dataset


def fetch_and_clean_data():
    reddit = praw.Reddit(
    client_id=
    client_secret=
    user_agent=
    )
    subreddit = reddit.subreddit("UnKnoWnCheaTs")
    with open("elden_ring_cheats_data.txt", "w", encoding="utf-8") as file:
        for post in subreddit.hot(limit=10):  
            file.write(post.title + " " + post.selftext + "\n")
    with open("elden_ring_cheats_data.txt", "r", encoding="utf-8") as file:
        data = file.readlines()
    cleaned_data = [
        re.sub(r"http\S+|www\S+|[^a-zA-Z\s]", "", post.lower())
        for post in data if "cheat" in post or "hack" in post
    ]
    with open("cleaned_elden_ring_cheats_data.txt", "w", encoding="utf-8") as file:
        for post in cleaned_data:
            file.write(post + "\n")
    print("Data fetched and cleaned successfully.")


def train_model():
    dataset = load_dataset('text', data_files={'train': 'cleaned_elden_ring_cheats_data.txt'})
    model_name = "gpt2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    def tokenize_function(examples):
        return tokenizer(examples['text'], truncation=True, padding=True, max_length=512)

    tokenized_datasets = dataset.map(tokenize_function, batched=True)

    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="steps",
        learning_rate=5e-5,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        num_train_epochs=3,
        weight_decay=0.01,
        save_steps=100,
        logging_dir="./logs",
        logging_steps=10,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        tokenizer=tokenizer
    )

    trainer.train()
    trainer.save_model("./elden_ring_chatbot")
    tokenizer.save_pretrained("./elden_ring_chatbot")
    print("Model fine-tuned and saved!")
    return model, tokenizer


def get_response(user_input, model, tokenizer):
    inputs = tokenizer.encode(user_input, return_tensors="pt")
    reply = model.generate(inputs, max_length=100)
    return tokenizer.decode(reply[0], skip_special_tokens=True)


if __name__ == "__main__":
   
    fetch_and_clean_data()
    
    
    model, tokenizer = train_model()
    
    
    while True:
        user_input = input("You: ")
        print("Bot:", get_response(user_input, model, tokenizer))
