import requests

from someproject import IrisData, Prediction


def test_ping():
    r = requests.get("http://localhost:8080/ping")
    assert r.status_code == 200
    assert r.headers["Content-Type"] == "application/json"
    assert r.json() == ""


def test_predictions():
    iris_data = IrisData(
        sepal_length=1.2, sepal_width=1.4, petal_length=1.5, petal_width=0.3
    )
    r = requests.post(
        "http://localhost:8080/predictions", json=iris_data.json(by_alias=True)
    )
    assert r.status_code == 200
    assert r.headers["Content-Type"] == "application/json"
    _ = Prediction(**r.json())
