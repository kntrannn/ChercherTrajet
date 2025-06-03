import heapq
import math

def euclidean(p1, p2):
    """
    Calculates the Euclidean distance between two points.
    Args:
        p1 (tuple): The first point (x1, y1).
        p2 (tuple): The second point (x2, y2).
    Returns:
        float: The Euclidean distance between the two points.
    """
    return math.dist(p1, p2)

def a_star_maximize_sites(start_site, goal_site, site_list, alpha=1.0, radius=5.0):
    """
    A* algorithm to find the path from start_site to goal_site while maximizing the number of sites visited within a given radius.
    Args:
        start_site (Site): The starting site.
        goal_site (Site): The goal site.
        site_list (list): A list of all available sites.
        alpha (float): Weighting factor to balance path length and number of sites visited.
        radius (float): Radius within which to consider neighboring sites.
    Returns:
        list: A path from start_site to goal_site that maximizes the number of sites visited.
    """
    visited = set()
    open_list = []
    
    # Chuyển site_list thành set để tra cứu nhanh
    sites_set = set(site_list)

    heapq.heappush(open_list, (0, start_site, [start_site], 0))  # (priority, current_site, path, g_cost)

    while open_list:
        priority, current_site, path, g_cost = heapq.heappop(open_list)

        if current_site == goal_site:
            return path

        visited.add(current_site)

        # Tìm các Site lân cận chưa thăm trong bán kính radius
        neighbors = [
            site for site in sites_set 
            if site not in visited and euclidean(current_site.coordinates_canvas, site.coordinates_canvas) <= radius
        ]

        for neighbor in neighbors:
            new_g = g_cost + euclidean(current_site.coordinates_canvas, neighbor.coordinates_canvas)
            h = euclidean(neighbor.coordinates_canvas, goal_site.coordinates_canvas)
            num_visited = len(path) + 1
            new_path = path + [neighbor]
            f = new_g + h - alpha * num_visited
            heapq.heappush(open_list, (f, neighbor, new_path, new_g))

    return None  # Không tìm thấy đường
