import asyncio
from bot import BOT, dp



dp.message.middleware()
dp.include_router()

async def main():
    print ("bot is running...")
    await dp.start_polling(BOT)

if __name__ == "__main__":
    asyncio.run(main())