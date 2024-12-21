function getCookie(name) {
    let value = `; ${document.cookie}`;
    let parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}
const private_key = getCookie('private_key')
document.getElementById('login-form').addEventListener('submit', function (event) {
    // Останавливаем отправку формы, чтобы выполнить шифрование
    event.preventDefault();

    // Получаем значения логина и пароля
    const login = document.getElementById('login').value;
    const password = document.getElementById('password').value;

    // Используем CryptoJS для шифрования пароля
    const encryptedPassword = CryptoJS.AES.encrypt(password, private_key).toString();
    const encryptedLogin = CryptoJS.AES.encrypt(login, private_key).toString();

    // Заменяем поле пароля зашифрованным значением
    document.getElementById('password').value = encryptedPassword;
    document.getElementById('login').value = encryptedPassword;
    console.log(encryptedPassword);
    console.log(encryptedLogin);
    // Теперь отправим форму
    this.submit();
});
