import json
from Model.Trip import Trip
from Repository.SiteRepository import get_site_by_id

def get_all_trips_by_user_id(user_id):
    """
    Retrieves all trips for a given user ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        list: A list of Trip objects.
    """
    trips = []
    with open("Database/Entity/trips.json", "r") as file:
        data = json.load(file)
        for i in data:
            if i["user_id"] == user_id:
                start_site = get_site_by_id(i["start_site_id"])
                end_site = get_site_by_id(i["end_site_id"])
                sites_visited = [get_site_by_id(site_name) for site_name in i["sites_visited"]]
                trip = Trip(
                    user_id=i["user_id"],
                    start_site=start_site,
                    end_site=end_site,
                    vehicle=i["vehicle"],
                    distance=i["distance"],
                    carbon_footprint=i["carbon_footprint"],
                    sites_visited=sites_visited
                )
                trips.append(trip)
    return trips

def add_trip(trip):
    with open("Database/Entity/trips.json", "r") as file:
        trips = json.load(file)
        new_trip = {
            "user_id": trip.user_id,
            "start_site_id": trip.start_site.id,
            "end_site_id": trip.end_site.id,
            "vehicle": trip.vehicle,
            "distance": trip.distance,
            "carbon_footprint": trip.carbon_footprint,
            "sites_visited": [site.id for site in trip.sites_visited],
        }
        trips.append(new_trip)
    with open("Database/Entity/trips.json", "w") as file:
        json.dump(trips, file, indent=4)
    return True