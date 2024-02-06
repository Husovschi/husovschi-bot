import os
import json
import re
from telethon import TelegramClient, events

from ollama import AsyncClient

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
ollama_api_endpoint = os.getenv('OLLAMA_API_ENDPOINT') or 'http://ollama-server:11434'

# Create the client and connect
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

f = open('whitelist.json')
white_list = json.load(f)
f.close()


@client.on(events.NewMessage(chats=None))
async def handler(event):
    message_text = ''
    if event.is_group:  # Check if its in  a group
        if event.message.mentioned and (str(event.chat_id) in white_list['group_ids']):  # Check if the bot is mentioned
            # Remove the bot's mention from the message
            message_text = event.message.message
            bot_username = (await client.get_me()).username
            message_text = message_text.replace(f"@{bot_username}", "").strip()
    else:
        message_text = event.message.message

    if message_text:
        with open("prompt.txt", "r") as file:
            prompt = file.read()
        prompt = prompt.replace("USER_TEXT", message_text)
        answer = ""
        m = None
        async for part in await (AsyncClient(host=ollama_api_endpoint)
                .chat(model='dolphin-phi',
                      messages=[{'role': 'user', 'content': prompt}],
                      stream=True,
                      )):
            if part['message']['content']:
                answer += part['message']['content']
                if m is not None:
                    if re.search(r'[,.!?]', part['message']['content']):
                        await client.edit_message(m, answer)
                else:
                    m = await event.reply(message=answer)


client.run_until_disconnected()
