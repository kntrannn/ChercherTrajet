import json
from Model.Commune import Commune

def get_list_of_communes():
    """
    Reads a JSON file containing commune data and returns a list of Commune objects.
    The JSON file is expected to have a specific structure with properties for each commune,
    including its ID, name, description, and coordinates.
    Returns:
        list: A list of Commune objects.
    """
    with open("Database/Entity/communes.json", "r") as file:
        data = json.load(file)
        communes = []
        for commune_data in data:
            commune = Commune(commune_data["id"], commune_data["name"], commune_data["description"], commune_data["coordinates"])
            communes.append(commune)
        return communes