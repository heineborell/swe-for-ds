class Dataset:
    def __init__(self, x: int):
        self.data = x


def increment(d: Dataset) -> Dataset:
    return Dataset(d.data + 1)


def double(d: Dataset) -> Dataset:
    return Dataset(d.data * 2)


if __name__ == "__main__":

    dataset = Dataset(1)
    incremented = increment(dataset)
    doubled = double(dataset)

    print(dataset.data)
    print(incremented.data)
    print(doubled.data)
