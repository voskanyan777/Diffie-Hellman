function getCookie(name) {
    let value = `; ${document.cookie}`;
    let parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}
const private_key = getCookie('private_key')

document.addEventListener('DOMContentLoaded', function (){
    const SHAREDPRIVATEKEY = localStorage.getItem("shared_private_key")
    console.log(`SHARED PRIVATE KEY ${SHAREDPRIVATEKEY}`)
})
document.getElementById('login-form').addEventListener('submit', function (event) {
    // Останавливаем отправку формы, чтобы выполнить шифрование
    event.preventDefault();

    const private_key = localStorage.getItem("shared_private_key")

    // Получаем значения логина и пароля
    const login = document.getElementById('login').value;
    const password = document.getElementById('password').value;

    // Используем CryptoJS для шифрования пароля
    const encryptedPassword = CryptoJS.AES.encrypt(password, private_key).toString();
    const encryptedLogin = CryptoJS.AES.encrypt(login, private_key).toString();

    // Заменяем поле пароля зашифрованным значением
    document.getElementById('password').value = encryptedPassword;
    document.getElementById('login').value = encryptedLogin;
    console.log(`Зашифрованный логин: ${encryptedLogin}`);
    console.log(`Зашифрованный пароль: ${encryptedPassword}`);
    // Теперь отправим форму
    this.submit();
});
