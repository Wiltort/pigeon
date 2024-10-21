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






document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    // Здесь будет логика отправки данных для входа
    console.log('Отправка формы входа');
  });

document.getElementById('registerForm').addEventListener('submit', function(e) {
    e.preventDefault();
    // Здесь будет логика отправки данных для регистрации
    console.log('Отправка формы регистрации');
  });

