import json
from Model.Trip import Trip

def get_all_trips_by_user_id(user_id, sites):
    """
    Retrieves all trips for a given user ID from the trips.json file.
    Args:
        user_id (int): The ID of the user.
        sites (list): A list of Site objects.
    Returns:
        list: A list of Trip objects associated with the user.
    """
    trips = []
    with open("Database/Entity/trips.json", "r") as file:
        data = json.load(file)
        for i in data:
            if i["user_id"] == user_id:
                start_site = get_site_by_id(i["start_site_id"], sites)
                end_site = get_site_by_id(i["end_site_id"], sites)
                sites_visited = [get_site_by_id(site_name, sites) for site_name in i["sites_visited"]]
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

def get_site_by_id(site_id, sites):
    """
    Retrieves a site by its ID from a list of Site objects.
    Args:
        site_id (int): The ID of the site.
        sites (list): A list of Site objects.
    Returns:
        Site: The Site object with the specified ID, or None if not found.
    """
    for site in sites:
        if site.id == site_id:
            return site
    return None

def add_trip(trip):
    """
    Adds a new trip to the trips.json file.
    Args:
        trip (Trip): The Trip object to be added.
    Returns:
        bool: True if the trip was added successfully, False otherwise.
    """
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