$(document).ready(function(){
    $('.slider').slider({indicators: true});
  });
var is_slider_exist = false
var json_data = {}
json_data['images'] = []
fetch('users/me').then(function (response) {
    if (response.status != 200) {
        localStorage.setItem('redirectTo', '/create')
        document.location.href = '/unauthorized'
    }
})
var create_btn = document.getElementById('create-btn')
create_btn.onclick = function() {
    document.getElementById('title_e').innerHTML = ''
    document.getElementById('content_e').innerHTML = ''
    var news_title = document.getElementById('title').value
    var news_content = document.getElementById('content').value
    if (news_title.split(' ').length > 4) {
        document.getElementById('title_e').style.color = 'red'
        document.getElementById('title_e').innerHTML = '<b>В названии больше трёх слов!</b>'
        return
    } 
    if (news_content.length > 500) {
        document.getElementById('content_e').style.color = 'red'
        document.getElementById('content_e').innerHTML = '<b>В теле поста больше 1000 символов!</b>'
        return
    } 
    json_data['title'] = news_title
    json_data['content'] = news_content
    var json_post = JSON.stringify(json_data)
    fetch('/posts', {
        method: 'POST', 
        body: json_post,
        headers: {
            'Content-Type': 'Application/json'
        }
    }).then(function(response) {
        if (response.status == 201) {
            document.location.href = '/'
        }
    })   
}
const file_input = document.getElementById('file-input')
const carousel_div = document.getElementById('slides')
function addFilesToCarousel(files) {
    json_data['image'] = []
    document.getElementById('slides').innerHTML = ''
    if (is_slider_exist === false) {
        carousel_div.style.display = 'block'
    }
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        if (!file.type.startsWith('image/')){ continue }
        var new_carousel_el = document.createElement('li')
        var el_img = document.createElement("img");
        el_img.file = file;
        new_carousel_el.appendChild(el_img)
        carousel_div.appendChild(new_carousel_el);
        var reader = new FileReader();
        reader.onload = (function(aImg) { return function(e) {
            var tempFileData = e.target.result
            aImg.src = tempFileData
            json_data['image'].push({'filename': file.name, 'data': tempFileData.split(",")[1]})
        }; })(el_img);
        reader.readAsDataURL(file);
        $('.slider').removeClass('initialized');
        $('.slider').slider({indicators: true});
        document.addEventListener('DOMContentLoaded', function() {
            var elems = document.querySelectorAll('.slider');
            var options = {indicators: true}
            var instances = M.Slider.init(elems, options);
          });
    }
}