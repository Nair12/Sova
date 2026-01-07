from aiogram.types import Message
from groq import Groq

from User import User
from Assistant.assistant import Assistant


class GorqAssistant(Assistant):


    def __init__(self,api_key):
        super().__init__(api_key)
        self.client = Groq(api_key=api_key)




    async def send_message(self,message: Message,user:User) -> str:
        chat_id = message.chat.id
        user.add_message({
            "role": "user",
            "content": message.text
        })
        completion = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are Sova, an empathetic AI psychologist. reply in the language of the last message"},
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
                 "content": "You are Sova, an empathetic AI psychologist. The person is leaving you, say goodbye and give a short parting word based on the conversation"},
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
                 "content": "You are Sova, an empathetic AI psychologist. A someone came to see you, greet him"},
                {"role": "user", "content": "Здраствуйте!"}
            ]
        )
        return completion.choices[0].message.content


    async def enable_listen_mode(self,message: Message,user: User):
        chat_id = message.chat.id

        completion = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are Sova, an empathetic AI psychologist."},
                *user.get_dialog(),
                {"role": "system", "content": "You switch to the listening mode, "
                                              "your task is to listen and respond briefly, "
                                              "as if you are having a conversation and the person is speaking to you, "
                                              "respond in the language of the dialogue, "
                                              "if there is no dialogue, then in Russian"},

            ]
        )
        return completion.choices[0].message.content



