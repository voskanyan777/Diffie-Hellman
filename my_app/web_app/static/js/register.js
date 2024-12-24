document.getElementById("login-form").addEventListener('submit', function(event){
    event.preventDefault();

    const login = document.getElementById("login").value
    const password = document.getElementById("password").value;
    const password_confirm = document.getElementById("password_confirm").value;
    const private_key = localStorage.getItem("shared_private_key")

    if (password != password_confirm) {
        alert("Пароли не совпадают!");
    }

    if (password.length < 8){
        alert("Длина пароля должна быть не менее 8 символов")
    }

    else{

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
    }

});
