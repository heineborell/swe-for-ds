class Entity:
    def __init__(self, name: str):
        self.name = name


def foo(e: Entity):
    e.name = "steve"


e = Entity("bob")
foo(e)
print(e.name)
