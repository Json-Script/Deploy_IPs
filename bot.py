import os
import requests
import telegram
from tempfile import NamedTemporaryFile

# Telegram bot credentials
chat_id = os.getenv('TELEGRAM_CHAT_ID')
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

# List of raw GitHub URLs
raw_links = [
    'https://raw.githubusercontent.com/Json-Script/Collect_IPs/main/list/export.json',
    'https://raw.githubusercontent.com/Json-Script/Collect_IPs/main/list/ipv4.json',
    'https://raw.githubusercontent.com/Json-Script/Collect_IPs/main/list/ipv6.json',
    'https://raw.githubusercontent.com/Json-Script/Collect_Keys/main/plus/full',
    'https://raw.githubusercontent.com/Json-Script/Collect_Keys/main/plus/lite'
]

# Initialize the bot
bot = telegram.Bot(token=bot_token)

def send_message(message):
    """Send a message to the Telegram chat."""
    try:
        bot.send_message(chat_id=chat_id, text=message)
        print(f"Message sent to chat {chat_id}")
    except telegram.error.TelegramError as e:
        print(f"Failed to send message: {str(e)}")

def send_file(content, filename):
    """Send a file to the Telegram chat."""
    try:
        # Send the file to Telegram chat
        with NamedTemporaryFile(delete=False, mode='wb') as temp_file:
            temp_file.write(content)
            temp_file.close()
            with open(temp_file.name, 'rb') as file:
                bot.send_document(chat_id=chat_id, document=file, filename=filename)
            os.remove(temp_file.name)  # Clean up the temporary file
        print(f"File {filename} sent to chat {chat_id}")
    except telegram.error.TelegramError as e:
        print(f"Failed to send file: {str(e)}")

def fetch_and_send_raw_content():
    """Fetch the content from the raw GitHub URLs and send it to the Telegram channel."""
    for url in raw_links:
        try:
            print(f"Attempting to fetch: {url}")
            # Fetch raw content
            response = requests.get(url)
            response.raise_for_status()  # This will raise an exception for 4xx/5xx HTTP responses
            content = response.content  # Get the raw content as bytes
            filename = url.split("/")[-1]  # Use the last part of the URL as the filename
            print(f"Fetched content from {url}")
            # Send the content as a file
            send_file(content, filename)
        except requests.exceptions.RequestException as e:
            error_message = f"Failed to fetch {url}: {str(e)}"
            print(error_message)
            send_message(error_message)  # Send failure message to Telegram

if __name__ == '__main__':
    fetch_and_send_raw_content()