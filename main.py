import asyncio
from contextlib import asynccontextmanager
from datetime import datetime,UTC
from enum import Enum
from os import getenv

import aiogram
from aiogram import F
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton, CallbackQuery
from dotenv import load_dotenv

from MongoDb.mongo_db_factory import MongoDbFactory
from MongoDb.user_mongo_db_repository import UserMongoDbRepository

from Task_Scheduler import add_mood_notification_sub, user_session_schedule
from User import User, AiMode
from buttons import BTN_START_DIALOG, BTN_ADVICE_FOR_DAY, BTN_CHARGE_MOTIVATION, BTN_FORGET, BTN_STOP, BTN_DONATES, \
    BTN_LISTEN, BTN_SETTINGS, BTN_SETTINGS_EXIT, BTN_SETTINGS_NOTIFY_DISABLE, BTN_SETTINGS_NOTIFY_ENABLE, \
    BTN_TEXT_NOTIFY_DISABLE, BTN_TEXT_NOTIFY_ENABLE
from reply_markups import dialog_process_markup, main_markup, get_settings_keyboard
from shared import dp,sessions,scheduler,assistant,bot
from settings_callbacks import notify_disable,notify_enable
from fastapi import FastAPI, Request,Response
from aiogram.types import Update

load_dotenv()






@dp.message(F.text == "/start")
async def start_handler(message: Message):
    photo = FSInputFile("Images/Logo.jpg")
    chat_id = message.chat.id
    user_id = message.from_user.id
    rep = UserMongoDbRepository()

    session = sessions.setdefault(chat_id, User(message.from_user.id))
    session.update_activity()
    if session.get_notify_status():
                add_mood_notification_sub(scheduler=scheduler,bot=bot,chat_id=chat_id)






    await message.answer_photo(photo=photo,
                               caption="Hi! *I am Sova🦉* "
                              "I am your listener — you can open up to me, "
                               "and I will try to help you sort out your feelings",reply_markup=main_markup,
                               parse_mode="Markdown"
                               )
    user = await rep.get_user(user_id)
    if user is None:
        await rep.add_user({
            "_id": user_id,
            "notification": True,
            "language": "en",
            "created_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC),
        })



@dp.message(F.text == BTN_LISTEN)
async def listening_handler(message: Message):
    session = sessions.setdefault(message.chat.id, User(message.from_user.id))
    session.update_activity()
    session.set_mode(AiMode.LISTEN)

    await message.answer("I`m ready to listen")



@dp.message(F.text == BTN_START_DIALOG)
async def start_dialog_handler(message: Message):
    session = sessions.setdefault(message.chat.id, User(message.from_user.id))
    session.update_activity()
    session.set_mode(AiMode.DIALOG)

    res = await assistant.start_dialog(message=message.text,user=session)
    await message.answer(res,reply_markup=dialog_process_markup)



@dp.message(F.text == BTN_FORGET)
async def forget_handler(message: Message):
      chat_id = message.chat.id
      sessions.pop(chat_id)
      await message.answer("Alright, let’s start with a clean slate 🤍")







@dp.message(F.text == BTN_STOP)
async def stop_dialog_handler(message: Message):
    user = sessions.setdefault(message.chat.id, User(message.from_user.id))
    user.update_activity()
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
      user = sessions.setdefault(chat_id, User(message.from_user.id))
      user.update_activity()
      settings_keyboard = await get_settings_keyboard(user.user_id)
      return await message.answer("Settings",reply_markup=settings_keyboard)


@dp.message(F.text)
async def echo_handler(message: Message):
    user = sessions.setdefault(message.chat.id, User(message.from_user.id))
    user.update_activity()
    res = await assistant.send_message(
        message,user=user)
    await message.answer(res,reply_markup=dialog_process_markup)






WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = getenv("WEBHOOK_URL") + WEBHOOK_PATH


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    scheduler.start()
    user_session_schedule(scheduler=scheduler)
    await bot.set_webhook(WEBHOOK_URL,allowed_updates=dp.resolve_used_update_types())
    print("Webhook set:", WEBHOOK_URL)

    yield

    #  shutdown
    await bot.delete_webhook()
    await MongoDbFactory.close()
    print("Webhook removed")


app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    update = Update.model_validate(await request.json())
    await dp.feed_update(bot, update)
    return Response(status_code=200)


