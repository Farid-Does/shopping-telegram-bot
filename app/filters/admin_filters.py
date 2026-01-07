# admin handlers filters

# from aiogram.filters import BaseFilter
# from aiogram.types import Message
# import os




# admins = list(map(int, os.getenv("ADMINS").split(",")))

# class IsAdminFilter(BaseFilter):
#     async def __call__(self, message: Message):
#         return message.from_user.id in admins