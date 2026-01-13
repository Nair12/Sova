from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from os import getenv

from Assistant.assistant_factory import AiAssistantFactory

load_dotenv()


# Shared object here. Can be used anywhere


sessions = {} # Collection to store sessions by chatId

TOKEN = getenv("TOKEN")
API_KEY = getenv("API_KEY")
PROVIDER = getenv("AI_PROVIDER")

bot = Bot(token=TOKEN)
dp = Dispatcher()


scheduler = AsyncIOScheduler(timezone="Europe/Kyiv") # Scheduler for notification


assistant = AiAssistantFactory().create_assistant(provider_name=PROVIDER,api_key=API_KEY) # Provider and api key from env