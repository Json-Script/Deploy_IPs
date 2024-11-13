# forward_bot.py
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Retrieve the bot token and chat ID from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("MY_CHAT_ID")

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Forward the received message to the specified chat ID
    if update.message:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=f"Message from {update.message.from_user.first_name}: {update.message.text}"
        )

if __name__ == "__main__":
    # Initialize the bot application
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Set up a handler for text messages to trigger forwarding
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message))

    # Start polling to receive messages
    app.run_polling()