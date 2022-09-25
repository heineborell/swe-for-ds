class Dataset:
    def __init__(self, x: int):
        self.data = x

    def increment(self):
        self.data += 1

    def double(self):
        self.data = self.data * 2


if __name__ == "__main__":

    dataset = Dataset(1)
    dataset.increment()
    dataset.double()
    print(dataset.data)
