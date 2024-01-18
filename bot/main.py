import os
from telethon import TelegramClient, events

from langchain.schema import HumanMessage
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.chat_models import ChatOllama

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
ollama_api_endpoint = os.getenv('OLLAMA_API_ENDPOINT') or 'http://ollama-server:11434'

# Create the client and connect
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)


# Initialize the Ollama object with the API endpoint and model name
chat_model = ChatOllama(
    model="dolphin-phi",
    base_url=ollama_api_endpoint
)

messages = []
@client.on(events.NewMessage(chats=None))
async def handler(event):
    if event.is_group and event.message.mentioned:  # Check if the bot is mentioned
        # Remove the bot's mention from the message
        message_text = event.message.message
        bot_username = (await client.get_me()).username
        message_text = message_text.replace(f"@{bot_username}", "").strip()
    else:
        message_text = event.message.message
        # Create a HumanMessage object for the new message
        new_message = HumanMessage(
            content=message_text
        )

        # Append the new HumanMessage object to the messages list
        messages.append(new_message)

        # Generate a response with the updated messages list
        answer = chat_model(messages)
        print(answer.content)
        await event.respond(answer.content)

client.run_until_disconnected()