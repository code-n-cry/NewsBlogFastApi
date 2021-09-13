var email = ''
var nickname = ''
var theme_slider = document.getElementById('theme')
if (localStorage.getItem('checked') == true) {
    theme_slider.checked = true
}
$(document).ready(function(){
    $('.modal').modal();
  }); 
fetch('users/me').then(
    function(response) {
        if (response.status === 200) {
            return response.json()
        } else {
            localStorage.setItem('redirectTo', '/profile')
            document.location.href = '/unauthorized'
            return
        }
    }
).then(function(data) {
    nickname = data['nickname']
    document.getElementById('nickname').value = nickname
    email = data['email']
})
document.getElementById('change').onclick = function() {
    fetch('/users/me', {
        method: 'PUT',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify({ nickname: document.getElementById('new_nickname').value, password: document.getElementById('password').value })
    }).then(function(response){
        if (response.status === 200) {
            document.getElementById('nickname').value = document.getElementById('new_nickname').value
            $('.modal').modal('close')
        } else {
            document.getElementById('password_error').style.color = "red"
            document.getElementById('password_error').innerHTML = '<b>Неверный пароль!</b>'
        }
    })
}
theme_slider.onchange = function() {
    if (theme_slider.checked === true) {
        document.getElementById('main').classList.add('dark')
        localStorage.setItem('theme', 'dark');
    } else {
        document.getElementById('main').classList.remove('dark')
        localStorage.setItem('theme', 'light');
    }
}