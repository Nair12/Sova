from math import expm1

from MongoDb.mongo_db_factory import MongoDbFactory


class UserMongoDbRepository:
    def __init__(self):
        self._users = MongoDbFactory().get_user_collection()




    async def get_user(self, _id):
           user = await self._users.find_one({'_id': _id})
           return user


    async def get_users(self):
            users = await self._users.find()
            return users


    async def add_user(self, payload):
           try:
               user = await self._users.insert_one(payload)

           except Exception:
                      print("Failed to insert user")


    async def update_user(self, payload):
        user = await self._users.update({'_id': payload['_id']}, {'$set': payload})


    async def delete_user(self, _id):
      try:
        user = await self._users.find_one({'_id': _id})
        if user:
              await self._users.delete_one({'_id': _id})
              return user
        else:
              return None
      except Exception:
          print("Failed to delete user")
          return None


    async def get_notify_status(self, _id):
          user = await self._users.find_one({'_id': _id})
          try:
               if user:
                     return user['notification']
               else:
                    return None
          except Exception:
                  print("Failed to get notification status")


    async def update_notify_status(self, _id, status):
        try:
          user = await self._users.find_one({'_id': _id})
          if user:
              await self._users.update_one({'_id': _id},  {'$set': {'notification': status}})
          else:
              return None
        except Exception:
                print("Failed to update notification status")





