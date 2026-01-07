import asyncio
from bot import BOT, dp
from handlers.start_handlers import start_router
from handlers.customer_handlers import customer_router
from middlewares.db_session_middleware import DbSessionMiddleware




dp.message.middleware(DbSessionMiddleware())
dp.include_router(start_router)
dp.include_router(customer_router)


async def main():
    print ("bot is running...")
    await dp.start_polling(BOT)

if __name__ == "__main__":
    asyncio.run(main())