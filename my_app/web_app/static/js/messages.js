document.getElementById('login-form').addEventListener('submit', function (event) {

    // Останавливаем отправку формы, чтобы выполнить шифрование
    event.preventDefault();

    const private_key = localStorage.getItem("shared_private_key")

    // Получаем значения логина и пароля
    const login = document.getElementById('login').value;
    const message = document.getElementById('message').value;

    console.log(`login: ${login}`)
    console.log(`message: ${message}`)

    const encryptedLogin = CryptoJS.AES.encrypt(login, private_key).toString();
    const encryptedMessage = CryptoJS.AES.encrypt(message, private_key).toString();

    console.log(`encrypted login: ${encryptedLogin}`)
    console.log(`encrypted message: ${encryptedMessage}`)

    document.getElementById('login').value = encryptedLogin
    document.getElementById('message').value = encryptedMessage

    this.submit()
});