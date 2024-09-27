#!pip install transformers datasets

import pandas as pd
from transformers import XLMRobertaTokenizer, XLMRobertaForTokenClassification, Trainer, TrainingArguments
from datasets import load_dataset, Dataset

# Load labeled dataset in CoNLL format
def load_conll(file_path):
    sentences = []
    current_sentence = []
    current_labels = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():  # Not a blank line
                token, label = line.strip().split()
                current_sentence.append(token)
                current_labels.append(label)
            else:
                if current_sentence:
                    sentences.append((current_sentence, current_labels))
                    current_sentence, current_labels = [], []
    
    return sentences

data = load_conll('labeled_data.conll')
train_texts, train_labels = zip(*data)

# Tokenization
tokenizer = XLMRobertaTokenizer.from_pretrained('xlm-roberta-base')
train_encodings = tokenizer(list(train_texts), truncation=True, padding=True)

# Align labels with tokens
train_labels = [[label_map[label] for label in labels] for labels in train_labels]

# Create Dataset
train_dataset = Dataset.from_dict({
    'input_ids': train_encodings['input_ids'],
    'attention_mask': train_encodings['attention_mask'],
    'labels': train_labels
})

# Fine-tuning
model = XLMRobertaForTokenClassification.from_pretrained('xlm-roberta-base', num_labels=len(label_map))
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    evaluation_strategy="epoch",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset
)

trainer.train()

# Save the model
model.save_pretrained('./ner_model')
tokenizer.save_pretrained('./ner_model')
