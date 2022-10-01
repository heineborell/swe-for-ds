"""simulating some data processing"""
import random
import time


class DataStore:
    """a fake datastore connection"""

    def __init__(self, database: str):
        self.database = database

    def get_data(self, data_id: int):
        """pretend to get data

        Simulates I/O bounded connection
        """
        time.sleep(0.1)
        return random.randint(0, 10)


def compute_important_value(data: list[int]) -> list[int]:
    """compute bounded computation"""
    time.sleep(len(data) * 0.01)
    return [datum * 2 for datum in data]
