from __future__ import print_function

import logging
import random

import grpc
import mobility_pb2
import mobility_pb2_grpc
import mobility_resources


def mobility_get_vehicle_internal(stub, tgt):
    vehicle = stub.Get(tgt)
    if not feature.location