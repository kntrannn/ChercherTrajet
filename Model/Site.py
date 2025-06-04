class Site:
    """
    Represents a site with an ID, name, description, and geographical coordinates.
    The coordinates are expected to be in the format (longitude, latitude) or (x, y).
    """

    __slots__ = ["id", "name", "description", "coordinates_map", "coordinates_canvas"]

    def __init__(self, id, name, description, coordinates_map, coordinates_canvas=None):
        self.id = id
        self.name = name
        self.description = description
        self.coordinates_map = coordinates_map
        self.coordinates_canvas = coordinates_canvas   # two sets of coordinates, one for real one for the program