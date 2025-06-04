class Commune:
    """
    Represents a Commune with its ID, name, description, and coordinates.
    The coordinates are expected to be in the format (longitude, latitude) or (x, y).
    """

    __slots__ = ["id", "name", "description", "coordinates_map", "coordinates_canvas"]

    def __init__(self, id, name, description, coordinates_map, coordinates_canvas=None):
        self.id = id
        self.name = name
        self.description = description
        self.coordinates_map = coordinates_map  # a list of coordinates that represente the border of a region
        self.coordinates_canvas = coordinates_canvas