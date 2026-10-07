from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Главная клавиатура внизу экрана
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Создать задачу"), KeyboardButton(text="📋 Список задач")],
        [KeyboardButton(text="⚙️ Управление задачами")],
    ],
    resize_keyboard=True,  # Делает кнопки компактными
    input_field_placeholder="Выбери действие или открой Mini App...",
)