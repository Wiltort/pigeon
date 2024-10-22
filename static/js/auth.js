function switchTab(tabName) {
    const tabs = document.querySelectorAll('.tab');
    const forms = document.querySelectorAll('.form');
    
    tabs.forEach(tab => tab.classList.remove('active'));
    forms.forEach(form => form.classList.remove('active'));
    
    document.querySelector(`.tab:nth-child(${tabName === 'login' ? '1' : '2'})`).classList.add('active');
    document.getElementById(`${tabName}Form`).classList.add('active');
  }

const validateForm = fields => fields.every(field => field.trim() !== '');

// Функция для отправки запросов
const sendRequest = async (url, data) => {
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            alert(result.message || 'Операция выполнена успешно!');
            return result;
        } else {
            alert(result.message || 'Ошибка выполнения запроса!');
            return null;
        }
    } catch (error) {
        console.error("Ошибка:", error);
        alert('Произошла ошибка на сервере');
    }
};

// Функция для обработки формы
const handleFormSubmit = async (formType, url, fields) => {
    if (!validateForm(fields)) {
        alert('Пожалуйста, заполните все поля.');
        return;
    }

    const data = await sendRequest(url, formType === 'login'
        ? {email: fields[0], password: fields[1]}
        : {email: fields[0], username: fields[1], password: fields[2], password_check: fields[3], telegram: fields[4]});

    if (data && formType === 'login') {
        window.location.href = '/chat';
    }
};




document.getElementById('loginForm').addEventListener('click', async (event) => {
    e.preventDefault();
    // Здесь будет логика отправки данных для входа
    const email = document.querySelector('#loginForm input[type="email"]').value;
    const password = document.querySelector('#loginForm input[type="password"]').value;
    await handleFormSubmit('login', 'login/', [email, password]);
});

document.getElementById('registerForm').addEventListener('click', async (event) => {
    e.preventDefault();
    // Здесь будет логика отправки данных для регистрации
    const email = document.querySelector('#registerForm input[type="email"]').value;
    const username = document.querySelector('#registerForm input[type="text"]')[0].value;
    const password = document.querySelectorAll('#registerForm input[type="password"]')[0].value;
    const password_check = document.querySelectorAll('#registerForm input[type="password"]')[1].value;
    const telegram = document.querySelector('#registerForm input[type="text"]')[1].value;


    if (password !== password_check) {
        alert('Пароли не совпадают.');
        return;
    }
    if (!telegram.startsWith('@')) {
        alert('Логин телеграм должен начинатся с символа "@"');
        return;
    }
    

    await handleFormSubmit('register', 'register/', [email, username, password, password_check, telegram]);
  });

