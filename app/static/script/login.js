var btn = document.getElementById("login-btn")
var error_span = document.getElementById("pass-errors")
btn.onclick = function() {
    var email_input = document.getElementById('email').value
    var password_input = document.getElementById('password').value
    fetch("/auth", {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify({ email: email_input, password: password_input })
    }).then(function(response){
        if (response.status == 200) {
            if (localStorage.getItem('redirectTo') != null) {
                document.location.href = localStorage.getItem('redirectTo')
                localStorage.removeItem('redirectTo')
            } else {
                document.location.href = '/'
            }
        } else {
            error_span.innerHTML = `<b>Неверный email или пароль!</b>`
        }
    })
}