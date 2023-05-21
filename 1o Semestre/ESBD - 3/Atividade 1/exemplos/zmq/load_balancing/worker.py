# from pprint import pprint

from time import sleep

import zmq


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    socket.connect("tcp://0.0.0.0:5556")
    print("worker ready")

    while True:
        socket.send(b"R")
        workload = socket.recv_json()
        print(workload)

        sleep(workload["timer"])

        print("Done! Slept for ", workload["timer"], " seconds")


if __name__ == "__main__":
    main()
