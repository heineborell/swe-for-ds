class Entity:
    def __init__(self, name: str):
        self.name = name


def foo(e: Entity):
    e = Entity("steve")  # noqa


e = Entity("bob")
foo(e)
print(e.name)
