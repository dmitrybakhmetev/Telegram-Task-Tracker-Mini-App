const tg = window.Telegram.WebApp;
tg.expand();

const user = tg.initDataUnsafe?.user;
const userId = user ? user.id : 123456;
const userName = user ? user.first_name : "Дмитрий";
document.getElementById('user-profile').innerHTML = `👤 ${userName}`;

const API_URL = "http://localhost:8000";
let allTasks = [];
let currentWeekOffset = 0;

const monthNames = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"];

function switchView(viewName, element) {
    document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active-view'));
    document.getElementById(`view-${viewName}`).classList.add('active-view');

    document.querySelectorAll('.menu-item, .mob-item').forEach(el => el.classList.remove('active'));
    if (element) element.classList.add('active');

    if (viewName === 'dashboard') updateDashboard();
    if (viewName === 'schedule') renderWeekView();
}

async function init() {
    await loadTasks();
}

async function loadTasks() {
    try {
        const res = await fetch(`${API_URL}/api/tasks/${userId}`);
        allTasks = await res.json();
    } catch (e) {
        allTasks = [];
    }
    updateDashboard();
    renderWeekView();
}

function changeWeek(direction) {
    currentWeekOffset += direction;
    renderWeekView();
}

// Обновление дашборда
function updateDashboard() {
    document.getElementById('dash-total').innerText = allTasks.length;
    
    const todayStr = new Date().toISOString().split('T')[0];
    const todayTasks = allTasks.filter(t => t.date === todayStr);
    document.getElementById('dash-today-count').innerText = todayTasks.length;

    const upcomingContainer = document.getElementById('dash-upcoming-list');
    if (allTasks.length === 0) {
        upcomingContainer.innerHTML = '<p style="color: var(--text-secondary); font-size: 13px; margin:0;">Нет запланированных задач.</p>';
        return;
    }

    const sorted = [...allTasks].sort((a,b) => new Date(a.date) - new Date(b.date)).slice(0, 4);
    upcomingContainer.innerHTML = sorted.map(t => `
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; background: var(--bg-app); border-radius: 10px; cursor: pointer;" onclick="openEditModal(${t.id})">
            <div>
                <strong style="font-size: 14px;">${t.title}</strong>
                <div style="font-size: 11px; color: var(--text-secondary);">📅 ${t.date} | ⏰ ${t.start_time} - ${t.end_time}</div>
            </div>
            <span style="font-size: 12px; color: var(--accent-color); font-weight: 500;">Изменить ›</span>
        </div>
    `).join('');
}

// Рендер недели
function renderWeekView() {
    const grid = document.getElementById('week-grid');
    grid.innerHTML = '';

    const today = new Date();
    const startOfWeek = new Date(today);
    const dayOfWeek = today.getDay() || 7;
    startOfWeek.setDate(today.getDate() - dayOfWeek + 1 + (currentWeekOffset * 7));

    const todayStr = today.toISOString().split('T')[0];
    const cardColors = ['yellow', 'blue', 'pink'];
    let monthTitleStr = "";

    for (let i = 0; i < 7; i++) {
        const d = new Date(startOfWeek);
        d.setDate(startOfWeek.getDate() + i);

        const yyyy = d.getFullYear();
        const mm = String(d.getMonth() + 1).padStart(2, '0');
        const dd = String(d.getDate()).padStart(2, '0');
        const dateStr = `${yyyy}-${mm}-${dd}`;

        if (i === 0) monthTitleStr = `${monthNames[d.getMonth()]} ${yyyy}`;

        const dayNames = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС'];
        const isToday = dateStr === todayStr;

        const column = document.createElement('div');
        column.className = 'day-column';

        column.innerHTML = `
            <div class="day-column-header ${isToday ? 'active-day' : ''}">
                <div class="name">${dayNames[i]}</div>
                <div class="num">${d.getDate()}</div>
            </div>
        `;

        const dayTasks = allTasks.filter(t => t.date === dateStr);
        
        if (dayTasks.length === 0) {
            column.innerHTML += `<div style="font-size: 11px; color: var(--text-secondary); text-align: center; margin-top: 20px;">Нет задач</div>`;
        } else {
            dayTasks.forEach((task, idx) => {
                const colorClass = cardColors[idx % cardColors.length];
                column.innerHTML += `
                    <div class="task-card ${colorClass}" onclick="openEditModal(${task.id})">
                        <button class="task-delete" onclick="event.stopPropagation(); deleteTask(${task.id})">×</button>
                        <span class="time">⏰ ${task.start_time} - ${task.end_time}</span>
                        <div class="title">${task.title}</div>
                    </div>
                `;
            });
        }
        grid.appendChild(column);
    }
    document.getElementById('current-month-label').innerText = monthTitleStr;
}

// Модальное окно (Создание / Редактирование)
function openCreateModal() {
    document.getElementById('modal-title').innerText = 'Новое событие';
    document.getElementById('task-id').value = '';
    document.getElementById('task-title').value = '';
    document.getElementById('task-date').value = new Date().toISOString().split('T')[0];
    document.getElementById('task-start').value = '10:00';
    document.getElementById('task-end').value = '11:00';
    document.getElementById('taskModal').style.display = 'flex';
}

function openEditModal(taskId) {
    const task = allTasks.find(t => t.id === taskId);
    if (!task) return;

    document.getElementById('modal-title').innerText = 'Редактировать задачу';
    document.getElementById('task-id').value = task.id;
    document.getElementById('task-title').value = task.title;
    document.getElementById('task-date').value = task.date;
    document.getElementById('task-start').value = task.start_time;
    document.getElementById('task-end').value = task.end_time;
    document.getElementById('taskModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('taskModal').style.display = 'none';
}

async function saveTask() {
    const taskId = document.getElementById('task-id').value;
    const title = document.getElementById('task-title').value;
    const date = document.getElementById('task-date').value;
    const start_time = document.getElementById('task-start').value;
    const end_time = document.getElementById('task-end').value;

    if (!title || !date) {
        alert('Заполни название и дату!');
        return;
    }

    if (taskId) {
        await fetch(`${API_URL}/api/tasks/${userId}/${taskId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, date, start_time, end_time })
        });
    } else {
        await fetch(`${API_URL}/api/tasks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, title, date, start_time, end_time })
        });
    }

    closeModal();
    loadTasks();
}

async function deleteTask(taskId) {
    await fetch(`${API_URL}/api/tasks/${userId}/${taskId}`, {
        method: 'DELETE'
    });
    loadTasks();
}

init();