import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama

# Read the Telegram bot token and Ollama API endpoint from environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') or 'your_fallback_token'
OLLAMA_API_ENDPOINT = os.getenv('OLLAMA_API_ENDPOINT') or 'your_fallback_endpoint'

# Initialize the Ollama object with the API endpoint and model name
ollama = Ollama(
    base_url=OLLAMA_API_ENDPOINT,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    model="mistral")

async def start(update: Update, context: CallbackContext) -> None:
    """
    Sends a welcome message when the /start command is issued.
    """
    await update.message.reply_text('Ask me any question.')

async def handle_message(update: Update, context: CallbackContext) -> None:
    """
    Handles incoming messages by forwarding them to the Ollama API
    and replying with the generated answer.
    """
    question = update.message.text
    answer = ollama(question)
    await update.message.reply_text(answer)

if __name__ == '__main__':
    # Create the bot application with the specified token
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register handlers for different commands and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling messages from Telegram
    application.run_polling()
