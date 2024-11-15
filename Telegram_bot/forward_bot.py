import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# List of file URLs to be sent by GitHub Actions
file_urls = [
    "https://raw.githubusercontent.com/Json-Script/Collect_IPs/main/list/export.json",
    "https://raw.githubusercontent.com/Json-Script/Collect_IPs/main/list/ipv4.json",
    "https://raw.githubusercontent.com/Json-Script/Collect_IPs/main/list/ipv6.json",
    "https://raw.githubusercontent.com/Json-Script/Collect_Keys/main/plus/full",
    "https://raw.githubusercontent.com/Json-Script/Collect_Keys/main/plus/lite"
]

def list_files(update: Update, context: CallbackContext):
    """Handle the /list command and send the file URLs."""
    message = "Here are the file URLs being sent:\n"
    for url in file_urls:
        message += f"{url}\n"
    update.message.reply_text(message)

def start(update: Update, context: CallbackContext):
    """Handle the /start command."""
    update.message.reply_text("Welcome! Use /list to get the list of file URLs being sent.")

def main():
    """Start the bot."""
    # Replace YOUR_BOT_TOKEN with your actual bot token
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)

    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("list", list_files))

    # Start the bot
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()