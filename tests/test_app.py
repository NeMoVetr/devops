from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "healthy"
    assert "timestamp" in data


def test_root_redirect():
    # проверим, что / редиректит на /docks с 307
    r = client.get("/", allow_redirects=False)
    assert r.status_code == 307
    assert r.headers.get("location") == "/docks"


def test_docks():
    r = client.get("/docks")
    assert r.status_code == 200
    data = r.json()
    assert "service" in data
    assert "timestamp" in data
    assert data["note"].startswith("Root")


def test_api_time():
    r = client.get("/api/time")
    assert r.status_code == 200
    payload = r.json()
    assert "timestamp" in payload
    assert payload.get("timezone") == "UTC"


def test_hello_valid():
    r = client.get("/api/hello/Alex")
    assert r.status_code == 200
    data = r.json()
    assert "Hello, Alex" in data.get("message", "")


def test_hello_invalid():
    # имя с цифрами — должно вернуть 400
    r = client.get("/api/hello/alex123")
    assert r.status_code == 400
