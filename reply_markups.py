from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from MongoDb.user_mongo_db_repository import UserMongoDbRepository
from User import User
from buttons import BTN_START_DIALOG, BTN_ADVICE_FOR_DAY, BTN_CHARGE_MOTIVATION, BTN_FORGET, BTN_STOP, BTN_DONATES, \
    BTN_LISTEN, BTN_SETTINGS, BTN_TEXT_NOTIFY_DISABLE, BTN_SETTINGS_NOTIFY_DISABLE, BTN_TEXT_NOTIFY_ENABLE, \
    BTN_SETTINGS_NOTIFY_ENABLE
from shared import sessions

# Static reply markups

main_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=BTN_START_DIALOG)],
        [KeyboardButton(text=BTN_ADVICE_FOR_DAY)],
        [KeyboardButton(text=BTN_CHARGE_MOTIVATION)],
        [KeyboardButton(text=BTN_FORGET)],
        [KeyboardButton(text=BTN_DONATES)],
        [KeyboardButton(text=BTN_LISTEN)],
       [KeyboardButton(text=BTN_SETTINGS)],
    ],
    resize_keyboard=True
)
dialog_process_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=BTN_STOP)],
     ]
,
resize_keyboard=True)


async def get_settings_keyboard(_id):
    rep = UserMongoDbRepository()
    notify_status = await rep.get_notify_status(_id)
    if notify_status:
        notify_button = [InlineKeyboardButton(text=BTN_TEXT_NOTIFY_DISABLE, callback_data=BTN_SETTINGS_NOTIFY_DISABLE)]
    else:
        notify_button = [InlineKeyboardButton(text=BTN_TEXT_NOTIFY_ENABLE, callback_data=BTN_SETTINGS_NOTIFY_ENABLE)]

    setting_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            notify_button,
        ]
    )
    return setting_keyboard


