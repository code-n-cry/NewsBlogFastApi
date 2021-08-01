import requests

print(requests.post('http://127.0.0.1:8000/signup', json={"nickname": "A", "email": "e.v.schukin@yandex.ru", "password": "E050698Sc"}).json())
