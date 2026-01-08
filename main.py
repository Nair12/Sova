import asyncio
from enum import Enum
from os import getenv
from aiogram import Dispatcher, Bot,F
from aiogram.types import Message, FSInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from groq import Groq

from Assistant.assistant_factory import AiAssistantFactory
from notify import ask_mood_notification
from Task_Scheduler import add_mood_notification_sub
from User import User, AiMode
from buttons import BTN_START_DIALOG, BTN_ADVICE_FOR_DAY, BTN_CHARGE_MOTIVATION, BTN_FORGET, BTN_STOP, BTN_DONATES, \
    BTN_LISTEN
from reply_markups import dialog_process_markup, main_markup

load_dotenv()



users = {} # Collection to store users by chatId


TOKEN = getenv("TOKEN")
API_KEY = getenv("API_KEY")

bot = Bot(token=TOKEN)
dp = Dispatcher()


scheduler = AsyncIOScheduler(timezone="Europe/Kyiv")


assistant = AiAssistantFactory().create_assistant(provider_name="groq",api_key=API_KEY)

@dp.message(F.text == "/start")
async def start_handler(message: Message):
    photo = FSInputFile("Images/Logo.jpg")
    chat_id = message.chat.id

    users.setdefault(chat_id, User())

    add_mood_notification_sub(scheduler=scheduler,bot=bot,chat_id=chat_id)

    await message.answer_photo(photo=photo,
                               caption="Hi! *I am Sova🦉* "
                              "I am your listener — you can open up to me, "
                               "and I will try to help you sort out your feelings",reply_markup=main_markup,
                               parse_mode="Markdown"
                               )

# @dp.message(F.text("help"))
# async def help_handler(message: Message):
#     await message.answer()

@dp.message(F.text == BTN_LISTEN)
async def listening_handler(message: Message):
    user = users.setdefault(message.chat.id, User())
    user.set_mode(AiMode.LISTEN)

    await message.answer("Я готов слушать")



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
    await message.answer_photo(
        photo=FSInputFile("Images/Donates.jpg"),
        caption= "It means a lot to us that you decided to support the project 🙏\n\n"
                 "*0x91BF04B3ada6f38aa18C0EF8011044cd6706ba17* - ETH\n"
                 "*bc1qz8u9au82lwpmy2wq0qfsfar6pc82e9v7du93dv* - BTC",
        parse_mode="Markdown"


    )




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


