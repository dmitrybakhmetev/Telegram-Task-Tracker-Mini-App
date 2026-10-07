from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)
from config import WEB_APP_URL

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
  user_name = message.from_user.first_name

  # Главное меню с инлайн-кнопками
  menu_kb = InlineKeyboardMarkup(inline_keyboard=[
      [
          InlineKeyboardButton(
              text="📅 Открыть календарь (Mini App)",
              web_app=WebAppInfo(url=WEB_APP_URL),
          )
      ],
      [
          InlineKeyboardButton(
              text="➕ Создать задачу", callback_data="btn_create_task"
          ),
          InlineKeyboardButton(
              text="📋 Список задач", callback_data="btn_list_tasks"
          ),
      ],
      [
          InlineKeyboardButton(
              text="⚙️ Управление задачами", callback_data="btn_manage_tasks"
          )
      ],
  ])

  await message.answer(
      f"Привет, {user_name}! 👋\n\nЯ твой бот-трекер задач. Выбери нужное"
      " действие с помощью меню ниже:",
      reply_markup=menu_kb,
  )