from Repository.TripRepository import add_trip
from Model.Trip import Trip
from Utility.AStar import a_star_maximize_sites

def add_new_trip(user_id, start_site, end_site, vehicle, sites):
    """
    Adds a new trip for the user with the specified start and end sites, vehicle, and list of sites.
    Args:
        user_id (int): The ID of the user.
        start_site (str): The name of the starting site.
        end_site (str): The name of the ending site.
        vehicle (str): The type of vehicle used for the trip.
        sites (list): A list of Site objects.
    Returns:
        tuple: A tuple containing a boolean indicating success or failure, and a message.
    Raises:
        ValueError: If any of the input fields are empty or if the start and end sites are the same.
    """
    if start_site == "" or end_site == "" or vehicle == "":
        return False, "Please type all fields"
    
    if start_site == end_site:
        return False, "Departure and destination countries must be different"

    start_site_obj = get_site_by_name(start_site, sites)
    end_site_obj = get_site_by_name(end_site, sites)
    path = a_star_maximize_sites(start_site_obj, end_site_obj, sites, alpha=5.0, radius=1.0)
    if not path:
        return False, "No valid path found between the selected sites"

    trip = Trip(user_id, start_site_obj, end_site_obj, vehicle, sites_visited=path)
    trip.calculate_distance()
    trip.calculate_carbon_footprint()

    return add_trip(trip), "Trip added successfully"

def get_site_by_name(name, sites):
    """
    Retrieves a site by its name from the list of sites.
    
    Args:
        name (str): The name of the site.
        sites (list): A list of Site objects.
        
    Returns:
        Site: The Site object with the specified name, or None if not found.
    """
    for site in sites:
        if site.name == name:
            return site
    return None

def get_list_sites_names(sites):
    """
    Retrieves a list of site names from the list of Site objects.
    
    Args:
        sites (list): A list of Site objects.
        
    Returns:
        list: A list of site names.
    """
    return [site.name for site in sites]