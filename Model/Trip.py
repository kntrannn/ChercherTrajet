from math import radians, sin, cos, sqrt, atan2

class Trip:
    __slots__ = ["user_id", "start_site", "end_site", "vehicle", "distance", "carbon_footprint", "sites_visited"]

    def __init__(self, user_id, start_site, end_site, vehicle, distance = None, carbon_footprint = None, sites_visited = None):
        self.user_id = user_id
        self.start_site = start_site
        self.end_site = end_site
        self.vehicle = vehicle
        if distance is None:
            self.distance = self.calculate_distance(start_site, end_site)
        else:
            self.distance = distance
        if carbon_footprint is None:
            self.carbon_footprint = self.calculate_carbon_footprint(vehicle, self.distance)
        else:
            self.carbon_footprint = carbon_footprint
        self.sites_visited = sites_visited

    def calculate_distance(self, start_site, end_site):
        long_start, lat_start = start_site.coordinates
        long_end, lat_end = end_site.coordinates
        R = 6371.0
        dlon = radians(long_end - long_start)
        dlat = radians(lat_end - lat_start)
        a = sin(dlat / 2)**2 + cos(radians(lat_start)) * cos(radians(lat_end)) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    def calculate_carbon_footprint(self, vehicle, distance):
        if vehicle == "Plane":
            return distance * 0.255
        elif vehicle == "Car":
            return distance * 0.192
        elif vehicle == "Bus":
            return distance * 0.089
        elif vehicle == "Train":
            return distance * 0.06
        elif vehicle == "Bicycle" or vehicle == "Walking":
            return 0