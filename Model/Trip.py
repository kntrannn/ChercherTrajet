from math import radians, sin, cos, sqrt, atan2

class Trip:
    """
    Represents a trip made by a user from a start site to an end site using a specific vehicle.
    The trip includes the distance traveled, carbon footprint, and sites visited during the trip.
    """

    __slots__ = ["user_id", "start_site", "end_site", "vehicle", "distance", "carbon_footprint", "sites_visited"]

    def __init__(self, user_id, start_site, end_site, vehicle, distance = None, carbon_footprint = None, sites_visited = None):
        self.user_id = user_id
        self.start_site = start_site
        self.end_site = end_site
        self.vehicle = vehicle
        self.distance = distance
        self.carbon_footprint = carbon_footprint
        self.sites_visited = sites_visited

    def calculate_distance(self):
        total_distance = 0.0
        for i in range(len(self.sites_visited) - 1):
            total_distance += self.haversine_distance(self.sites_visited[i].coordinates_map, self.sites_visited[i + 1].coordinates_map)
        self.distance = total_distance

    def haversine_distance(self, coord1, coord2): #chat GPT: a very scientific way to calculate distance
        """
        Calculates the Haversine distance between two points on the Earth specified by their latitude and longitude.
        Args:
            coord1 (tuple): The first point (latitude, longitude).
            coord2 (tuple): The second point (latitude, longitude).
        Returns:
            float: The distance between the two points in kilometers.
        """
        R = 6371.0 # Radius of the Earth in kilometers
        lon1, lat1 = radians(coord1[0]), radians(coord1[1])
        lon2, lat2 = radians(coord2[0]), radians(coord2[1])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c # distance in kilometers

    def calculate_carbon_footprint(self):
        """
        Calculates the carbon footprint of the trip based on the vehicle type and distance traveled.
        Args:
            vehicle (str): The type of vehicle used for the trip.
            distance (float): The distance traveled in kilometers.
        Returns:
            float: The carbon footprint of the trip in kilograms of CO2.
        """
        carbon_footprint = 0.0
        if self.vehicle == "Plane":
            carbon_footprint = self.distance * 0.255
        elif self.vehicle == "Car":
            carbon_footprint = self.distance * 0.192
        elif self.vehicle == "Bus":
            carbon_footprint = self.distance * 0.089
        elif self.vehicle == "Train":
            carbon_footprint = self.distance * 0.06

        self.carbon_footprint = carbon_footprint
