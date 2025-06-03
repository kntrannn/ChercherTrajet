from Model.Site import Site
import json

def get_list_of_sites():
    """
    Retrieves a list of Site objects from the sites.json file.

    Returns:
        list: A list of Site objects.
    """
    with open("Database/Entity/sites.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        sites = []
        for site_data in data:
            site = Site(site_data["id"], site_data["name"], site_data["description"], site_data["coordinates"])
            sites.append(site)
        return sites