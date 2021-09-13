fetch('/users/me')
.then(function(response){
    if (response.status === 200) {
        fetch('/posts/me')
            .then((response) => { return response.json() })
                .then(function(data) { 
                    console.log(data)
                })
    } else {
        localStorage.setItem('redirectTo', '/my_posts/')
        document.location.href = '/unauthorized'
    }
})