from aiogram.types import Message
from groq import Groq

from User import User, AiMode
from Assistant.assistant import Assistant


class GorqAssistant(Assistant):


    def __init__(self,api_key):
        super().__init__(api_key)
        self.client = Groq(api_key=api_key)
        self.systemPrompt = """ You're an AI assistant, Owl. Your job is to listen to people as truthfully as possible and offer advice. Act like a friend who listens and supports them, not like in a psychologist's office, but like a friend trying to support them. Don't ask too many questions; answer only in the language of the user's last message. Avoid multilingual responses. """




    async def send_message(self,message: Message,user:User) -> str:
        chat_id = message.chat.id

        mode = user.get_mode()
        ai_role = None
        if mode == AiMode.LISTEN:
            ai_role =  {"role": "system", "content": "You are Sova, an empathetic AI psychologist. now you in listening mode, answer shortly and listen like friend. Do not generate multilanguage text"}
        elif mode == AiMode.DIALOG:
            ai_role =  {"role": "system", "content": self.systemPrompt}



        user.add_message({
            "role": "user",
            "content": message.text
        })
        completion = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                ai_role,
                *user.get_dialog(),
            ]
        )

        user.add_message({
            "role": "assistant",
            "content": completion.choices[0].message.content
        })

        return completion.choices[0].message.content

    async def send_goodbye(self,message: Message,user:User) -> str:
        completion = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system",
                 "content": f"{self.systemPrompt} The person is leaving you, say goodbye and give a short parting word based on the conversation"},
                *user.get_dialog(),
                {"role": "user", "content": "Спасибо за поддержку!"}
            ]
        )
        return completion.choices[0].message.content


    async def start_dialog(self,message: Message,user:User) -> str:
        completion = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system",
                 "content": f"{self.systemPrompt} A someone came to see you, greet him"},
                {"role": "user", "content": "Здраствуйте!"}
            ]
        )
        return completion.choices[0].message.content






