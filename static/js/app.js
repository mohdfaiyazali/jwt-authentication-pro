const API_BASE = '/api';
const ACCESS_TOKEN_KEY = 'jwt_access_token';
const REFRESH_TOKEN_KEY = 'jwt_refresh_token';

function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

function getRefreshToken() {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
}

function setTokens(access, refresh) {
  localStorage.setItem(ACCESS_TOKEN_KEY, access);
  localStorage.setItem(REFRESH_TOKEN_KEY, refresh);
}

function clearTokens() {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
}

function showMessage(container, message, type = 'info') {
  if (!container) return;
  container.className = `alert alert-${type}`;
  container.textContent = message;
  container.classList.remove('d-none');
}

async function apiRequest(path, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
  const token = getAccessToken();
  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (response.status === 401 && getRefreshToken()) {
    const refreshed = await refreshAccessToken();
    if (refreshed) return apiRequest(path, options);
  }
  return response;
}

async function refreshAccessToken() {
  const refresh = getRefreshToken();
  if (!refresh) return false;
  const response = await fetch(`${API_BASE}/token/refresh/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh })
  });
  if (!response.ok) {
    clearTokens();
    return false;
  }
  const data = await response.json();
  localStorage.setItem(ACCESS_TOKEN_KEY, data.access);
  return true;
}

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('loginForm');
  const registerForm = document.getElementById('registerForm');
  const taskForm = document.getElementById('taskForm');
  const taskList = document.getElementById('taskList');
  const taskCount = document.getElementById('taskCount');
  const taskMessage = document.getElementById('taskMessage');
  const authMessage = document.getElementById('authMessage');
  const searchInput = document.getElementById('searchInput');
  const refreshTasksBtn = document.getElementById('refreshTasksBtn');
  const logoutBtn = document.getElementById('logoutBtn');

  let taskFilter = 'all';

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const formData = new FormData(loginForm);
      const payload = Object.fromEntries(formData.entries());
      const response = await fetch(`${API_BASE}/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await response.json();
      if (!response.ok) {
        showMessage(authMessage, data.detail || data.message || 'Login failed.', 'danger');
        return;
      }
      setTokens(data.access, data.refresh);
      window.location.href = '/tasks/';
    });
  }

  if (registerForm) {
    registerForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const formData = new FormData(registerForm);
      const payload = Object.fromEntries(formData.entries());
      const response = await fetch(`${API_BASE}/register/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await response.json();
      if (!response.ok) {
        showMessage(authMessage, JSON.stringify(data), 'danger');
        return;
      }
      showMessage(authMessage, data.message, 'success');
      registerForm.reset();
      setTimeout(() => window.location.href = '/login/', 1200);
    });
  }

  async function loadTasks() {
    if (!taskList) return;
    const query = new URLSearchParams();
    if (taskFilter === 'done') query.set('completed', 'true');
    if (taskFilter === 'open') query.set('completed', 'false');
    if (searchInput && searchInput.value.trim()) query.set('search', searchInput.value.trim());

    const response = await apiRequest(`/tasks/${query.toString() ? `?${query.toString()}` : ''}`);
    if (response.status === 401) {
      clearTokens();
      window.location.href = '/login/';
      return;
    }
    const data = await response.json();
    const tasks = data.results || data;
    taskList.innerHTML = '';
    taskCount.textContent = `${tasks.length} item${tasks.length === 1 ? '' : 's'}`;

    if (!tasks.length) {
      taskList.innerHTML = '<div class="task-item text-white-50">No tasks yet.</div>';
      return;
    }

    tasks.forEach((task) => {
      const item = document.createElement('div');
      item.className = 'task-item fade-in';
      item.innerHTML = `
        <div class="d-flex flex-column flex-md-row justify-content-between gap-3">
          <div>
            <div class="task-title">${task.completed ? '[Done] ' : ''}${task.title}</div>
            <div class="task-meta">Created ${new Date(task.created_at).toLocaleString()}</div>
          </div>
          <div class="task-actions d-flex flex-wrap gap-2">
            <button class="btn btn-sm btn-outline-light" data-action="toggle">Toggle</button>
            <button class="btn btn-sm btn-outline-info" data-action="edit">Edit</button>
            <button class="btn btn-sm btn-outline-danger" data-action="delete">Delete</button>
          </div>
        </div>
      `;
      item.querySelector('[data-action="toggle"]').addEventListener('click', () => updateTask(task, { completed: !task.completed }));
      item.querySelector('[data-action="edit"]').addEventListener('click', async () => {
        const newTitle = prompt('Update task title', task.title);
        if (newTitle && newTitle.trim()) await updateTask(task, { title: newTitle.trim() });
      });
      item.querySelector('[data-action="delete"]').addEventListener('click', () => deleteTask(task.id));
      taskList.appendChild(item);
    });
  }

  async function updateTask(task, payload) {
    const response = await apiRequest(`/tasks/${task.id}/`, {
      method: 'PATCH',
      body: JSON.stringify(payload)
    });
    if (response.ok) {
      showMessage(taskMessage, 'Task updated.', 'success');
      loadTasks();
    } else {
      showMessage(taskMessage, 'Unable to update task.', 'danger');
    }
  }

  async function deleteTask(taskId) {
    const response = await apiRequest(`/tasks/${taskId}/`, { method: 'DELETE' });
    if (response.ok) {
      showMessage(taskMessage, 'Task deleted.', 'success');
      loadTasks();
    } else {
      showMessage(taskMessage, 'Unable to delete task.', 'danger');
    }
  }

  if (taskForm) {
    taskForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const formData = new FormData(taskForm);
      const payload = Object.fromEntries(formData.entries());
      const response = await apiRequest('/tasks/', {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      if (response.ok) {
        taskForm.reset();
        showMessage(taskMessage, 'Task created.', 'success');
        loadTasks();
      } else {
        showMessage(taskMessage, 'Unable to create task.', 'danger');
      }
    });
  }

  if (searchInput) {
    searchInput.addEventListener('input', () => loadTasks());
  }

  document.querySelectorAll('[data-filter]').forEach((button) => {
    button.addEventListener('click', () => {
      taskFilter = button.dataset.filter;
      loadTasks();
    });
  });

  if (refreshTasksBtn) refreshTasksBtn.addEventListener('click', () => loadTasks());
  if (logoutBtn) {
    logoutBtn.addEventListener('click', async () => {
      const refresh = getRefreshToken();
      if (refresh) {
        await fetch(`${API_BASE}/logout/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${getAccessToken()}` },
          body: JSON.stringify({ refresh })
        });
      }
      clearTokens();
      window.location.href = '/';
    });
  }

  if (taskList) {
    if (!getAccessToken()) {
      window.location.href = '/login/';
      return;
    }
    loadTasks();
  }
});
