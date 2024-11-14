import os
import requests

# Set your Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

def send_message(bot_token, chat_id, message):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {'chat_id': chat_id, 'text': message}
    requests.post(url, data=data)

# Fetch the file contents
with open('export.json', 'r') as f:
    export_content = f.read()

with open('ipv4.json', 'r') as f:
    ipv4_content = f.read()

with open('ipv6.json', 'r') as f:
    ipv6_content = f.read()

with open('full', 'r') as f:
    full_content = f.read()

with open('lite', 'r') as f:
    lite_content = f.read()

# Send the file contents as text messages to the Telegram bot
send_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, "Export file content:\n\n" + export_content)
send_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, "IPv4 file content:\n\n" + ipv4_content)
send_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, "IPv6 file content:\n\n" + ipv6_content)
send_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, "Full file content:\n\n" + full_content)
send_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, "Lite file content:\n\n" + lite_content)