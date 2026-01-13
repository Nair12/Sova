import enum
import uuid
from datetime import datetime,UTC

from MongoDb.user_mongo_db_repository import UserMongoDbRepository


class AiMode(enum.Enum):
    DIALOG = 1
    VOICE = 2
    LISTEN = 3




class User:
    def __init__(self,_id):
        self.__dialog = []
        self.__mode = AiMode.DIALOG
        self.__notify_enabled = True
        self.last_activity = datetime.now(UTC)
        self.user_id = _id

    def add_message(self,obj):
        self.__dialog.append(obj)
        if self.__dialog.__len__() > 15:
            self.__dialog.pop(0)

    def get_dialog(self):
        return self.__dialog

    def get_mode(self):
        return self.__mode

    def set_mode(self,mode:AiMode):
        self.__mode = mode

    def update_activity(self):
        self.last_activity = datetime.now(UTC)












