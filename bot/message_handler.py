import re


class MessageHandler:
    def __init__(self, telegram_client, ollama_client, whitelist_manager):
        self.telegram_client = telegram_client
        self.ollama_client = ollama_client
        self.whitelist_manager = whitelist_manager

    async def handle_message(self, event):
        message_text = ''
        if event.is_group:
            if event.message.mentioned and (str(event.chat_id) in self.whitelist_manager.whitelist['group_ids']):
                message_text = event.message.message
                bot_username = (await self.telegram_client.get_me()).username
                message_text = message_text.replace(f"@{bot_username}", "").strip()
        else:
            message_text = event.message.message

        if message_text:
            with open("prompt.txt", "r") as file:
                prompt = file.read()
            prompt = prompt.replace("USER_TEXT", message_text)
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
            if m.message != answer:
                await self.telegram_client.edit_message(m, answer)

    async def ollama_chat(self, prompt):
        chat_result = await self.ollama_client.chat(messages=[{'role': 'user', 'content': prompt}], stream=True)
        async for part in await chat_result:
            yield part
