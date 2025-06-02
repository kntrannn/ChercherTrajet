import json
from openai import OpenAI
# client = OpenAI()

def generate_commune_database():
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

# def generate_description(place):
#     """
#     Generates a brief description for a given country using the OpenAI API.
    
#     Args:
#         country (str): The name of the country to generate a description for.
        
#     Returns:
#         str: A description of the country suitable for tourists.
#     """
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "Generate a brief description of the following place in France. The description should be for tourists who are planning to visit the place."},
#             {"role": "user", "content": place}
#         ]
#     )

#     return response.choices[0].message.content

# def update_descriptions():
#     """
#     Reads the country list from a JSON file, generates descriptions for each country,
#     updates the list with the descriptions, and writes the updated data back to the JSON file.
#     """
#     with open("Database/Entity/sites.json", "r") as f:
#         sites = json.load(f)
#         for site in sites:
#             site["description"] = generate_description(site["name"])

#     with open("Database/Entity/countries.json", "w") as f:
#         json.dump(sites, f, indent=4)

if __name__ == "__main__":
    generate_commune_database()
    # update_descriptions()