# EthioMart-
Project: EthioMart Entity Labeling and Data Ingestion
Introduction
This project involves the development of scripts to perform data ingestion and entity labeling on a dataset of messages from Telegram. The goal is to preprocess the data for natural language processing tasks such as named entity recognition (NER) and other machine learning applications.

Task 1: Data Ingestion
Script: data_injestion.py

Objective: The purpose of this task is to ingest raw data from a CSV file and perform initial preprocessing.

Steps:

Data Loading: The script reads data from a CSV file containing Telegram messages.
Data Cleaning: Basic cleaning operations are performed, such as handling missing values and removing duplicates.
Data Transformation: Additional transformations may include normalizing text, converting text to lowercase, and removing unwanted characters or patterns.
Data Saving: The cleaned and preprocessed data is saved to a new CSV file for further analysis or labeling.
Usage:
Run the script from the command line using the following command:
python scripts/data_injestion.py
Output:
A cleaned dataset saved as telegram_data.csv in the specified directory.

Task 2: Entity Labeling
Script: Labling_dataset.py

Objective: This task involves labeling the dataset with entity tags in the CoNLL format. It is designed to identify specific entities such as products, locations, and prices within the text.

Entity Types Labeled:

B-Product: The beginning of a product entity (e.g., "ስልክ", "ጫማ").
I-Product: Inside a product entity (e.g., "መታሻ", "እንቁላል").
B-LOC: The beginning of a location entity (e.g., "አዲስ", "ጎንደር").
I-LOC: Inside a location entity (e.g., "አባላጅ", "ሀዋሳ").
B-PRICE: The beginning of a price entity (e.g., "1000 ብር").
I-PRICE: Inside a price entity (e.g., "ብር", "ዋጋ").
O: Tokens outside of any labeled entities.
Steps:

Data Loading: Load the preprocessed CSV file containing the cleaned messages.
Entity Labeling: Apply regular expressions to label entities within each message based on predefined patterns for different entity types.
Data Saving: Save the labeled data in the CoNLL format, which is commonly used for NER tasks.
Usage:
Run the script from the command line using the following command:
python scripts/Labling_dataset.py
Output:
A file named labeled_data.conll containing the labeled messages in the CoNLL format.