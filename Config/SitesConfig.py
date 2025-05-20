from Map import Map

def is_in_any_polygon(point, coords_dict):
        """
        Check if a point is inside any polygon in the coordinates dictionary.

        Args:
            point (tuple): The point to check (x, y).
            coords_dict (dict): The coordinates dictionary.

        Returns:
            bool: True if the point is inside any polygon, False otherwise.
        """
        for v in coords_dict.values():
            depth = map.list_depth(v)
            if depth == 4:
                for ele in v:
                    for ele2 in ele:
                        if is_point_in_polygon(point, ele2):
                            return True
            elif depth == 3:
                for ele in v:
                    if is_point_in_polygon(point, ele):
                        return True
        return False

def is_point_in_polygon(point, polygon):
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

# Remove all the sites that are not in any polygon
def remove_sites_not_in_polygon(sites, coords_dict):
    """
    Remove sites that are not in any polygon in the coordinates dictionary.

    Args:
        sites (dict): The sites dictionary.
        coords_dict (dict): The coordinates dictionary.

    Returns:
        dict: The filtered sites dictionary.
    """
    filtered_sites = {}
    for k, v in sites.items():
        if is_in_any_polygon(v, coords_dict):
            filtered_sites[k] = v
    return filtered_sites

if __name__ == "__main__":
    map = Map(100, 100)
    filtered_sites = remove_sites_not_in_polygon(map.sites, map.coordinates_dict)
    print("Filtered Sites:", filtered_sites)

    # Dump the filtered sites to a JSON file
    import json
    with open("filtered_sites.json", "w") as f:
        json.dump(filtered_sites, f, indent=4)