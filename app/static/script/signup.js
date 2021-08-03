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
            console.log(response.json())
            if (response.status === 200) {
                fetch(`/auth`,
                {
                    method: "POST",
                    headers: {
                        'Content-type': 'application/x-www-form-urlencoded'
                    },
                    body: `username=${ emailInput.value }&password=${ passwordInput.value }`
                })
                .then((response) => {return response.json()})
                .then(function(data) {
                    localStorage.setItem("access_token", Object.values(data)[0])
                        console.log(Object.values(data)[0])
                    })
                } else {
                    if (Object.values(JSON.parse(response.json())[0]) === "Incorrect password!") {
                        document.getElementById("error").innerHTML = `Пароль должен состоять из букв и цифр и включать в себя не менее 5 символов!`
                    } else {
                        document.getElementById("error").innerHTML = `Пользователь уже зарегистрирован!<div class="row"><a class="btn waves-effect waves-light col s2" href="/login">Войти</a>`
                    }
                }
            })
        }
