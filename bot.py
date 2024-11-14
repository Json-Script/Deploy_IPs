import os
import requests
import telegram

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
    bot.send_message(chat_id=chat_id, text=message)

def fetch_and_send_raw_content():
    """Fetch the content from the raw GitHub URLs and send it to the Telegram channel."""
    for url in raw_links:
        try:
            print(f"Fetching: {url}")  # Debugging log
            # Fetch raw content
            response = requests.get(url)
            response.raise_for_status()
            content = response.text
            print(f"Fetched content from {url}")  # Debugging log
            # Send the content as a message
            send_message(content)
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch {url}: {str(e)}")  # Debugging log
            send_message(f"Failed to fetch {url}: {str(e)}")

if __name__ == '__main__':
    fetch_and_send_raw_content()