class Commune:
    __slots__ = ["id", "name", "description", "coordinates"]

    def __init__(self, id, name, description, coordinates):
        self.id = id
        self.name = name
        self.description = description
        self.coordinates = coordinates

    def __str__(self):
        return f"{self.name}, {self.description}, {self.coordinates}\n"