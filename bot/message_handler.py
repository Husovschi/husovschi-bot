import re
import os

class MessageHandler:
    def __init__(self, telegram_client, ollama_client, whitelist_manager):
        self.telegram_client = telegram_client
        self.ollama_client = ollama_client
        self.whitelist_manager = whitelist_manager

    async def handle_message(self, event):
        if event.photo:
            await self.handle_photo_message(event)
        else:
            await self.handle_text_message(event)

    async def handle_photo_message(self, event):
        photo_path = await self.download_photo(event.photo)

        if photo_path:
            await self.process_photo(event, photo_path)
            os.remove(photo_path)
        else:
            await event.reply("Sorry, I couldn't download your photo.")

    async def download_photo(self, photo):
        """Download photo from a Telegram event and return the file path."""
        try:
            # Get the file path
            file_path = await self.telegram_client.download_media(photo)
            return file_path
        except Exception as e:
            print(f"Error downloading photo: {e}")
            return None

    async def process_photo(self, event, photo_path):
        answer = ""
        m = None
        async for part in self.ollama_chat('Describe this image:', image=photo_path):
            if part['message']['content']:
                answer += part['message']['content']
                if m is not None:
                    if re.search(r'[,.!?:;]', part['message']['content']):
                        m = await self.telegram_client.edit_message(m, answer)
                else:
                    m = await event.reply(message=answer)
        if len(m.message) != len(answer.strip()):
            await self.telegram_client.edit_message(m, answer)


    async def handle_text_message(self, event):
        message_text = event.message.message if not event.is_group else ""
        if event.is_group:
            if event.message.mentioned and (str(event.chat_id) in self.whitelist_manager.whitelist['group_ids']):
                bot_username = (await self.telegram_client.get_me()).username
                message_text = event.message.message.replace(f"@{bot_username}", "").strip()

        if message_text:
            # with open("prompt.txt", "r") as file:
            #     prompt = file.read()
            # prompt = prompt.replace("USER_TEXT", message_text)
            prompt = message_text
            answer = ""
            m = None

            async for part in self.ollama_chat(prompt):
                if part['message']['content']:
                    answer += part['message']['content']
                    if m is not None:
                        if re.search(r'[,.!?:;]', part['message']['content']):
                            m = await self.telegram_client.edit_message(m, answer)
                    else:
                        m = await event.reply(message=answer)
            if len(m.message) != len(answer.strip()):
                await self.telegram_client.edit_message(m, answer)

    async def ollama_chat(self, prompt, image=None):
        messages = [{'role': 'user', 'content': prompt}]
        if image:
            messages[0]['images'] = [image]
        chat_result = await self.ollama_client.chat(messages=messages, stream=True)
        async for part in await chat_result:
            yield part
