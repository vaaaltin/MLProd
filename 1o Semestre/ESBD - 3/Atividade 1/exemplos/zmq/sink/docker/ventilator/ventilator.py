import random
import time

import zmq


def produce():
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.bind("tcp://*:5555")

    count = 0
    while True:
        count += 1
        num = random.randint(0, 999)
        workload = {"num": num}
        print(count, workload)

        zmq_socket.send_json(workload)

        time.sleep(0.5)


if __name__ == "__main__":
    produce()
