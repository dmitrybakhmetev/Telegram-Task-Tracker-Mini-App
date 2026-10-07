from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Task Tracker Core API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

# Монтируем папку сразу на ДВА возможных пути, чтобы сервер не выдавал 404
app.mount("/frontend", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend")
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

IN_MEMORY_TASKS = {}

class TaskCreate(BaseModel):
    user_id: int
    title: str
    date: str
    start_time: str
    end_time: str

class TaskUpdate(BaseModel):
    title: str
    date: str
    start_time: str
    end_time: str

@app.get("/")
def read_index():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/api/tasks/{user_id}")
def get_tasks(user_id: int):
    return IN_MEMORY_TASKS.get(user_id, [])

@app.post("/api/tasks")
def create_task(task: TaskCreate):
    if task.user_id not in IN_MEMORY_TASKS:
        IN_MEMORY_TASKS[task.user_id] = []

    user_tasks = IN_MEMORY_TASKS[task.user_id]
    new_id = max([t["id"] for t in user_tasks], default=0) + 1

    new_task = {
        "id": new_id,
        "title": task.title,
        "date": task.date,
        "start_time": task.start_time,
        "end_time": task.end_time,
    }
    user_tasks.append(new_task)
    return {"status": "success", "task": new_task}

@app.put("/api/tasks/{user_id}/{task_id}")
def update_task(user_id: int, task_id: int, task_data: TaskUpdate):
    if user_id not in IN_MEMORY_TASKS:
        raise HTTPException(status_code=404, detail="User not found")

    for task in IN_MEMORY_TASKS[user_id]:
        if task["id"] == task_id:
            task["title"] = task_data.title
            task["date"] = task_data.date
            task["start_time"] = task_data.start_time
            task["end_time"] = task_data.end_time
            return {"status": "success", "task": task}

    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/api/tasks/{user_id}/{task_id}")
def delete_task(user_id: int, task_id: int):
    if user_id not in IN_MEMORY_TASKS:
        raise HTTPException(status_code=404, detail="User not found")

    user_tasks = IN_MEMORY_TASKS[user_id]
    for i, task in enumerate(user_tasks):
        if task["id"] == task_id:
            deleted = user_tasks.pop(i)
            return {"status": "success", "deleted": deleted}

    raise HTTPException(status_code=404, detail="Task not found")