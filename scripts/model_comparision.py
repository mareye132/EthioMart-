from transformers import DistilBertTokenizer, DistilBertForTokenClassification
from sklearn.metrics import accuracy_score

# Load the datasets (training and validation)
train_dataset = Dataset.from_dict({
    'input_ids': train_encodings['input_ids'],
    'attention_mask': train_encodings['attention_mask'],
    'labels': train_labels
})

# DistilBERT Fine-tuning
distil_model = DistilBertForTokenClassification.from_pretrained('distilbert-base-uncased', num_labels=len(label_map))
distil_trainer = Trainer(
    model=distil_model,
    args=training_args,
    train_dataset=train_dataset
)

distil_trainer.train()

# Evaluation (replace with validation dataset)
predictions = distil_trainer.predict(train_dataset)
pred_labels = predictions.predictions.argmax(-1)

# Accuracy
accuracy = accuracy_score(train_labels, pred_labels)
print(f'DistilBERT Accuracy: {accuracy}')

# Compare models based on evaluation metrics
# This process should include evaluating XLM-Roberta and other models similarly.
