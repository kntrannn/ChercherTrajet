import csv
import json

def load_csv_to_database(csv_file, db_file):
    """
    Reads a CSV file containing site data and converts it to a JSON format.
    The CSV file is expected to have a specific structure with columns for site name,
    description, and coordinates (longitude and latitude).
    The output JSON file will contain a list of sites, each with an ID, name, description,
    and coordinates.
    Args:
        csv_file (str): Path to the input CSV file.
        db_file (str): Path to the output JSON file.
    Returns:
        None
    """
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header line
        sites = []
        for i, row in enumerate(reader):
            if len(row) >= 2:  # Ensure there are at least two columns
                site = {
                    "id": i + 1,  # Start IDs from 1
                    "name": row[0].strip(),
                    "description": row[13].strip(),
                    "coordinates": (float(row[3].strip()), float(row[2].strip())),  # (longitude, latitude)
                }
                sites.append(site)

    with open(db_file, 'w', encoding='utf-8') as file:
        json.dump(sites, file, indent=4)

def check_duplication(json_file):
    """
    Checks for duplicate site names in the JSON file and prints them.
    Args:
        json_file (str): Path to the JSON file containing site data.
    Returns:
        None
    """
    with open(json_file, mode='r', encoding='utf-8') as file:
        data = json.load(file)

        sites = {}
        for site in data:
            value = sites.get(site["name"], 0)
            sites[site["name"]] = value + 1

        for k, v in sites.items():
            if v > 1:
                print(k)

if __name__ == "__main__":
    load_csv_to_database("Database/ExternalData/datatourisme-reg-ara.csv", "Database/Entity/sites.json")
    check_duplication("Database/Entity/sites.json")