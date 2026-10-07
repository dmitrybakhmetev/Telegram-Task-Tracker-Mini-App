from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)
from config import WEB_APP_URL
from keyboards.reply import main_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
  user_name = message.from_user.first_name

  # Инлайн-кнопка для Mini App (внутри сообщения)
  webapp_kb = InlineKeyboardMarkup(inline_keyboard=[[
      InlineKeyboardButton(
          text="📅 Открыть календарь (Mini App)",
          web_app=WebAppInfo(url=WEB_APP_URL),
      )
  ]])

  await message.answer(
      f"Привет, {user_name}! 👋\n\nЯ твой бот-трекер задач. Нажми кнопку ниже,"
      " чтобы открыть календарь, или используй меню внизу экрана для"
      " управления задачами через чат.",
      reply_markup=webapp_kb,
  )

  # Отправляем сообщение с нижней клавиатурой
  await message.answer(
      "⬇️ Панель управления внизу:", reply_markup=main_keyboard
  )