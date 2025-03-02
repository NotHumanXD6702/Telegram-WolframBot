from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CallbackContext
import wolframalpha
import hashlib
import os

# Get credentials from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")

# Initialize Wolfram Alpha Client
wa_client = wolframalpha.Client(WOLFRAM_APP_ID)

# Function to handle inline queries
def inline_query(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    if not query:
        return
    
    try:
        res = wa_client.query(query)
        answer = next(res.results).text
    except:
        answer = "Couldn't solve it."

    result_id = hashlib.md5(query.encode()).hexdigest()  # Unique ID for caching
    results = [
        InlineQueryResultArticle(
            id=result_id,
            title="Wolfram Alpha Result",
            input_message_content=InputTextMessageContent(answer),
        )
    ]
    update.inline_query.answer(results)

# Start the bot
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(InlineQueryHandler(inline_query))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
