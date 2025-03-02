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

# Get the bot token from the environment variable
TOKEN = os.getenv("BOT_TOKEN")

# Function to handle /start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! I am your bot. How can I help you?")

# Main function to set up the bot
async def main():
    # Initialize the bot application
    app = Application.builder().token(TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))

    # Start polling
    await app.run_polling()

# Properly handle the event loop for Railway deployment
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If an event loop is already running, use `create_task`
            loop.create_task(main())
        else:
            loop.run_until_complete(main())
    except RuntimeError as e:
        # Create a new event loop if none exists
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except Exception as e:
        logger.error(f"An error occurred: {e}")
