import pickle


with open("clf.pickle", "rb") as f:
    model = pickle.load(f)


if __name__ == "__main__":
    y = model.predict([[1, 1, 1, 1]])
    print(y[0])
