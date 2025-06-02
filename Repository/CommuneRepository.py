import json
from Model.Commune import Commune

def get_list_of_communes():
    """
    Retrieves a list of Country objects from the countries.json file.

    Returns:
        list: A list of Country objects.
    """
    with open("Database/Entity/communes.json", "r") as file:
        data = json.load(file)
        communes = []
        for commune_data in data:
            commune = Commune(commune_data["id"], commune_data["name"], commune_data["description"], commune_data["coordinates"])
            communes.append(commune)
        return communes