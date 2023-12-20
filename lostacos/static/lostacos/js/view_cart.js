function clearCart() {
    // Отправляем AJAX-запрос на сервер для очистки корзины
    fetch('/clear_cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), // Добавляем CSRF-токен
        },
        // body: JSON.stringify(data), // Можно передать данные, если необходимо
    })
    .then(response => response.json())
    .then(data => {
        // Обработка ответа от сервера
        alert(data.message); // Вместо alert можно использовать другие методы обратной связи с пользователем
        // Дополнительные действия после очистки корзины (например, обновление отображения)
    })
}

// Функция для получения CSRF-токена из cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

