class Map:
    """
    Represents a map with coordinates for visualization.
    """

    __slots__ = ["l_canvas", "h_canvas"]

    def __init__(self, l_canvas, h_canvas):
        """
        Initializes the Map object.

        Args:
            l_canvas (int): Width of the canvas.
            h_canvas (int): Height of the canvas.
        """
        self.l_canvas = l_canvas
        self.h_canvas = h_canvas
        # self.load_coordinates(l_canvas, h_canvas)
        # self.load_sites()

    # def load_coordinates(self, l_canvas, h_canvas):
    #     """
    #     Loads coordinates from a JSON file and converts them to canvas coordinates.

    #     Args:
    #         l_canvas (int): Width of the canvas.
    #         h_canvas (int): Height of the canvas.
    #     """
    #     with open("Database/Entity/communes.json", "r", encoding="utf-8") as f:
    #         data = json.load(f)
    #         for commune in data:
    #             coordinates = commune["coordinates"]
    #             # Convert coordinates to canvas coordinates
    #             commune["coordinates"] = self.convert_whole_coordinates(coordinates, l_canvas, h_canvas)

    #     self.communes = data

    # def load_sites(self):
    #     """
    #     Loads site coordinates from a JSON file and converts them to canvas coordinates.
    #     """
    #     with open("Database/Entity/sites.json", "r", encoding="utf-8") as f:
    #         data = json.load(f)
    #         for site in data:
    #             x, y = self.xy_from_lat_long(site["coordinates"][1], site["coordinates"][0], self.l_canvas, self.h_canvas)
    #             site["coordinates"] = (x, y)
    #     self.sites = data