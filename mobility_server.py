from concurrent import futures
import logging
import math
import time

import grpc
import mobility_pb2
import mobility_pb2_grpc
import mobility_resources

def get_vehicle(data_list, tgt):
    for data in data_list:
        if data['id'] == tgt.id:
            tgt_long = data['position'][-1]['longitude']
            tgt_lat = data['position'][-1]['latitude']
            return mobility_pb2.Position(longitude=tgt_long, latitude=tgt_lat)
    return None

def get_distance(pt_1, pt_2):
    long_1 = pt_1.longitude
    long_2 = pt_2.longitude
    lat_1 = pt_1.latitude
    lat_2 = pt_2.latitude
    delta_lat = lat_1 - lat_2
    delta_long = long_1 - long_2
    sqr_sum = pow(delta_lat, 2) + pow(delta_long, 2)
    return math.sqrt(sqr_sum)

def put_vehicle(data_list, vehicle):
    recived_time = time.time()
    for data in data_list:
        if data['id'] == vehicle.id.id:
            data['position'].append({'longitude':vehicle.pos.longitude, 'latitude':vehicle.pos.latitude, 'time':recived_time})
            result = "Vehicle id " + str(vehicle.id.id) + " position is update to " + str(vehicle.pos.longitude) + ", " + str(vehicle.pos.latitude)
            return result
    data = {'id':vehicle.id.id, 'position':[{'longitude':vehicle.pos.longitude, 'latitude':vehicle.pos.latitude, 'time':recived_time}]}
    result = "New vehicle id " + str(vehicle.id.id) + " is added to server"
    data_list.append(data)
    return result


class MobilityServicer(mobility_pb2_grpc.MobilityServicer):
    def __init__(self):
        self.data_list = mobility_resources.read_data()

    def Put(self, request, context):
        put_result = put_vehicle(self.data_list, request)
        return mobility_pb2.PutResponse(response=put_result)

    def Get(self, request, context):
        position = get_vehicle(self.data_list, request)
        if position is None:
            return mobility_pb2.Position(longitude=-1, latitude=-1)
        else:
            return position
    
    def Search(self, request, context):
        for data in self.data_list:
            position = mobility_pb2.Position(longitude=data['position'][-1]['longitude'], latitude=data['position'][-1]['latitude'])
            dist = get_distance(position, request.pos)
            if dist <= request.radius:
                yield mobility_pb2.Vehicle(id=mobility_pb2.Identifier(id=data['id']), pos=position)
    
    def History(self, request, context):
        for data in self.data_list:
            if data['id'] == request.id.id:
                for position in data['position']:
                    if position['time'] >= request.start.time and position['time'] <= request.end.time:
                        yield mobility_pb2.Position(longitude=position['longitude'], latitude=position['latitude'])
                return
        return mobility_pb2.Position(longitude=-1, latitude=-1)
    


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mobility_pb2_grpc.add_MobilityServicer_to_server(MobilityServicer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
            