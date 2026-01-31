import asyncio
from bot import BOT, dp
from handlers.start_handlers import start_router
from handlers.customer_handlers import customer_router
from middlewares.db_middlewares import DbSessionMiddleware




# Attach the DB session middleware to all message handlers
# Each handler will receive an async SQLAlchemy session as `db` in its data dict
# Handles automatic commit/rollback per handler
dp.message.middleware(DbSessionMiddleware())


# Register all customer-related handlers from customer_router
# This allows organizing handlers in separate modules (routers)
# Keeps the main dispatcher clean and modular
dp.include_router(start_router)
dp.include_router(customer_router)


async def main():
    print ("bot is running...")
    await dp.start_polling(BOT)

if __name__ == "__main__":
    asyncio.run(main())