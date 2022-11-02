import os

from fastapi import FastAPI

from someproject import IrisData, Prediction, Predictor

app = FastAPI(title="iris_fastapi")
predictor = Predictor(os.environ.get("IRIS_PICKLE_DIR", "."))


@app.get("/ping")
def ping():
    return ""


@app.get("/predictions", response_model=Prediction)
def predictions_get(
    sepal_length: float, sepal_width: float, petal_length: float, petal_width: float
) -> Prediction:
    iris_data = IrisData(
        sepal_length=sepal_length,
        sepal_width=sepal_width,
        petal_length=petal_length,
        petal_width=petal_width,
    )

    return predictor.predict_one(iris_data)


@app.post("/predictions", response_model=Prediction)
def predictions_post(iris_data: IrisData) -> Prediction:
    return predictor.predict_one(iris_data)
