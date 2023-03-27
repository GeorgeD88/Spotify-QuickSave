import json
import os


# === JSON Operations ===
def read_from_json(filename: str) -> dict:
    """ Reads and returns the data stored in the given JSON file (without file extension). """
    # raise FileNotFoundError if file to read from does not exist
    if not os.path.isfile(filename + '.json'):
        raise FileNotFoundError(f'{filename}.json does not exist.')

    with open(filename + '.json', 'r') as json_infile:
        data = json.load(json_infile)

    return data

def write_to_json(data: dict, filename: str, indent: int = 4):
    """ Writes the given data to the given JSON file (without file extension). """
    with open(filename + '.json', 'w+') as json_outfile:
        json.dump(data, json_outfile, indent=indent)

def format_to_json(data: dict, indent: int = 4) -> str:
    """ Returns the given data as a JSON formatted string. """
    return json.dumps(data, indent=indent)


# === String Manipulation ===
def spotify_id_from_link(spotify_link: str) -> str:
    """ Extracts and returns the Spotify ID from the given Spotify link. """
    return spotify_link.split('/')[-1].split('?')[0]
