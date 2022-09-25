import os


class Entity:
    def __init__(self, name: str):
        self.__name = name

    @classmethod
    def from_env(cls):
        return cls(os.getenv("ENTITY_NAME", "123"))

    @property
    def name(self):
        return self.__name

    @staticmethod
    def run():
        return "the entity is running"

    def speak(self):
        return self.name


class Person(Entity):
    def __init__(self, name: str):
        super().__init__(name)

    def speak(self):
        return f"hi, my name is {self.name}"


class Dog(Entity):
    def __init__(self, name: str):
        super().__init__(name)

    def speak(self):
        return "bark bark bark"


def foo(x: Entity):
    return x.name + " is the entity's name"
