document.getElementById("login-form").addEventListener('submit', function(event){
    event.preventDefault();

    const password = document.getElementById("password").value;
    const password_confirm = document.getElementById("password_confirm").value;

    if (password != password_confirm) {
        alert("Пароли не совпадают!");
    } else {
        event.target.submit();
    }
});
