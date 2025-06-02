import json
from openai import OpenAI
client = OpenAI()

def generate_sites_database():
    with open("Database/ExternalData/filtered_sites.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        sites = []
        for i, ele in enumerate(data.keys()):
            dico = {
                "id": i + 1,
                "name": ele
            }
            sites.append(dico)
        
    sites.sort(key=lambda x: x["name"])

    # Update the id for each site
    for i, site in enumerate(sites):
        site["id"] = i + 1

    with open("Database/Entity/sites.json", "w", encoding="utf-8") as f:
        json.dump(sites, f, indent=4)

def generate_description(place):
    """
    Generates a brief description for a given country using the OpenAI API.
    
    Args:
        country (str): The name of the country to generate a description for.
        
    Returns:
        str: A description of the country suitable for tourists.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Generate a brief description of the following place in France. The description should be for tourists who are planning to visit the place."},
            {"role": "user", "content": place}
        ]
    )

    print(f"Generated description for {place}: {response.choices[0].message.content}")

    return response.choices[0].message.content

def update_descriptions():
    """
    Reads the country list from a JSON file, generates descriptions for each country,
    updates the list with the descriptions, and writes the updated data back to the JSON file.
    """
    with open("Database/Entity/sites.json", "r") as f:
        sites = json.load(f)
        for site in sites:
            site["description"] = generate_description(site["name"])

    with open("Database/Entity/countries.json", "w") as f:
        json.dump(sites, f, indent=4)

if __name__ == "__main__":
    # generate_sites_database()
    update_descriptions()