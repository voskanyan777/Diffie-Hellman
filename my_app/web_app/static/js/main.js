function getCookie(name) {
    let value = `; ${document.cookie}`;
    let parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Извлекаем значения из cookie
const pValue = getCookie('p');
const gValue = getCookie('g');

const a = 6;

let A = (gValue ** a) % pValue;

let sharedSecret;
// Отправка публичного ключа на сервер
fetch('/public-key/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ public_key: A })
})
.then(response => {
    // Проверяем успешность ответа
    if (response.ok) {
        return response.json(); // Преобразуем ответ в JSON
    } else {
        throw new Error('Ошибка при получении ответа от сервера');
    }
})
.then(data => {
    console.log('Ответ от сервера:', data);

    // Используем общий секрет или что-то другое, что отправил сервер
    const B = data.B;  // Пример получения значения из ответа
    sharedSecret = (A**15) % 23
    document.cookie = `private_key=${sharedSecret}; expires=${new Date(new Date().getTime() + 7 * 24 * 60 * 60 * 1000).toUTCString()}; path=/; samesite=strict`;
    console.log("Общий секрет: ", sharedSecret)
})
.catch(error => {
    console.error('Ошибка при отправке запроса:', error);  // Обработка ошибок
});
