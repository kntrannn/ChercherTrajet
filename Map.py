import json

class Map:
    """
    Represents a map with coordinates for visualization.
    """

    __slots__ = ["l_canvas", "h_canvas", "coordinates_dict", "sites"]

    def __init__(self, l_canvas, h_canvas):
        """
        Initializes the Map object.

        Args:
            l_canvas (int): Width of the canvas.
            h_canvas (int): Height of the canvas.
        """
        self.l_canvas = l_canvas
        self.h_canvas = h_canvas
        self.load_coordinates(l_canvas, h_canvas)
        # self.load_sites()

    def load_coordinates(self, l_canvas, h_canvas):
        """
        Loads coordinates from a JSON file and converts them to canvas coordinates.

        Args:
            l_canvas (int): Width of the canvas.
            h_canvas (int): Height of the canvas.
        """
        with open("Database/ExternalData/result.json", "r") as f:
            data = json.load(f)
            coordinates = {}
            for key, value in data.items():
                coordinates[key] = self.convert_whole_coordinates(value, l_canvas, h_canvas)

        self.coordinates_dict = coordinates

    def load_sites(self):
        """
        Loads site coordinates from a JSON file and converts them to canvas coordinates.
        """
        with open("Database/ExternalData/concac.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            sites = {}
            for key, value in data.items():
                # Remove sites that are not in any polygon
                x, y = self.xy_from_lat_long(value[1], value[0], self.l_canvas, self.h_canvas)
                if self.is_in_any_polygon((x, y), self.coordinates_dict):
                    sites[key] = (x, y)

            # Dump the filtered sites to a JSON file
            with open("Database/ExternalData/filtered_sites.json", "w", encoding="utf-8") as f:
                json.dump(sites, f, ensure_ascii=False, indent=4)
        self.sites = sites

    def is_in_any_polygon(self, point, coords_dict):
        """
        Check if a point is inside any polygon in the coordinates dictionary.

        Args:
            point (tuple): The point to check (x, y).
            coords_dict (dict): The coordinates dictionary.

        Returns:
            bool: True if the point is inside any polygon, False otherwise.
        """
        for v in coords_dict.values():
            depth = self.list_depth(v)
            if depth == 4:
                for ele in v:
                    for ele2 in ele:
                        if self.is_point_in_polygon(point, ele2):
                            return True
            elif depth == 3:
                for ele in v:
                    if self.is_point_in_polygon(point, ele):
                        return True
        return False

    def is_point_in_polygon(self, point, polygon):
        """
        Check if a point is inside a polygon using the ray-casting algorithm.

        Args:
            point (tuple): The point to check (x, y).
            polygon (list): The polygon vertices [(x1, y1), (x2, y2), ...].

        Returns:
            bool: True if the point is inside the polygon, False otherwise.
        """
        x, y = point
        n = len(polygon)
        inside = False

        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    def xy_from_lat_long(self, latitude, longitude, l_canvas, h_canvas):
        """
        Converts latitude and longitude to canvas coordinates.

        Args:
            latitude (float): Latitude.
            longitude (float): Longitude.
            l_canvas (int): Width of the canvas.
            h_canvas (int): Height of the canvas.

        Returns:
            tuple: Canvas coordinates (x, y).
        """
        x = (longitude + 180) * (l_canvas / 360)
        y = h_canvas - (latitude + 90) * (h_canvas / 180)
        return x, y

    def convert_whole_coordinates(self, coordinates, l_canvas, h_canvas):
        """
        Converts all coordinates in a data structure to canvas coordinates.

        Args:
            coordinates (list or dict): Coordinates data structure.
            l_canvas (int): Width of the canvas.
            h_canvas (int): Height of the canvas.

        Returns:
            list or dict: Converted coordinates.
        """
        if self.list_depth(coordinates) == 4: # Corresponds to multipolygon coordinates
            for ele in coordinates:
                for ele2 in ele:
                    for ele3 in ele2:
                        lng, lat = ele3
                        x, y = self.xy_from_lat_long(lat, lng, l_canvas, h_canvas)
                        ele3[0] = x
                        ele3[1] = y
        elif self.list_depth(coordinates) == 3: # Corresponds to polygon coordinates
            for ele in coordinates:
                for ele2 in ele:
                    lng, lat = ele2
                    x, y = self.xy_from_lat_long(lat, lng, l_canvas, h_canvas)
                    ele2[0] = x
                    ele2[1] = y

        return coordinates

    def list_depth(self, lst):
        """
        Determines the depth of a nested list.

        Args:
            lst (list): The nested list.

        Returns:
            int: The depth of the list.
        """
        if not isinstance(lst, list):
            return 0
        return 1 + max(self.list_depth(item) for item in lst)