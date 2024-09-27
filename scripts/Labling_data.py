import pandas as pd
import re

# Load the dataset
df = pd.read_csv('C:/Users/user/Desktop/Github/EthioMart-/telegram_data.csv')  # Replace with the correct path to your CSV file

# Select the 'Message' column
messages = df['Message'].dropna().tolist()

# Define a function to label entities in the CoNLL format
def label_message(message):
    tokens = message.split()  # Simple tokenization
    labeled_tokens = []

    for token in tokens:
        # Product Entity
        if re.match(r'\b(ስልክ|የልጅ|ጫማ|አደይ|ቤት|እስር|ምስል|እንቁላል|ቶንዶስ|ማጂክ|የምሳ|ድስቶች|የሴራሚክ|አክለሪክ|የጁስ|ፔርሙዝ|የጀርባ)\b', token):  # B-Product
            labeled_tokens.append(f'{token} B-Product')
        elif re.match(r'\b(መጥበሻ|መታሻ|የውሀ|የምሳ|ምስል)\b', token):  # I-Product
            labeled_tokens.append(f'{token} I-Product')

        # Location Entity
        elif re.match(r'\b(አዲስ|አባላጅ|ኢትዮጵያ|ጎንደር|ሀዋሳ|ሞል|መዳህኒአለም|መሽ)\b', token):  # B-LOC
            labeled_tokens.append(f'{token} B-LOC')
        elif re.match(r'\b(አድራሻ|ታሜ|መወልወያ|ግራንድ)\b', token):  # I-LOC
            labeled_tokens.append(f'{token} I-LOC')

        # Price Entity (Expanded Patterns)
        elif re.match(r'(\d+\s?(ብር|ዶላር|ፓውንድ)|በ\s?\d+\s?(ብር|ዶላር|ፓውንድ)|ዋጋ\s?\d+\s?(ብር|ዶላር|ፓውንድ))', token):  # B-PRICE
            labeled_tokens.append(f'{token} B-PRICE')
        elif re.match(r'\b(ብር|ዶላር|ፓውንድ|እንደ|ማንኛውም|ከ|በላይ|በታች|ለ|ዋጋ)\b', token):  # I-PRICE
            labeled_tokens.append(f'{token} I-PRICE')

        else:
            labeled_tokens.append(f'{token} O')  # Outside any entity

    return labeled_tokens

# Apply the labeling function to each message
labeled_data = []
for message in messages[:50]:  # Label the first 50 messages
    labeled_tokens = label_message(message)
    labeled_data.extend(labeled_tokens)
    labeled_data.append('')  # Blank line to separate messages

# Save the labeled data in CoNLL format
with open('labeled_data.conll', 'w', encoding='utf-8') as f:
    for line in labeled_data:
        f.write(line + '\n')

print("Labeled data for the first 50 messages has been saved in 'labeled_data.conll' file.")
