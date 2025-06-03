class Map:
    """
    Represents a map with coordinates for visualization.
    """

    __slots__ = ["l_canvas", "h_canvas"]

    def __init__(self, l_canvas, h_canvas):
        self.l_canvas = l_canvas
        self.h_canvas = h_canvas