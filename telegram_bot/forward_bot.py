import os
from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import logging

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the bot and owner ID from environment variables
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
OWNER_ID = os.getenv("MY_CHAT_ID")

# Create the bot instance
updater = Updater(BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Define message handler function
def forward_message(update: Update, context):
    user_message = update.message.text
    context.bot.send_message(chat_id=OWNER_ID, text=f"Message from {update.message.from_user.username}: {user_message}")
    update.message.reply_text("Your message has been sent to the owner.")

# Add a message handler
message_handler = MessageHandler(Filters.text & ~Filters.command, forward_message)
dispatcher.add_handler(message_handler)

# Start the bot
updater.start_polling()
updater.idle()