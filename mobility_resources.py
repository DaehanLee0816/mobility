import json
import mobility_pb2

def read_id():
    id_list = []
    with open("mobility_data.json", "r") as mobility_data_file:
        for item in json.load(mobility_data_file):
            item_id = item["id"]
            id_list.append(item_id)
    return id_list


def read_position_list():
    position_list = []
    with open("mobility_data.json", "r") as mobility_data_file:
        for item in json.load(mobility_data_file):
            item_position_list = item["position"]
            obj_position_list = []
            for position in item_position_list:
                longitude = position["longitude"]
                latitude = position["latitude"]
                time = position["time"]
                elem = {longitude, latitude, time}
                obj_position_list.append(elem)
            position_list.append(obj_position_list)
    return position_list