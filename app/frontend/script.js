const API_URL = window.location.hostname === 'localhost' && window.location.port !== '80'
    ? 'http://localhost:8000/api/v1'
    : '/api/v1';

// Переключение форм
document.getElementById('show-register').addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('login-form').classList.add('hidden');
    document.getElementById('register-form').classList.remove('hidden');
    hideMessage();
});

document.getElementById('show-login').addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('register-form').classList.add('hidden');
    document.getElementById('login-form').classList.remove('hidden');
    hideMessage();
});

// Регистрация
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
        name: document.getElementById('reg-name').value,
        email: document.getElementById('reg-email').value,
        password: document.getElementById('reg-password').value,
    };

    try {
        const response = await fetch(`${API_URL}/users`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            showMessage('Пользователь создан! Переход на вход...', 'success');
            document.getElementById('register-form').reset();
            setTimeout(() => {
                document.getElementById('show-login').click();
            }, 1500);
        } else {
            const error = await response.json();
            showMessage(error.detail || 'Ошибка регистрации', 'error');
        }
    } catch (err) {
        showMessage('Не удалось подключиться к серверу', 'error');
    }
});

// Вход
document.getElementById('login-form').addEventListener('submit', (e) => {
    e.preventDefault();
    localStorage.setItem('isLoggedIn', 'true');
    window.location.href = 'dashboard.html';
});

// Утилиты
function showMessage(text, type = 'success') {
    const el = document.getElementById('message');
    el.textContent = text;
    el.className = `message ${type}`;
}

function hideMessage() {
    const el = document.getElementById('message');
    el.className = 'message hidden';
}
