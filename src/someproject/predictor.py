"""module containing a predictor which makes predictions"""

import os
import pickle
from abc import ABC, abstractmethod

from humps.main import camelize
from pydantic import BaseModel


class IrisData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class Prediction(BaseModel):
    iris_class = 1

    class Config:
        alias_generator = camelize


class Model(ABC):
    @abstractmethod
    def predict(self, x: list[list[float]]) -> list[int]:
        pass


class Predictor:
    """make predictions from a model"""

    def __init__(self, path: str):
        """initialize class from path to artifact named clf.pickle

        The pickled model must have a predict method which accepts
        lists of lists of 4 floats

        """
        with open(os.path.join(path, "clf.pickle"), "rb") as f:
            self.__model = pickle.load(f)

    @property
    def model(self) -> Model:
        """the model used to make predictions"""
        return self.__model

    def predict_one(self, x: IrisData) -> Prediction:
        """take one set of IrisData and return one prediction

        Arguments:
            x (IrisData): the data to predict on

        Returns:
            Prediction with the iris_class

        """
        raw_prediction = self.model.predict(
            [[x.sepal_length, x.sepal_width, x.petal_length, x.petal_width]]
        )
        return Prediction(iris_class=raw_prediction)

    def predict_batch(self, x: list[IrisData]) -> list[Prediction]:
        """take lists of IrisData and make predictions

        Arguments:
            x (list[IrisData]): list of IrisData to predict on

        Returns:
            list of Predictions with iris_classes

        """
        raw_data = [
            [data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]
            for data in x
        ]
        raw_predictions = list(self.model.predict(raw_data))
        return [Prediction(iris_class=raw) for raw in raw_predictions]
