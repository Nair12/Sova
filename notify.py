import asyncio


async def ask_mood_notification(bot,chatId):
      await bot.send_message(chatId,"How are you feeling today from 1 to 5? 🤩")