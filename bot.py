import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import start, tasks


async def main():
  # Инициализация логирования
  logging.basicConfig(
      level=logging.INFO,
      stream=sys.stdout,
      format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
  )

  bot = Bot(token=BOT_TOKEN)
  dp = Dispatcher()

  # Подключаем роутеры (модули с обработчиками)
  dp.include_router(start.router)
  dp.include_router(tasks.router)

  print("Бот успешно запущен и готов к работе...")
  await bot.delete_webhook(drop_pending_updates=True)
  await dp.start_polling(bot)


if __name__ == "__main__":
  asyncio.run(main())