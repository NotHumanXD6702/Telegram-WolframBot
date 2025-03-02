import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import os

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! I am your bot. How can I help you?")

async def main():
    """Main async function to run the bot"""
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    # Critical fix: Prevent the library from closing the existing event loop
    await app.run_polling(close_loop=False)

if __name__ == "__main__":
    # Railway-specific event loop handling
    try:
        # First try standard execution
        asyncio.run(main())
    except RuntimeError as e:
        if "Event loop is closed" in str(e):
            # Handle Railway's persistent event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(main())
            loop.close()
        elif "already running" in str(e):
            # Use existing running loop
            loop = asyncio.get_event_loop()
            loop.create_task(main())
            try:
                # Keep the loop running indefinitely
                loop.run_forever()
            except KeyboardInterrupt:
                pass
        else:
            logger.error(f"Unexpected RuntimeError: {e}")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
