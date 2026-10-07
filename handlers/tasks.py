from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from states.task_states import TaskCreation

router = Router()

# Временное хранилище задач в памяти
TEMP_USER_TASKS = {}


# Состояния для управления задачами
class TaskManagement(StatesGroup):
  waiting_for_task_number = State()
  waiting_for_action = State()
  waiting_for_new_text = State()


# 1. Клик по кнопке снизу «➕ Создать задачу»
@router.message(F.text == "➕ Создать задачу")
async def start_create_task(message: types.Message, state: FSMContext):
  await message.answer(
      "✍️ **Создание новой задачи**\n\nНапиши задачу в следующем формате:\n"
      "<code>Название | ГГГГ-ММ-ДД | ЧЧ:ММ - ЧЧ:ММ</code>\n\n*Пример:* `Сделать"
      " отчет | 2026-10-08 | 10:00 - 12:30`",
      parse_mode="HTML",
  )
  await state.set_state(TaskCreation.waiting_for_task_text)


# 2. Получение текста задачи
@router.message(TaskCreation.waiting_for_task_text)
async def process_task_text(message: types.Message, state: FSMContext):
  user_text = message.text
  user_id = message.from_user.id

  if user_id not in TEMP_USER_TASKS:
    TEMP_USER_TASKS[user_id] = []

  new_task = {"id": len(TEMP_USER_TASKS[user_id]) + 1, "title": user_text}
  TEMP_USER_TASKS[user_id].append(new_task)

  await message.answer(
      f"✅ **Задача успешно сохранена!**\n\n📄 <code>{user_text}</code>",
      parse_mode="HTML",
  )
  await state.clear()


# 3. Клик по кнопке снизу «📋 Список задач»
@router.message(F.text == "📋 Список задач")
async def list_tasks_handler(message: types.Message):
  user_id = message.from_user.id
  user_tasks = TEMP_USER_TASKS.get(user_id, [])

  if not user_tasks:
    await message.answer(
        "📋 У тебя пока нет активных задач. Создай их через меню!"
    )
    return

  tasks_text = "📋 **Твои текущие задачи:**\n\n"
  for i, task in enumerate(user_tasks, 1):
    tasks_text += f"{i}. {task['title']}\n"

  await message.answer(tasks_text, parse_mode="HTML")


# 4. Клик по кнопке снизу «⚙️ Управление задачами»
@router.message(F.text == "⚙️ Управление задачами")
async def manage_tasks_handler(message: types.Message, state: FSMContext):
  user_id = message.from_user.id
  user_tasks = TEMP_USER_TASKS.get(user_id, [])

  if not user_tasks:
    await message.answer("⚙️ У тебя пока нет задач для управления.")
    return

  tasks_text = (
      "⚙️ **Управление задачами**\nВведи **номер** задачи, с которой хочешь"
      " что-то сделать:\n\n"
  )
  for i, task in enumerate(user_tasks, 1):
    tasks_text += f"[{i}] {task['title']}\n"

  await message.answer(tasks_text, parse_mode="HTML")
  await state.set_state(TaskManagement.waiting_for_task_number)


# 5. Получение номера задачи и предложение выбрать действие (Изменить / Удалить)
@router.message(TaskManagement.waiting_for_task_number)
async def process_task_number(message: types.Message, state: FSMContext):
  text = message.text.strip()
  user_id = message.from_user.id

  if not text.isdigit():
    await message.answer("❌ Пожалуйста, введи только **цифру** задачи из списка.")
    return

  task_index = int(text) - 1
  user_tasks = TEMP_USER_TASKS.get(user_id, [])

  if not (0 <= task_index < len(user_tasks)):
    await message.answer(
        "❌ Нет задачи с таким номером. Проверь список и попробуй снова."
    )
    return

  # Сохраняем выбранный индекс задачи в память состояния (FSM)
  await state.update_data(selected_task_index=task_index)

  # Создаем инлайн-кнопки выбора действия
  action_kb = types.InlineKeyboardMarkup(inline_keyboard=[
      [
          types.InlineKeyboardButton(
              text="✏️ Изменить", callback_data="action_edit"
          ),
          types.InlineKeyboardButton(
              text="❌ Удалить", callback_data="action_delete"
          ),
      ]
  ])

  selected_task = user_tasks[task_index]
  await message.answer(
      f"Выбрана задача: <b>{selected_task['title']}</b>\nЧто именно ты хочешь"
      " сделать?",
      reply_markup=action_kb,
      parse_mode="HTML",
  )
  await state.set_state(TaskManagement.waiting_for_action)


# 6. Обработка нажатия «Удалить»
@router.callback_query(
    TaskManagement.waiting_for_action, F.data == "action_delete"
)
async def delete_selected_task(callback: types.CallbackQuery, state: FSMContext):
  data = await state.get_data()
  task_index = data.get("selected_task_index")
  user_id = callback.from_user.id

  user_tasks = TEMP_USER_TASKS.get(user_id, [])
  if 0 <= task_index < len(user_tasks):
    deleted_task = user_tasks.pop(task_index)
    await callback.message.edit_text(
        f"🗑️ Задача <b>«{deleted_task['title']}»</b> успешно удалена!",
        parse_mode="HTML",
    )
  else:
    await callback.message.edit_text(
        "❌ Ошибка: задача не найдена или уже была удалена."
    )

  await state.clear()
  await callback.answer()


# 7. Обработка нажатия «Изменить»
@router.callback_query(
    TaskManagement.waiting_for_action, F.data == "action_edit"
)
async def edit_selected_task_prompt(
    callback: types.CallbackQuery, state: FSMContext
):
  await callback.message.edit_text(
      "✍️ Введи новый текст/параметры для этой задачи (в том же формате):\n"
      "<code>Название | ГГГГ-ММ-ДД | ЧЧ:ММ - ЧЧ:ММ</code>",
      parse_mode="HTML",
  )
  await state.set_state(TaskManagement.waiting_for_new_text)
  await callback.answer()


# 8. Сохранение измененного текста задачи
@router.message(TaskManagement.waiting_for_new_text)
async def save_edited_task(message: types.Message, state: FSMContext):
  new_text = message.text
  data = await state.get_data()
  task_index = data.get("selected_task_index")
  user_id = message.from_user.id

  user_tasks = TEMP_USER_TASKS.get(user_id, [])
  if 0 <= task_index < len(user_tasks):
    user_tasks[task_index]["title"] = new_text
    await message.answer(
        f"✅ Задача успешно обновлена!\n\n📄 <code>{new_text}</code>",
        parse_mode="HTML",
    )
  else:
    await message.answer("❌ Произошла ошибка при обновлении задачи.")

  await state.clear()