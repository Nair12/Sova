from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from buttons import BTN_START_DIALOG, BTN_ADVICE_FOR_DAY, BTN_CHARGE_MOTIVATION, BTN_FORGET, BTN_STOP, BTN_DONATES, \
    BTN_LISTEN

main_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=BTN_START_DIALOG)],
        [KeyboardButton(text=BTN_ADVICE_FOR_DAY)],
        [KeyboardButton(text=BTN_CHARGE_MOTIVATION)],
        [KeyboardButton(text=BTN_FORGET)],
        [KeyboardButton(text=BTN_DONATES)],
        [KeyboardButton(text=BTN_LISTEN)],
    ],
    resize_keyboard=True
)
dialog_process_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=BTN_STOP)],
     ]
,
resize_keyboard=True)