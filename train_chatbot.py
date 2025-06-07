from transformers import Trainer, TrainingArguments, AutoTokenizer, AutoModelForCausalLM
from datasets import load_dataset

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
