import requests


def test_ping():
    r = requests.get("http://localhost:8080/ping")
    assert r.status_code == 200
    assert r.headers["Content-Type"] == "application/json"
    assert r.json() == ""


def test_predictions():
    r = requests.post("http://localhost:8080/predictions", json={"x": 1, "y": 2})
    assert r.status_code == 200
    assert r.headers["Content-Type"] == "application/json"
    assert "prediction" in r.json().keys()
