from abc import ABC, abstractmethod

from aiogram.types import Message

from User import User


class Assistant(ABC):
    def __init__(self,api_key):
        self._api_key = api_key

    @abstractmethod
    async def send_message(self,message:Message,user:User) -> str:
        pass

    @abstractmethod
    async def send_goodbye(self,message:Message,user:User) -> str:
         pass

    @abstractmethod
    async def start_dialog(self,message:Message,user:User) -> str:
         pass











