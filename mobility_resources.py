import json

def read_data():
    with open("mobility_data.json", "r") as mobility_data_file:
        data = json.load(mobility_data_file)
    return data

def write_data(data_list):
    with open("mobility_data.json", "w", encoding='utf-8') as mobility_data_file:
        json.dump(data_list, mobility_data_file, indent=4)
