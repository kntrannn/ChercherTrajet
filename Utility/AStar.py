import heapq
import math

def euclidean(p1, p2):
    return math.dist(p1, p2)

def a_star_maximize_sites(start_site, goal_site, site_list, alpha=1.0, radius=5.0):
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
            if site not in visited and euclidean(current_site.coordinates, site.coordinates) <= radius
        ]

        for neighbor in neighbors:
            new_g = g_cost + euclidean(current_site.coordinates, neighbor.coordinates)
            h = euclidean(neighbor.coordinates, goal_site.coordinates)
            num_visited = len(path) + 1
            new_path = path + [neighbor]
            f = new_g + h - alpha * num_visited
            heapq.heappush(open_list, (f, neighbor, new_path, new_g))

    return None  # Không tìm thấy đường
