from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from User import User
from buttons import BTN_SETTINGS, BTN_SETTINGS_NOTIFY_DISABLE, BTN_SETTINGS_NOTIFY_ENABLE, BTN_START_DIALOG, \
    BTN_SETTINGS_EXIT
from shared import  dp
from aiogram import F

from shared import sessions


@dp.message_handler(F.text == BTN_SETTINGS_EXIT)
async def exit_welcome(message: Message):
    pass



@dp.message(F.text == BTN_SETTINGS)
async def settings_handler(message: Message):
      chat_id = message.chat.id
      user = sessions.setdefault(chat_id, User())

      notify_status = user.get_notify_status()

      if notify_status:
          notify_button = [KeyboardButton(text=BTN_SETTINGS_NOTIFY_DISABLE)]
      else:
          notify_button = [KeyboardButton(text=BTN_SETTINGS_NOTIFY_ENABLE)]



      settings_markup = ReplyKeyboardMarkup(
          keyboard=[
              [KeyboardButton(text=BTN_START_DIALOG)],
              [KeyboardButton(text=BTN_SETTINGS_EXIT)],
              notify_button
          ],
          resize_keyboard=True
      )

      return await message.answer("Settings",reply_markup=settings_markup)

