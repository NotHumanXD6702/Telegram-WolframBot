import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import os

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram Bot Token from Railway environment variables
TOKEN = os.getenv("BOT_TOKEN")

# Function to handle /start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! I am your bot. How can I help you?")

# Main function
async def main():
    # Initialize the bot application
    app = Application.builder().token(TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))

    # Start polling
    await app.run_polling()

# Proper handling of asyncio event loop
if __name__ == "__main__":
    try:
        asyncio.run(main())  # ✅ Works fine when running normally
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())  # ✅ Fixes issue when inside an existing loop
