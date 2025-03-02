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
        # Check if an event loop is already running
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If an event loop is already running, schedule the main() coroutine
            loop.create_task(main())
        else:
            # If no event loop is running, create a new one and run main()
            loop.run_until_complete(main())
    except RuntimeError as e:
        # Handle cases where the event loop is closed or unavailable
        logger.error(f"RuntimeError: {e}")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
