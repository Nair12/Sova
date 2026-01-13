from aiogram.types import CallbackQuery

from buttons import BTN_SETTINGS_NOTIFY_ENABLE, BTN_SETTINGS_NOTIFY_DISABLE
from reply_markups import get_settings_keyboard
from shared import dp,sessions
from aiogram import F
from MongoDb.user_mongo_db_repository import UserMongoDbRepository




@dp.callback_query(F.data == BTN_SETTINGS_NOTIFY_DISABLE)
async def notify_disable(call: CallbackQuery):
    print(f"Notify disable  started id : {call.message.chat.id} ")
    session = sessions.get(call.message.chat.id)
    if session:
        rep = UserMongoDbRepository()
        await rep.update_notify_status(session.user_id, False)
        setting_markup = await get_settings_keyboard(call.message.chat.id)
        await call.message.answer(text="Settings",reply_markup=setting_markup)



@dp.callback_query(F.data == BTN_SETTINGS_NOTIFY_ENABLE)
async def notify_enable(call: CallbackQuery):
    print(f"Notify enable  started id : {call.message.chat.id} ")
    session = sessions.get(call.message.chat.id)
    if session:
        rep = UserMongoDbRepository()
        await rep.update_notify_status(session.user_id, True)
        setting_markup = await get_settings_keyboard(call.message.chat.id)
        await call.message.answer(text="Settings", reply_markup=setting_markup)
