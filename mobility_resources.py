import json
import mobility_pb2

def read_data():
    data_list = []
    with open("mobility_data.json", "r") as mobility_data_file:
        for item in json.load(mobility_data_file):
            data_list.append(item)
    return data_list
