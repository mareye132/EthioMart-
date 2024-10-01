# EthioMart-
Project: Final Report on EthioMart: Named Entity Recognition (NER)
System for Ethiopian E-commerce Data

## Task 1: Data Ingestion and Preprocessing

For the EthioMart project, the first step was setting up a data ingestion system to capture messages from an Ethiopian-based Telegram e-commerce channel called @Shegeronlinestore. These messages typically include product listings, prices, and location information.

### Steps:

1. **Channel Identification and Scraping**: 
   A custom scraper was developed to connect and extract messages from the Ethiopian-based Telegram channel. The scraper captured text, images, and metadata (e.g., sender, timestamp).

2. **Message Ingestion**: 
   The system ingested the data in real-time, capturing various data types (e.g., text and images). Python’s Telethon library was used for this purpose, ensuring the messages were collected in a structured format.

3. **Preprocessing**:
   - **Tokenization**: Tokenized the Amharic text to handle the unique morphology of the language. The text was processed using a tokenizer that supports Amharic.
   - **Normalization**: Handled specific linguistic features, including vowel normalization and stopword removal.
   - **Data Cleaning**: Removed irrelevant characters and symbols, ensuring consistent formatting.
   - **Data Structuring**: The final structured data included metadata (sender, timestamp) separated from the message content, ready for downstream tasks such as Named Entity Recognition (NER).

4. **Storage**: 
   Preprocessed data was stored in a structured format (CSV) for further labeling and model training.

## Task 2: Labeling Subset of Dataset in CoNLL Format

The next task involved labeling a portion of the dataset in the CoNLL format, which is often used in Named Entity Recognition (NER) tasks.

### Key Entity Types:
- **B-Product** and **I-Product**: Beginning and inside a product entity (e.g., "ቢዝኒስ ሳምንት" for "Business Week").
- **B-LOC** and **I-LOC**: Beginning and inside a location entity (e.g., "ባህር ዳር").
- **B-PRICE** and **I-PRICE**: Beginning and inside a price entity (e.g., "ብር 1000").

### Example CoNLL Format:
The dataset labeled in this format was saved in a plain text file, with each token tagged appropriately for further model training.

## Task 3: Fine-tuning the NER Model

For fine-tuning the NER model, the following approach was used:

1. **Environment Setup**: Used Google Colab with GPU support to accelerate the training process. Necessary libraries such as transformers, torch, and datasets were installed.
   
2. **Pre-trained Model**: A pre-trained model, XLM-Roberta (supporting Amharic), was used as a base. The model was fine-tuned for three epochs using the labeled CoNLL dataset.

3. **Training & Validation Losses**:
   - **Epoch 1**: Training Loss: No log, Validation Loss: 0.000024
   - **Epoch 2**: Training L
## Task 4: Model Comparison & Selection

For the model comparison task, the performance of multiple models was evaluated based on validation loss, evaluation speed, and robustness in handling Amharic language text.

### Evaluated Models:
1. **DistilBERT**: A lighter, faster variant of BERT.
- Validation Loss: 0.1220
- Eval Samples/Second: 270.221

2. **XLM-Roberta**: A large multilingual model specifically fine-tuned for Amharic.
- Validation Loss: 0.1735
- Eval Samples/Second: 212.856

3. **mBERT (Multilingual BERT)**: Optimized for multilingual tasks, including Amharic.
- Validation Loss: 0.1058
- Eval Samples/Second: 230.8874

### Results:
The best-performing model based on evaluation loss is **mBERT**, with a validation loss of 0.1058. While XLM-Roberta had a lower sample-per-second rate, mBERT provided a better balance between accuracy and speed, making it ideal for production deployment in EthioMart’s NER task.

## Task 5: Model Interpretability

To ensure transparency and trust in the system, model interpretability tools like SHAP (SHapley Additive exPlanations) and LIME (Local Interpretable Model-agnostic Explanations) were implemented.

### Steps:
1. **SHAP & LIME**: These tools helped interpret how the fine-tuned NER model predicted entities, providing insights into the model’s decision-making process.

2. **Error Analysis**: Difficult cases, such as ambiguous text or overlapping entities, were analyzed to understand where the model struggled.

3. **Model Reports**: Detailed reports were generated to explain model predictions and provide insights into areas where the model could improve.

## Conclusion

The EthioMart NER system was successfully developed, using real-time data from an Ethiopian-based Telegram channel. Fine-tuning **mBERT** resulted in the best model performance, and model interpretability techniques were used to ensure transparency. This NER system can extract entities such as products, prices, and locations from Amharic text, providing a robust solution for Ethiopian e-commerce data analysis.
oss: 0.011900, Validation Loss: 0.000013
   - **Epoch 3**: Training Loss: 0.011900, Validation Loss: 0.000010
   
   **Final training output**:
