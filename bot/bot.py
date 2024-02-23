import os

from telethon import TelegramClient, events
from whitelist_manager import WhitelistManager
from ollama_client import OllamaClient
from message_handler import MessageHandler

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
ollama_api_endpoint = os.getenv('OLLAMA_API_ENDPOINT') or 'http://ollama-server:11434'

telegram_client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
whitelist_manager = WhitelistManager()
ollama_client = OllamaClient(ollama_api_endpoint)
message_handler = MessageHandler(telegram_client, ollama_client, whitelist_manager)

telegram_client.add_event_handler(message_handler.handle_message, events.NewMessage(chats=None))

telegram_client.run_until_disconnected()
