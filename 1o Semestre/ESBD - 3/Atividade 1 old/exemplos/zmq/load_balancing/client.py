# from pprint import pprint

import random

import zmq


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    socket.connect("tcp://0.0.0.0:5555")

    socket.send_json({"timer": random.randint(1, 5)})
    _ = socket.recv()


if __name__ == "__main__":
    main()
