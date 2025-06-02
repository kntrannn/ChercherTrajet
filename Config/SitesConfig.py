# Read data from csv file and convert to JSON format (element of index 0 is the key, element of index 1 is the value)

import csv
import json

def load_csv_to_json(csv_file, json_file):
    """
    Reads a CSV file and converts it to a JSON format where the first column is the key and the second and third columns are the values.
    Skips the header line.

    Args:
        csv_file (str): Path to the input CSV file.
        json_file (str): Path to the output JSON file.
    """
    data = {}
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header line
        for row in reader:
            if len(row) >= 4:  # Ensure there are at least four columns
                key = row[0].strip()
                value = (float(row[3].strip()), float(row[2].strip())) # (longitude, latitude)
                data[key] = value

    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def load_csv_to_database(csv_file, db_file):
    """
    Reads a CSV file and converts it to a JSON format where the first column is the key and the second column is the value.
    Skips the header line.

    Args:
        csv_file (str): Path to the input CSV file.
        db_file (str): Path to the output database file.
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
    # load_csv_to_json("Database/ExternalData/datatourisme-reg-ara.csv", "Database/ExternalData/sites_touristiques.json")
    # load_csv_to_database("Database/ExternalData/datatourisme-reg-ara.csv", "Database/Entity/sites.json")
    check_duplication("Database/Entity/sites.json")