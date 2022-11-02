import json
import os

from flask import Flask, Response, request
from pydantic import ValidationError

from someproject import IrisData, Predictor

app = Flask("iris_flask")
predictor = Predictor(os.environ.get("IRIS_PICKLE_DIR", "."))


def get_validation_error_response(e: ValidationError) -> Response:
    """compares required and received, returning missing args"""
    error_data = {
        "event": "ValidationError",
        "error": str(e),
    }

    return Response(
        response=json.dumps(error_data),
        status=422,
        mimetype="application/json",
    )


def get_model_error_response(e: Exception) -> Response:
    """return 500 for other error"""
    error_data = {
        "event": "ModelError",
        "error": str(e),
    }

    return Response(
        response=json.dumps(error_data),
        status=500,
        mimetype="application/json",
    )


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
        return get_validation_error_response(e)

    try:
        prediction = predictor.predict_one(iris_data)
    except Exception as e:
        return get_model_error_response(e)

    return Response(
        response=prediction.json(),
        status=200,
        mimetype="application/json",
    )


@app.post("/predictions")
def predictions_post():

    try:
        iris_data = IrisData(**request.json)
    except ValidationError as e:
        return get_validation_error_response(e)

    try:
        prediction = predictor.predict_one(iris_data)
    except Exception as e:
        return get_model_error_response(e)

    return Response(
        response=prediction.json(),
        status=200,
        mimetype="application/json",
    )
