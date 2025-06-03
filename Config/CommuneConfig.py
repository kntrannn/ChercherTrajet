import json
from openai import OpenAI
client = OpenAI()

def load_json_to_database(): #chat GPT
    """
    Reads a GeoJSON file containing communes in Auvergne-Rhône-Alpes, France,
    extracts relevant information, and writes it to a JSON file in the database.
    The GeoJSON file is expected to have a specific structure with properties
    for each commune, including its name and coordinates.
    The output JSON file will contain a list of communes, each with an ID,
    name, description, and coordinates.
    """
    with open("Database/ExternalData/cantons-auvergne-rhone-alpes.geojson", "r") as f:
        data = json.load(f)
        communes = []
        for i, ele in enumerate(data["features"]):
            commune = {
                "id": i + 1,  # Start IDs from 1
                "name": ele["properties"]["nom"],
                "description": "",  # Placeholder for description
                "coordinates": ele["geometry"]["coordinates"]
            }
            communes.append(commune)

    with open("Database/Entity/communes.json", "w", encoding="utf-8") as f:
        json.dump(communes, f, indent=4)

def generate_description(place): #chat GPT
    """
    Generates a brief description of a given place using OpenAI's GPT-3.5 Turbo model.
    Args:
        place (str): The name of the place to describe.
    Returns:
        str: A brief description of the place.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Generate a brief description (in french) of the following town in Auvergne-rhone-alpes, France. The description should be for tourists who are planning to visit the place."},
            {"role": "user", "content": place}
        ]
    )

    return response.choices[0].message.content

def update_descriptions():
    """
    Reads the communes from a JSON file, generates descriptions for each commune using OpenAI's GPT-3.5 Turbo model,
    and writes the updated communes back to the JSON file.
    The descriptions are generated based on the name of each commune, and the output JSON file will contain
    the updated descriptions for each commune.
    Args:
        None
    Returns:
        None
    """
    with open("Database/Entity/communes.json", "r") as f:
        communes = json.load(f)
        for commune in communes:
            description = generate_description(commune["name"])
            print(f"Generated description for {commune['name']}: {description}")
            commune["description"] = description

    with open("Database/Entity/communes.json", "w") as f:
        json.dump(communes, f, indent=4)

if __name__ == "__main__":
    # load_json_to_database()
    update_descriptions()
