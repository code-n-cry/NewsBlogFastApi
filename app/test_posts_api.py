from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_all_posts():
    response = client.get('/posts')
    assert response.json()['results'] is not None