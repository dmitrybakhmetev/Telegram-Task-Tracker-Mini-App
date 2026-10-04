import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)

# Токен твоего бота, полученный от @BotFather
TOKEN = "8883361544:AAH2o3XyDAefVMnnOWymWzDc8BQ0aTzRoro"

# URL твоего Mini App (пока локальный или ngrok-адрес)
WEB_APP_URL = "https://your-mini-app-frontend-url.com"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()


# Состояния для FSM (если захочешь добавить диалоговое создание задачи через чат)
class TaskForm(StatesGroup):
  waiting_for_task_text = State()


# 1. Команда /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
  user_name = message.from_user.first_name

  # Клавиатура с кнопкой запуска Mini App
  webapp_kb = InlineKeyboardMarkup(inline_keyboard=[
      [
          InlineKeyboardButton(
              text="📅 Открыть календарь задач",
              web_app=WebAppInfo(url=WEB_APP_URL),
          )
      ],
      [
          InlineKeyboardButton(
              text="➕ Быстрая задача текстом", callback_data="add_task_prompt"
          )
      ],
  ])

  await message.answer(
      f"Привет, {user_name}! 👋\n\nЯ твой бот-трекер задач. Ты можешь управлять"
      " задачами прямо здесь или открыть красивый календарь в Mini App.",
      reply_markup=webapp_kb,
  )


# 2. Обработка нажатия на инлайн-кнопку быстрой задачи
@dp.callback_query(F.data == "add_task_prompt")
async def process_callback_add_task(
    callback: types.CallbackQuery, state: FSMContext
):
  await callback.message.answer(
      "Напиши текст задачи, а также дату и время (например: <i>Купить продукты"
      " 2026-10-06 15:00</i>):"
  )
  await state.set_state(TaskForm.waiting_for_task_text)
  await callback.answer()  # Закрываем часики на кнопке


# 3. Получение текста задачи через FSM (состояние ожидания)
@dp.message(TaskForm.waiting_for_task_text)
async def process_text_task(message: types.Message, state: FSMContext):
  task_text = message.text
  user_id = message.from_user.id

  # Здесь в будущем будет отправка POST-запроса на твой Core API (FastAPI)
  # Пример:
  # async with aiohttp.ClientSession() as session:
  #     await session.post("http://localhost:8000/api/tasks", json={
  #         "user_id": user_id, "title": task_text, ...
  #     })

  await message.answer(
      f"✅ <b>Задача успешно сохранена!</b>\n\n📄 {task_text}\n\nОна уже ждет"
      " тебя в календаре.",
      parse_mode="HTML",
  )
  await state.clear()  # Сбрасываем состояние


# 4. Обработка обычных текстовых сообщений (если пользователь просто пишет боту)
@dp.message(F.text & ~F.text.startswith("/"))
async def handle_any_text(message: types.Message):
  await message.answer(
      "Я получил твое сообщение. Чтобы создать задачу через чат, нажми кнопку"
      " «➕ Быстрая задача текстом» в меню /start, либо открой Mini App для"
      " полноценного управления."
  )


# Запуск поллинга
async def main():
  logging.basicConfig(
      level=logging.INFO,
      stream=sys.stdout,
      format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
  )
  print("Бот запущен и готов к работе...")
  await dp.start_polling(bot)


if __name__ == "__main__":
  asyncio.run(main())
