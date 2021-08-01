var btn = document.getElementById('reg-btn')
btn.onclick = function() {
    var nickInput = document.getElementById('nickname')
    var passwordInput = document.getElementById('password')
    var emailInput = document.getElementById('email')
    fetch('/signup',
        {
            method: 'POST',
            body: JSON.stringify({"nickname": nickInput.value, "email": emailInput.value, "password": passwordInput.value})})
}