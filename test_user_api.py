from app.main import app
from app.config import database
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_invalid_password_signup():
    await database.connect()
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000') as ac:
        response = await ac.post("/signup", json=({'nickname': 'zeumb', 'email': 'egor.schuin@yandex.ru','password': 'qw23'}))
    assert response.status_code == 400
    assert response.json()['detail'] == "Incorrect password!"
    await database.disconnect()


@pytest.mark.asyncio
async def test_invalid_email_signup():
    await database.connect()
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000') as ac:
        response = await ac.post("/signup", json=({'nickname': 'zeumb', 'email': 'egor.schuin@yandex.ru','password': 'qwert123'}))
    assert response.status_code == 400
    assert response.json()['detail'] == "Email already exists!"
    await database.disconnect()


@pytest.mark.asyncio
async def test_correct_signup():
    await database.connect()
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000') as ac:
        response = await ac.post("/signup", json=({'nickname': 'zeumb', 'email': 'YOUR_UNIQUE_EMAIL@DOMAIN.COM','password': 'SUPER_PASSWORD'}))
    assert response.status_code == 400
    assert response.json()['detail'] == "Email already exists!"
    await database.disconnect()


@pytest.mark.asyncio
async def test_invalid_auth():
    await database.connect()
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000') as ac:
        response = await ac.post("/signup", json=({'nickname': 'zeumb', 'email': 'egor.schuin@yandex.ru','password': 'qwer123'}))
    assert response.status_code == 401
    assert response.json()['detail'] == "Incorrect username or password"
    await database.disconnect()


@pytest.mark.asyncio
async def test_correct__auth():
    await database.connect()
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000') as ac:
        response = await ac.post("/signup", json=({'nickname': 'zeumb', 'email': 'egor.schuin@yandex.ru','password': 'qwert123'}))
    assert response.status_code == 200
    assert response.json()['msg'] == "Succesfully login"
    await database.disconnect()