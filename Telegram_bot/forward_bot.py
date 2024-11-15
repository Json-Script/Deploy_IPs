import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import requests

# Define states for conversation
SELECTING_COMMAND, SELECTING_URL, EDITING_URL = range(3)

# Define variables to store user state and data
user_urls = []  # This will store URLs for editing or deletion
current_url = None  # The currently selected URL

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Command handlers

def start(update: Update, context: CallbackContext) -> int:
    """Start command, send a greeting."""
    update.message.reply_text("Hello! I am your IP distribution bot. How can I assist you today?")
    return SELECTING_COMMAND

def list_urls(update: Update, context: CallbackContext) -> int:
    """List all the URLs that have been sent."""
    urls = [
        "1. Export File URL",
        "2. IPv4 File URL",
        "3. IPv6 File URL",
        "4. Full Data URL",
        "5. Lite Data URL"
    ]
    update.message.reply_text("\n".join(urls))
    return SELECTING_COMMAND

def edit_url(update: Update, context: CallbackContext) -> int:
    """Start editing a URL."""
    update.message.reply_text("Please send the URL number or the file name you'd like to edit.")
    return SELECTING_URL

def handle_url_selection(update: Update, context: CallbackContext) -> int:
    """Handle selection of URL by number or name."""
    global current_url
    user_input = update.message.text.strip().lower()

    # Map user input to corresponding URL
    url_mapping = {
        "1": "https://raw.githubusercontent.com/Json-Script/Collect_IPs/main/list/export.json",
        "2": "https://raw.githubusercontent.com/Json-Script/Collect_IPs/main/list/ipv4.json",
        "3": "https://raw.githubusercontent.com/Json-Script/Collect_IPs/main/list/ipv6.json",
        "4": "https://raw.githubusercontent.com/Json-Script/Collect_Keys/main/plus/full",
        "5": "https://raw.githubusercontent.com/Json-Script/Collect_Keys/main/plus/lite"
    }

    # Match the user input to the corresponding URL
    if user_input in url_mapping:
        current_url = url_mapping[user_input]
        update.message.reply_text(f"You selected: {current_url}. Please send the new raw GitHub URL to update it.")
        return EDITING_URL
    else:
        update.message.reply_text("Invalid selection. Please send a valid number (1-5).")
        return SELECTING_URL

def edit_new_url(update: Update, context: CallbackContext) -> int:
    """Update the selected URL."""
    global current_url
    new_url = update.message.text.strip()

    # Here, update the URL in the bot's data (e.g., in a file or database if necessary)
    # For simplicity, we just print the change and update the URL
    if current_url:
        update.message.reply_text(f"URL updated from {current_url} to {new_url}.")
        current_url = new_url
    else:
        update.message.reply_text("No URL selected to edit.")
    return SELECTING_COMMAND

def delete_url(update: Update, context: CallbackContext) -> int:
    """Delete a URL."""
    global current_url
    if current_url:
        update.message.reply_text(f"URL {current_url} has been deleted.")
        current_url = None
    else:
        update.message.reply_text("No URL selected to delete.")
    return SELECTING_COMMAND

def cancel(update: Update, context: CallbackContext) -> int:
    """Cancel the current operation and go back to the greeting."""
    update.message.reply_text("Operation canceled. Hello! I am your IP distribution bot. How can I assist you today?")
    return SELECTING_COMMAND

def unknown(update: Update, context: CallbackContext) -> None:
    """Handle unknown commands."""
    update.message.reply_text("Sorry, I didn't understand that command.")

def main():
    """Start the bot."""
    # Use your bot's token here
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)

    # Dispatcher for handling commands
    dp = updater.dispatcher

    # Set up ConversationHandler to manage different commands and states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                      CommandHandler('list', list_urls),
                      CommandHandler('edit', edit_url),
                      CommandHandler('delete', delete_url),
                      CommandHandler('cancel', cancel)],
        states={
            SELECTING_COMMAND: [
                CommandHandler('start', start),
                CommandHandler('list', list_urls),
                CommandHandler('edit', edit_url),
                CommandHandler('delete', delete_url),
                CommandHandler('cancel', cancel),
            ],
            SELECTING_URL: [
                MessageHandler(Filters.text, handle_url_selection),
            ],
            EDITING_URL: [
                MessageHandler(Filters.text, edit_new_url),
            ],
        },
        fallbacks=[MessageHandler(Filters.text, unknown)],
    )

    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.command, unknown))

    # Start polling for updates
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()