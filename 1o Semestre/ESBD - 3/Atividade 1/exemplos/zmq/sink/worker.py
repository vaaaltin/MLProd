import os
import time
from math import sqrt

import zmq


def task_pesada(num: int):
    time.sleep(2)
    return {"num": num, "sqrt": sqrt(num)}


def work():
    _id = str(os.getpid())
    print(f"WORKER: {_id}")

    context = zmq.Context()
    socket_rcv = context.socket(zmq.PULL)
    socket_rcv.connect("tcp://localhost:5555")

    socket_snd = context.socket(zmq.PUSH)
    socket_snd.connect("tcp://localhost:5556")

    while True:
        workload = socket_rcv.recv_json()

        result = task_pesada(workload["num"])
        print({"worker_id": _id, "result": result})
        socket_snd.send_json({"worker_id": _id, "result": result})


if __name__ == "__main__":
    print("starting worker...")
    work()
