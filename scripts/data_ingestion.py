from telethon import TelegramClient, events
import csv
import os
import re

# Your Telegram API credentials (replace with your actual credentials)
api_id = '21138037'  # Replace with your actual API ID
api_hash = 'f62291f2ec7170893596772793ead07e'  # Replace with your actual API hash
phone = '+251906283518'  # Replace with your actual phone number

# Amharic normalization map
amharic_normalization_map = {
    'ሃ': 'ሀ',  # Normalize 'ሃ' to 'ሀ'
    'ኃ': 'ሀ',  # Normalize 'ኃ' to 'ሀ'
    'ኀ': 'ሀ',  # Normalize 'ኀ' to 'ሀ'
    'ዓ': 'አ',  # Normalize 'ዓ' to 'አ'
    'አ': 'አ',  # No change for 'አ'
    'ፀ': 'ጸ',  # Normalize 'ፀ' to 'ጸ'
    'ቨ': 'በ',  # Normalize 'ቨ' to 'በ'
}

# List of Amharic stop words (common, non-informative words)
amharic_stop_words = [
    'እና', 'ነበር', 'ወይም', 'እንዲህ', 'እንጂ', 'እንደ', 'ሁሉም', 'እዚህ', 'እሱ', 'እሷ', 'እኔ',
    'አንተ', 'አንቺ', 'እነሱ', 'ሁላችንም', 'ማንኛውም', 'በተጨማሪ', 'እንዲሁም', 'እዚህም', 'እነዚህ', 
    'በግምት', 'ከዚህ', 'በመሆኑ', 'ወደ', 'ሆኖ', 'ከዚህም', 'ሁሉን', 'ሁሉና', 'ይህ', 'ችሎ', 'ከነበረ',
    # Add more stop words as needed
]

# Function to preprocess Amharic text
def preprocess_amharic_text(text):
    if not text:
        return ''
    
    # Normalization: Map similar characters to a single representation
    for original_char, normalized_char in amharic_normalization_map.items():
        text = text.replace(original_char, normalized_char)

    # Remove Amharic punctuation and special characters
    text = re.sub(r'[፡።፣፤፥፦፧፨]', ' ', text)  # Replace Amharic punctuation marks with space
    text = re.sub(r'[^\u1200-\u137F\s]', '', text)  # Keep only Amharic characters and spaces
    
    # Tokenization: Split text into words
    tokens = text.split()
    
    # Remove stop words
    tokens = [token for token in tokens if token not in amharic_stop_words]
    
    # Return preprocessed text as a single string
    return ' '.join(tokens)

# Function to scrape data from a single channel
async def scrape_channel(client, channel_username, writer, media_dir):
    entity = await client.get_entity(channel_username)
    channel_title = entity.title  # Extract the channel's title
    
    async for message in client.iter_messages(entity, limit=10000):
        media_path = None
        if message.media:
            if hasattr(message.media, 'photo'):
                filename = f"{channel_username}_{message.id}.jpg"
                media_path = os.path.join(media_dir, filename)
                await client.download_media(message.media, media_path)
            elif hasattr(message.media, 'document'):
                filename = f"{channel_username}_{message.id}.pdf"  # Change as needed for other file types
                media_path = os.path.join(media_dir, filename)
                await client.download_media(message.media, media_path)

        # Preprocess the text message
        cleaned_message = preprocess_amharic_text(message.message) if message.message else None
        
        # Write the channel title along with other data
        writer.writerow([channel_title, channel_username, message.id, cleaned_message, message.date, media_path])

# Initialize the client once
client = TelegramClient('scraping_session', api_id, api_hash)

async def main():
    await client.start()
    
    # Create a directory for media files
    media_dir = 'media_files'  # Changed to accommodate different media types
    os.makedirs(media_dir, exist_ok=True)

    # Open the CSV file and prepare the writer
    with open('telegram_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])  # Include channel title in the header
        
        # List of channels to scrape
        channels = [
            '@Shageronlinestore',  # Example channel
            # Add other Ethiopian-based e-commerce channels
        ]
        
        # Iterate over channels and scrape data into the single CSV file
        for channel in channels:
            await scrape_channel(client, channel, writer, media_dir)
            print(f"Scraped data from {channel}")

# Real-time message handler to collect data in real-time
@client.on(events.NewMessage(chats=['@Shageronlinestore']))  # Add more channels as needed
async def new_message_handler(event):
    channel_username = event.chat.username
    media_dir = 'media_files'  # Ensure the media directory is set
    with open('telegram_data_realtime.csv', 'a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        media_path = None
        if event.message.media:
            if hasattr(event.message.media, 'photo'):
                filename = f"{channel_username}_{event.message.id}.jpg"
                media_path = os.path.join(media_dir, filename)
                await client.download_media(event.message.media, media_path)
            elif hasattr(event.message.media, 'document'):
                filename = f"{channel_username}_{event.message.id}.pdf"  # Change as needed for other file types
                media_path = os.path.join(media_dir, filename)
                await client.download_media(event.message.media, media_path)

        # Preprocess the text message
        cleaned_message = preprocess_amharic_text(event.message.message) if event.message.message else None

        # Write the channel title along with other data
        writer.writerow([event.chat.title, channel_username, event.message.id, cleaned_message, event.message.date, media_path])

# Running the main scraping function
with client:
    client.loop.run_until_complete(main())

# Start listening to real-time messages
client.start(phone=phone)
client.run_until_disconnected()
