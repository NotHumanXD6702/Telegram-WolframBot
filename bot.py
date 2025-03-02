import os
import wolframalpha
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, InlineQueryHandler
import hashlib

# Get environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")

# Initialize Wolfram Alpha Client
wa_client = wolframalpha.Client(WOLFRAM_APP_ID)

# Function to handle inline queries
async def inline_query(update: Update, context) -> None:
    query = update.inline_query.query
    if not query:
        return
    
    try:
        res = wa_client.query(query)
        answer = next(res.results).text
    except:
        answer = "Couldn't solve it."

    result_id = hashlib.md5(query.encode()).hexdigest()
    results = [
        InlineQueryResultArticle(
            id=result_id,
            title="Wolfram Alpha Result",
            input_message_content=InputTextMessageContent(answer),
        )
    ]
    await update.inline_query.answer(results)

# Start the bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(InlineQueryHandler(inline_query))
    app.run_polling()

if __name__ == "__main__":
    main()
