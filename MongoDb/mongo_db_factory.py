from motor.motor_asyncio import AsyncIOMotorClient
from os import getenv
from dotenv import load_dotenv


load_dotenv()




class MongoDbFactory:
    __client = None

    @classmethod
    def get_user_collection(cls):
        if cls.__client is None:
            connection_string = getenv("MONGO_URI")
            cls.__client = AsyncIOMotorClient(connection_string)

        db =  cls.__client["Sova"]
        users =  db["users"]
        return users


    @classmethod
    def close(cls):
        if cls.__client is not None:
            cls.__client.close()












