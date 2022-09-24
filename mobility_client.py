from __future__ import print_function

import logging

import grpc
import mobility_pb2
import mobility_pb2_grpc


def get(stub, id):
    tgt_id = mobility_pb2.Identifier(id=id)
    pos = stub.Get(tgt_id)
    if pos.longitude == -1:
        print("Found no vehicle id %s" % id)
        return None
    else:
        print("Vehicle id %s is in location, %.3f , %.3f"% (tgt_id.id, pos.longitude, pos.latitude))
        return [pos.longitude, pos.latitude]


def put(stub, id, long, lat):
    vehicle = mobility_pb2.Vehicle(id=mobility_pb2.Identifier(id=id), pos=mobility_pb2.Position(longitude=long, latitude=lat))
    put_result = stub.Put(vehicle)
    print(put_result)


def search(stub, long, lat, dist):
    results = stub.Search(mobility_pb2.SearchRequest(pos=mobility_pb2.Position(longitude=long, latitude=lat), radius=dist))
    for result in results:
        print("Vehicle which have id %s is in location, %.3f , %.3f"% (result.id.id, result.pos.longitude, result.pos.latitude))
    return results


def history(stub, id, start_time, end_time):
    req = mobility_pb2.HistoryRequest(id=mobility_pb2.Identifier(id=id), start=mobility_pb2.Time(time=start_time), end=mobility_pb2.Time(time=end_time))
    results = stub.History(req)
    for result in results:
        print("Vehicle is in location %.3f , %.3f"% (result.longitude, result.latitude))
    return results

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = mobility_pb2_grpc.MobilityStub(channel)
        print("----------Get----------")
        get(stub, 1)
        get(stub, 10)
        print("----------Put----------")
        put(stub, 3, 10.2123, 13.2424)
        put(stub, 5, 142, 121)
        put(stub, 5, 145, 118)
        print("----------Search----------")
        search(stub, 10, 10, 5)
        print("----------History----------")
        history(stub, 1, 1664031111.9978276, 1664031113.9978276)

if __name__ == '__main__':
    logging.basicConfig()
    run()
