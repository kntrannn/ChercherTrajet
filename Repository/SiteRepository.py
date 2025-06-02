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

def get_site_by_name(name):
    """
    Retrieves a Site object by its name.

    Args:
        name (str): The name of the site.

    Returns:
        Site: The Site object with the specified name, or None if not found.
    """
    sites = get_list_of_sites()
    for site in sites:
        if site.name == name:
            return site
    return None

def get_site_by_id(site_id):
    """
    Retrieves a Site object by its ID.

    Args:
        site_id (int): The ID of the site.

    Returns:
        Site: The Site object with the specified ID, or None if not found.
    """
    sites = get_list_of_sites()
    for site in sites:
        if site.id == site_id:
            return site
    return None