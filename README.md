# 📅 Telegram-Task-Tracker-Mini-App


Telegram-бот и Mini App для управления задачами, расписанием и ежедневными делами.

Проект построен на **Aiogram 3**, **FastAPI** и современном frontend на **HTML5, CSS3 и Vanilla JavaScript**.

---

## ✨ Возможности

* 🤖 **Telegram-бот** — команды, обработчики, FSM и клавиатуры.
* 📊 **Mini App** — удобный дашборд со статистикой и задачами.
* 📅 **Расписание** — просмотр задач по дням недели.
* ✅ **Управление задачами** — создание, редактирование и удаление.
* 🔄 **Синхронизация** — бот и Mini App работают с единым API.
* 📱 **Адаптивный интерфейс** — поддержка мобильных устройств и Telegram Desktop.

---

## 🛠 Технологии

### Backend

* Python
* FastAPI
* Pydantic
* Uvicorn
* CORS

### Telegram Bot

* Aiogram 3
* FSM
* Inline / Reply Keyboards

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript (ES6+)
* Flexbox / Grid
* CSS Variables

### Дополнительно

* `python-dotenv`
* REST API
* `.env` для конфигурации

---

## 📁 Структура проекта

```text
Telegram Task Tracker/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── handlers/
│   ├── start.py
│   └── tasks.py
│
├── keyboards/
│   └── reply.py
│
├── states/
│   └── task_states.py
│
├── api_client.py
├── app.py
├── bot.py
├── config.py
├── requirements.txt
├── .env
└── README.md
```

---

## 🚀 Установка и запуск

### 1. Клонирование

```bash
git clone https://github.com/dmitrybakhmetev/Telegram-Task-Tracker-Mini-App.git
cd "Telegram-Task-Tracker-Mini-App"
```

### 2. Виртуальное окружение

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка `.env`

Создайте файл `.env` в корне проекта:

```env
BOT_TOKEN=your_telegram_bot_token
```

> ⚠️ Не публикуйте `.env` и токен Telegram-бота в репозитории.

---

## ▶️ Запуск

Для работы проекта необходимо запустить **FastAPI** и **Telegram-бота**.

### FastAPI

```bash
uvicorn app:app --reload --port 8000
```

### Telegram-бот

В отдельном терминале:

```bash
python bot.py
```

После запуска откройте бота в Telegram и используйте Mini App.

---

## 🔌 API

| Метод    | Endpoint                         | Описание                     |
| -------- | -------------------------------- | ---------------------------- |
| `GET`    | `/api/tasks/{user_id}`           | Получить задачи пользователя |
| `POST`   | `/api/tasks`                     | Создать задачу               |
| `PUT`    | `/api/tasks/{user_id}/{task_id}` | Обновить задачу              |
| `DELETE` | `/api/tasks/{user_id}/{task_id}` | Удалить задачу               |

Документация FastAPI доступна после запуска:

```text
http://localhost:8000/docs
```

---

## 📌 Архитектура

```text
Telegram
   │
   ▼
Aiogram Bot
   │
   ▼
API Client
   │
   ▼
FastAPI
   │
   ▼
Task Management
   ▲
   │
Mini App
```

Telegram-бот и Mini App используют единый backend API для работы с задачами.

---

## 🔒 Безопасность

Конфиденциальные данные хранятся в `.env` и не должны попадать в Git.

Добавьте `.env` в `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```
