from someproject import IrisData, Predictor

if __name__ == "__main__":

    predictor = Predictor(".")
    y = predictor.predict_one(
        IrisData(sepal_length=1.2, sepal_width=0.8, petal_length=2.4, petal_width=1.2)
    )
    print(y)

    x = [
        IrisData(sepal_length=1.2, sepal_width=0.8, petal_length=2.4, petal_width=1.2),
        IrisData(sepal_length=2.1, sepal_width=1.4, petal_length=1.0, petal_width=3.2),
    ]
    y_batch = predictor.predict_batch(x)
    print(y_batch)
