import asyncio
from enum import Enum
from os import getenv

import aiogram
from aiogram import Dispatcher, Bot,F
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.text_decorations import markdown_decoration
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from groq import Groq

from Assistant.assistant_factory import AiAssistantFactory
from notify import ask_mood_notification
from Task_Scheduler import add_mood_notification_sub
from User import User, AiMode
from buttons import BTN_START_DIALOG, BTN_ADVICE_FOR_DAY, BTN_CHARGE_MOTIVATION, BTN_FORGET, BTN_STOP, BTN_DONATES, \
    BTN_LISTEN, BTN_SETTINGS
from reply_markups import dialog_process_markup, main_markup

load_dotenv()



users = {} # Collection to store users by chatId


TOKEN = getenv("TOKEN")
API_KEY = getenv("API_KEY")
PROVIDER = getenv("AI_PROVIDER")

bot = Bot(token=TOKEN)
dp = Dispatcher()


scheduler = AsyncIOScheduler(timezone="Europe/Kyiv")


assistant = AiAssistantFactory().create_assistant(provider_name=PROVIDER,api_key=API_KEY) # Provider and api key from env

@dp.message(F.text == "/start")
async def start_handler(message: Message):
    photo = FSInputFile("Images/Logo.jpg")
    chat_id = message.chat.id

    user = users.setdefault(chat_id, User())

    if user.get_notify_status():
                add_mood_notification_sub(scheduler=scheduler,bot=bot,chat_id=chat_id)


    await message.answer_photo(photo=photo,
                               caption="Hi! *I am Sova🦉* "
                              "I am your listener — you can open up to me, "
                               "and I will try to help you sort out your feelings",reply_markup=main_markup,
                               parse_mode="Markdown"
                               )



@dp.message(F.text == BTN_LISTEN)
async def listening_handler(message: Message):
    user = users.setdefault(message.chat.id, User())
    user.set_mode(AiMode.LISTEN)

    await message.answer("I`m ready to listen")



@dp.message(F.text == BTN_START_DIALOG)
async def start_dialog_handler(message: Message):
    user = users.setdefault(message.chat.id, User())
    user.set_mode(AiMode.DIALOG)
    res = await assistant.start_dialog(message=message,user=user)
    return message.answer(res,reply_markup=dialog_process_markup)



@dp.message(F.text == BTN_FORGET)
async def forget_handler(message: Message):
      chat_id = message.chat.id
      users.pop(chat_id)
      await message.answer("Alright, let’s start with a clean slate 🤍")







@dp.message(F.text == BTN_STOP)
async def stop_dialog_handler(message: Message):

    user = users.setdefault(message.chat.id, User())
    res  = await assistant.send_goodbye(message=message,user=user)
    await message.answer(res,reply_markup=main_markup)





@dp.message(F.text == BTN_DONATES)
async def donates_handler(message: Message):


    wallet_eth = "0x91BF04B3ada6f38aa18C0EF8011044cd6706ba17"
    wallet_btc = "bc1qz8u9au82lwpmy2wq0qfsfar6pc82e9v7du93dv"

    text = (
        "It means a lot to us that you decided to support the project 🙏\n\n"
        f"<b><code>{aiogram.html.quote(wallet_eth)}</code></b> - ETH\n\n"
        f"<b><code>{aiogram.html.quote(wallet_btc)}</code></b> - BTC"
    )






    await message.answer_photo(
        photo=FSInputFile("Images/Donates.jpg"),
        caption= text,
        parse_mode="HTML"

    )

@dp.message(F.text == BTN_SETTINGS)
async def settings_handler(message: Message):
      chat_id = message.chat.id
      user = users.setdefault(chat_id, User())

      notify_status = user.get_notify_status()

      settings_markup = ReplyKeyboardMarkup(
          keyboard=[
              [KeyboardButton(text=BTN_START_DIALOG)],

          ]
      )

      return await message.answer("",reply_markup=settings_markup)


@dp.message(F.text)
async def echo_handler(message: Message):
    user = users.setdefault(message.chat.id, User())
    res = await assistant.send_message(
        message,user=user)
    await message.answer(res,reply_markup=dialog_process_markup)









async def main():
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


