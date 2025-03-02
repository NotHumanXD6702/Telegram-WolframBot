import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Get API keys from Railway environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Your Telegram bot token
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")  # Your Wolfram Alpha API key

# Function to get answer from Wolfram Alpha
def get_wolfram_answer(query):
    url = f"https://api.wolframalpha.com/v2/query?input={query}&format=plaintext&output=JSON&appid={WOLFRAM_APP_ID}"
    response = requests.get(url).json()

    try:
        for pod in response["queryresult"]["pods"]:
            if "primary" in pod and pod["primary"]:  # Get the main answer
                return pod["subpods"][0]["plaintext"]
        return "Couldn't find a proper answer."
    except Exception as e:
        return f"Error: {str(e)}"

# Command function to handle /math
async def solve(update: Update, context: CallbackContext) -> None:
    if not context.args:
        await update.message.reply_text("Please provide a math expression. Example: /math 2+2")
        return

    query = " ".join(context.args)
    answer = get_wolfram_answer(query)

    await update.message.reply_text(f"🧮 *Question:* `{query}`\n✅ *Answer:* `{answer}`", parse_mode="Markdown")

# Start the bot
async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("math", solve))

    # Start polling
    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
