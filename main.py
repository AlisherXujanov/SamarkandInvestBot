import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from handlers import start, store, echo

async def main():
    # Logging sozlamalari
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        stream=sys.stdout
    )

    # Bot va Dispatcher yaratish
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Router-larni ro'yxatdan o'tkazish (Tartib muhim: start -> store -> echo)
    dp.include_router(start.router)
    dp.include_router(store.router)
    dp.include_router(echo.router)

    logging.info("O'yinchoqlar do'koni boti ishga tushmoqda...")
    
    # Eski kutilayotgan yangilanishlarni (updates) o'chirib tashlash
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Polling rejalarini boshlash
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi!")
