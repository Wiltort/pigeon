// Добавление нового чата
document.querySelector('.new-chat-btn').addEventListener('click', () => {
    const newContact = prompt('Введите имя нового контакта:');
    if (newContact) {
      const li = document.createElement('li');
      li.textContent = newContact;
      document.querySelector('.contact-list').appendChild(li);
    }
  });

  // Отправка сообщения
  document.querySelector('.chat-input button').addEventListener('click', () => {
    const input = document.querySelector('.chat-input input');
    const message = input.value.trim();
    if (message) {
      const div = document.createElement('div');
      div.className = 'message sent';
      div.textContent = message;
      document.querySelector('.chat-history').appendChild(div);
      input.value = '';
    }
  });

  // Выход из чата
  document.querySelector('.logout-btn').addEventListener('click', () => {
    if (confirm('Вы уверены, что хотите выйти?')) {
      alert('Выход выполнен успешно');
      // Здесь можно добавить логику для выхода из системы
    }
  });