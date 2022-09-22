from concurrent import futures
import logging
import math
import time

import grpc
import mobility_pb2
import mobility_pb2_grpc
import mobility_resources

def get_vehicle(id_db, position_db, tgt):
    i = 0
    for i_th_id in id_db:
        if i_th_id == tgt.id:
            tgt_long = position_db[i][-1][0]
            tgt_lat = positon_db[i][-1][1]
            return mobility_pb2.Position(longitude=tgt_long, latitude=tgt_lat)
        else:
            i = i + 1
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

def put_vehicle(id_db, position_db, vehicle):
    i = 0
    time = time.time()
    for tgt_id in id_db:
        if tgt_id == vehicle.id:
            postion = {vehicle.pos.longitude, vehicle.pos.latitude, time}
            position_db[i].append(position)
            return
        else:
            i = i + 1
    id_db.append(tgt_id)
    pos_list = []
    position = {vehicle.pos.longitude, vehicle.pos.latitude, time}
    pos_list.append(position)
    position_db.append(pos_list)


class MobilityServicer(mobility_pb2_grpc.MobilityServicer):
    def __init__(self):
        self.id_db = mobility_resources.read_id()
        self.position_db = mobility_resources.read_position_list()

    def Put(self, request, context):
        put_vehicle(self.id_db, self.position_db, request)
        return mobility_pb2.PutResponse(response="Put id=%s method success" % request.id)

    def Get(self, request, context):
        vehicle = get_vehicle(self.id_db, self.position_db, request)
        if vehicle is None:
            return mobility_pb2.Position(longitude=-1, latitude=-1)
        else:
            return vehicle
    
    def Search(self, request, context):
        i = 0
        for pos_list in self.position_db:
            position = mobility_pb2.Position(longitude=pos_list[-1][0], latitude=pos_list[-1][1])
            dist = get_distance(position, request.pos)
            if dist <= request.radius:
                yield mobility_pb2.Vehicle(id=self.position_db[i], pos=position)
            i = i+1
    
    def History(self, request, context):
        i = 0
        for tgt_id in self.id_db:
            if tgt_id == request.id:
                pos_list = self.position_db[i]
                for position in pos_list:
                    if position[2] >= request.start.time and position[2] <= request.end.time:
                        yield mobility_pb2.Position(longitude=position[0], latitude=position[1])
                return
            else:
                i=i+1
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
            