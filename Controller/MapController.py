from Repository.CommuneRepository import get_list_of_communes
from Repository.SiteRepository import get_list_of_sites
from Repository.TripRepository import get_all_trips_by_user_id
import math

def get_all_trips(user_id, sites):
    """
    Retrieves all trips for a given user.
    Args:
        user_id (int): The ID of the user.
        sites (list): A list of Site objects.
    Returns:
        list: A list of all trips for the user.
    """
    return get_all_trips_by_user_id(user_id, sites)

def get_all_communes_with_x_y(canvas_width, canvas_height):
    """
    Retrieves a list of all communes. (calculate all the canvas coordinates for communes)
    Args:
        canvas_width (int): Width of the canvas.
        canvas_height (int): Height of the canvas.
    Returns:
        list: A list of all communes.
    """
    communes = get_list_of_communes()
    for commune in communes:
        coordinates = commune.coordinates_map
        commune.coordinates_canvas = convert_whole_coordinates(coordinates, canvas_width, canvas_height)
    return communes

def get_all_filtered_sites_with_x_y(canvas_width, canvas_height, min_distance):
    """
    Retrieves a list of all sites with converted coordinates and filtered by minimum distance.
    Args:
        canvas_width (int): Width of the canvas.
        canvas_height (int): Height of the canvas.
        min_distance (float): Minimum distance between points.
    Returns:
        list: A list of all filtered sites with converted coordinates.
    """
    sites = get_list_of_sites()
    for site in sites:
        coordinates = site.coordinates_map
        site.coordinates_canvas = xy_from_lat_long(coordinates[1], coordinates[0], canvas_width, canvas_height)
    sites = filter_points(sites, min_distance)
    return sites

def get_centroid(communes, sites):
    """
    Calculates the centroid of all communes and sites.
    Args:
        communes (list): A list of Commune objects.
        sites (list): A list of Site objects.
    Returns:
        tuple: The centroid coordinates (x, y).
    """
    all_points_communes = []
    for commune in communes:
        v = commune.coordinates_canvas
        depth = list_depth(v)
        if depth == 4:
            for ele in v:
                for ele2 in ele:
                    all_points_communes.extend(ele2)
        elif depth == 3:
            for ele in v:
                all_points_communes.extend(ele)

    # Collect all region coordinates efficiently
    xs_regions, ys_regions = zip(*all_points_communes)
    sum_x = sum(xs_regions)
    sum_y = sum(ys_regions)

    # Collect all site coordinates efficiently
    all_points_sites = [site.coordinates_canvas for site in sites]
    xs_sites, ys_sites = zip(*all_points_sites)
    sum_x += sum(xs_sites)
    sum_y += sum(ys_sites)

    total_points = len(all_points_communes) + len(all_points_sites)
    return sum_x / total_points + 4, sum_y / total_points

def xy_from_lat_long(latitude, longitude, l_canvas, h_canvas):
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

def convert_whole_coordinates(coordinates, l_canvas, h_canvas):
    """
    Converts all coordinates in a data structure to canvas coordinates.

    Args:
        coordinates (list or dict): Coordinates data structure.
        l_canvas (int): Width of the canvas.
        h_canvas (int): Height of the canvas.

    Returns:
        list or dict: Converted coordinates.
    """
    if list_depth(coordinates) == 4: # Corresponds to multipolygon coordinates
        for ele in coordinates:
            for ele2 in ele:
                for ele3 in ele2:
                    lng, lat = ele3
                    x, y = xy_from_lat_long(lat, lng, l_canvas, h_canvas)
                    ele3[0] = x
                    ele3[1] = y
    elif list_depth(coordinates) == 3: # Corresponds to polygon coordinates
        for ele in coordinates:
            for ele2 in ele:
                lng, lat = ele2
                x, y = xy_from_lat_long(lat, lng, l_canvas, h_canvas)
                ele2[0] = x
                ele2[1] = y

    return coordinates

def list_depth(lst):
    """
    Determines the depth of a nested list.  # proposed by AI

    Args:
        lst (list): The nested list.

    Returns:
        int: The depth of the list.
    """
    if not isinstance(lst, list):
        return 0            # condition initiale
    return 1 + max(list_depth(item) for item in lst)  # very classique recurrence fonction 

def distance(p1, p2):
    """
    Calculates the Euclidean distance between two points.
    Args:
        p1 (tuple): The first point (x1, y1).
        p2 (tuple): The second point (x2, y2).
    Returns:
        float: The Euclidean distance between the two points.
    """
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])  # norme euclidienne: hypotenuse

def filter_points(points, min_distance):
    """
    Filters a list of points to ensure that each point is at least a minimum distance from all previously kept points.
    Args:
        points (list): A list of points, where each point has a 'coordinates' attribute.
        min_distance (float): The minimum distance between points.

    Returns:
        list: A filtered list of points that are at least `min_distance` apart.
    """
    kept_points = []
    for site in points:
        p = site.coordinates_canvas
        if all(distance(p, kp.coordinates_canvas) >= min_distance for kp in kept_points): # all([]) est true par convention
            kept_points.append(site)                               # a simple way to write conjunction proposed by AI
                                                                # distance is function write before
    return kept_points