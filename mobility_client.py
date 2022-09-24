from __future__ import print_function

import logging
import random

import grpc
import mobility_pb2
import mobility_pb2_grpc
import mobility_resources


def mobility_get_vehicle_internal(stub, tgt):
    pos = stub.Get(tgt)
    if pos.longitude == -1:
        print("Found no vehicle id %s" % tgt.id)
    else:
        print("Vehicle id %s is in location, %.3f , %.3f"% (tgt.id, pos.longitude, pos.latitude))


def mobility_get_vehicle(stub):
    mobility_get_vehicle_internal(stub, mobility_pb2.Identifier(id=3))
    mobility_get_vehicle_internal(stub, mobility_pb2.Identifier(id=10))


def mobility_put_vehicle_internal(stub, tgt_vehicle):
    put_result = stub.Put(tgt_vehicle)
    print(put_result)


def mobility_put_vehicle(stub):
    mobility_put_vehicle_internal(stub, mobility_pb2.Vehicle(id=mobility_pb2.Identifier(id=3), pos=mobility_pb2.Position(longitude=10.2123, latitude=13.2424)))
    mobility_put_vehicle_internal(stub, mobility_pb2.Vehicle(id=mobility_pb2.Identifier(id=15), pos=mobility_pb2.Position(longitude=142, latitude=121)))


def mobility_search_vehicle(stub):
    results = stub.Search(mobility_pb2.SearchRequest(pos=mobility_pb2.Position(longitude=10, latitude=10), radius=5))
    for result in results:
        print("Vehicle which have id %s is in location, %.3f , %.3f"% (result.id.id, result.pos.longitude, result.pos.latitude))


def mobility_history_vehicle(stub):
    results = stub.History(mobility_pb2.HistoryRequest(id=mobility_pb2.Identifier(id=1), start=mobility_pb2.Time(time=123124124), end=mobility_pb2.Time(time=123124155)))
    for result in results:
        print("Vehicle is in location %.3f , %.3f"% (result.longitude, result.latitude))

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = mobility_pb2_grpc.MobilityStub(channel)
        print("----------Get----------")
        mobility_get_vehicle(stub)
        print("----------Put----------")
        mobility_put_vehicle(stub)
        print("----------Search----------")
        mobility_search_vehicle(stub)
        print("----------History----------")
        mobility_history_vehicle(stub)

if __name__ == '__main__':
    logging.basicConfig()
    run()
