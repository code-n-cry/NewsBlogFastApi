if (localStorage.getItem("access_token") === null){
            document.getElementById("name").innerHTML = `<div class="row"><h3 align="center"><b>Вы не авторизованы!</b></h3>
            <div class="col s3 offset-s3"><a href="/register" class="waves-effect waves-dark btn reg"><i class="material-icons left">add_circle_outline</i>Регистрация</a></div>
            <div class="col s2"><a href="/auth" class="waves-effect waves-dark btn log"><i class="material-icons right">input</i>Вход</a></div></div>`
} else {
    document.getElementById("name").innerHTML = '<h3 align="center"><b>Ваши посты:</b></h3><br>'
}