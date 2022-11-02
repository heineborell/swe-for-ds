import json
import os

from flask import Flask, Response, request
from pydantic import ValidationError

from someproject import IrisData, Predictor

app = Flask("iris_flask")
predictor = Predictor(os.environ.get("IRIS_PICKLE_DIR", "."))


def validate_args(received: list[str], required: list[str]) -> list[str]:
    """compares required and received, returning missing args"""
    return [arg for arg in required if arg not in received]


@app.get("/predictions")
def predictions_get():

    try:
        iris_data = IrisData(
            sepal_length=request.args.get("sepal_length"),
            sepal_width=request.args.get("sepal_width"),
            petal_length=request.args.get("petal_length"),
            petal_width=request.args.get("petal_width"),
        )
    except ValidationError as e:
        error_data = {
            "event": "ValidationError",
            "error": str(e),
        }

        return Response(
            response=json.dumps(error_data),
            status=422,
            mimetype="application/json",
        )

    try:
        prediction = predictor.predict_one(iris_data)
    except Exception as e:
        error_data = {
            "event": "ModelError",
            "error": str(e),
        }

        return Response(
            response=json.dumps(error_data),
            status=500,
            mimetype="application/json",
        )

    return Response(
        response=prediction.json(),
        status=200,
        mimetype="application/json",
    )
