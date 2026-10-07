from aiogram.fsm.state import State, StatesGroup


class TaskCreation(StatesGroup):
  waiting_for_task_text = State()