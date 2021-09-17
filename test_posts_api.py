from app.main import app
from app.config import database
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_all_posts():
    await database.connect()
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000') as ac:
        response = await ac.get("/posts")
    assert response.status_code == 200
    assert list(response.json().keys()) == ["total_count", "results"]
    await database.disconnect()


@pytest.mark.asyncio
async def test_get_one_post():
    await database.connect()
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000') as ac:
        response = await ac.get("/posts/7")
    assert response.status_code == 200
    assert list(response.json().keys()) == [
        'title', 'content', 'image', 'id', 'creation_date', 'nickname', 'user_id']
    await database.disconnect()


@pytest.mark.asyncio
async def test_error_get_one_post():
    await database.connect()
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000') as ac:
        response = await ac.get("/posts/999999")
    assert response.status_code == 404
    await database.disconnect()


@pytest.mark.asyncio
async def test_post_editing():
    await database.connect()
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000') as ac:
        auth_response = await ac.post('/auth', json={'email': 'e.v.schukin@yandex.ru', 'password': 'Egor2013!'})
        access_token = auth_response.cookies['access_token_cookie']
    async with AsyncClient(app=app, base_url='htpp://127.0.0.1:8000') as ac:
        response = await ac.put('posts/7', json={'title': 'Я устал', 'content': 'Я ухожу', 'image': None}, cookies={'access_token_cookie': access_token})
    assert response.status_code == 200
    assert response.json()['title'] == 'Я устал'
    assert response.json()['content'] == 'Я ухожу'
    await database.disconnect()


@pytest.mark.asyncio
async def test_incorrect_data_post_editing():
    await database.connect()
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000') as ac:
        auth_response = await ac.post('/auth', json={'email': 'e.v.schukin@yandex.ru', 'password': 'Egor2013!'})
        access_token = auth_response.cookies['access_token_cookie']
    async with AsyncClient(app=app, base_url='htpp://127.0.0.1:8000') as ac:
        response = await ac.put('posts/7', json={'no_title': 'Я устал'}, cookies={'access_token_cookie': access_token})
    assert response.status_code == 422
    await database.disconnect()



@pytest.mark.asyncio
async def test_post_adding():
    await database.connect()
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000') as ac:
        auth_response = await ac.post('/auth', json={'email': 'e.v.schukin@yandex.ru', 'password': 'Egor2013!'})
        access_token = auth_response.cookies['access_token_cookie']
    async with AsyncClient(app=app, base_url='htpp://127.0.0.1:8000') as ac:
        response = await ac.post('posts', json={'title': 'Я устал 2.0', 'content': 'Теперь я мухожук!', 'image': None}, cookies={'access_token_cookie': access_token})
    assert response.status_code == 201
    assert response.json()['title'] == 'Я устал 2.0'
    await database.disconnect()


@pytest.mark.asyncio
async def test_invalid_post_adding():
    await database.connect()
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000') as ac:
        auth_response = await ac.post('/auth', json={'email': 'e.v.schukin@yandex.ru', 'password': 'Egor2013!'})
        access_token = auth_response.cookies['access_token_cookie']
    async with AsyncClient(app=app, base_url='htpp://127.0.0.1:8000') as ac:
        response = await ac.post('posts', json={'no_title': 'Я устал 2.0', 'r_content': 'Теперь я мухожук!', 'an_image': None}, cookies={'access_token_cookie': access_token})
    assert response.status_code == 422
    await database.disconnect()


@pytest.mark.asyncio
async def test_post_deleting():
    await database.connect()
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000') as ac:
        auth_response = await ac.post('/auth', json={'email': 'e.v.schukin@yandex.ru', 'password': 'Egor2013!'})
        access_token = auth_response.cookies['access_token_cookie']
    async with AsyncClient(app=app, base_url='htpp://127.0.0.1:8000') as ac:
        response = await ac.delete('posts/12', cookies={'access_token_cookie': access_token})
    assert response.status_code == 200
    await database.disconnect()


@pytest.mark.asyncio
async def test_ivalid_post_deleting():
    await database.connect()
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000') as ac:
        auth_response = await ac.post('/auth', json={'email': 'e.v.schukin@yandex.ru', 'password': 'Egor2013!'})
        access_token = auth_response.cookies['access_token_cookie']
    async with AsyncClient(app=app, base_url='htpp://127.0.0.1:8000') as ac:
        response = await ac.delete('posts/999', cookies={'access_token_cookie': access_token})
    assert response.status_code == 404
    await database.disconnect()