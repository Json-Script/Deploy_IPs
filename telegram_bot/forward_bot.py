# forward_bot.py
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Retrieve the bot token and your chat ID from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("MY_CHAT_ID")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Retrieve the message text, sender's chat ID, and username if available
    message_text = update.message.text
    sender_chat_id = update.message.chat_id
    sender_username = update.message.from_user.username if update.message.from_user.username else "No username"

    # Compose the message to send to your chat ID
    forwarded_message = f"Message from {sender_username} (ID: {sender_chat_id}):\n\n{message_text}"

    # Send the message to your specified chat ID
    await context.bot.send_message(chat_id=CHAT_ID, text=forwarded_message)

if __name__ == "__main__":
    # Initialize the bot application
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Set up a handler to listen for text messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling for messages
    app.run_polling()