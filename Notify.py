import asyncio


async def ask_mood_notification(bot,chatId):
      await asyncio.sleep(120)
      await bot.send_message(chatId,"Как ты себя чувствуешь от 1 до 5 ? 🤩")