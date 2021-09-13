var btn = document.getElementById('reg-btn')
btn.onclick = function() {
    var nickInput = document.getElementById('nickname')
    var emailInput = document.getElementById('email')
    var passwordInput = document.getElementById('password')
    var json_data = JSON.stringify({ nickname: nickInput.value, email: emailInput.value, password: passwordInput.value })
    fetch('/signup',
        {
            method: 'POST',
            body: json_data,
            headers: {
                'Content-Type': 'application/json'
              }})
        .then(function(response){
            if (response.status === 200) {
                fetch(`/auth`,
                {
                    method: "POST",
                    headers: {
                        'Content-type': 'application/json'
                    },
                    body: json_data
                }).then(function(response){
                    if (response.status == 200){
                        if (localStorage.getItem('redirectTo') != null) {
                            document.location.href = localStorage.getItem('redirectTo')
                            localStorage.removeItem('redirectTo')
                        } else {
                            document.location.href = '/'
                        }
                    }
                })
                } else {
                    return response.json()
                }
            }).then(function(data){
                if (Object.values(data)[0] === 'Email already exists!') {
                    document.getElementById("errors").innerHTML = `E-mail уже зарегистрирован! <a href='/login'>Войти?</a>`
                } else {
                    document.getElementById("errors").innerHTML = `Неверный пароль! В нём должны быть латинские символы с цифрами и знаками, а длина должна быть больше 5 символов!`
                }
            })
        }
