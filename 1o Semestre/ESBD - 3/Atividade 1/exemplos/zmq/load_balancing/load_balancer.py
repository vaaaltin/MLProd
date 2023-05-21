"""
Workers precisam ser criados manualmente

https://zguide.zeromq.org/docs/chapter3/#The-Load-Balancing-Pattern
"""

from multiprocessing import Process

import zmq
from worker import main as worker

WORKLOADS = []
PROCESSES = []


def spawn_worker():
    p = Process(target=worker)
    PROCESSES.append(p)
    p.start()


def kill_worker():
    p = PROCESSES.pop()
    p.terminate()
    p.join()


def main():
    context = zmq.Context()
    zmq_frontend = context.socket(zmq.REP)
    zmq_backend = context.socket(zmq.REP)

    zmq_frontend.bind("tcp://*:5555")
    zmq_backend.bind("tcp://*:5556")

    poller = zmq.Poller()
    poller.register(zmq_frontend, zmq.POLLIN)
    poller.register(zmq_backend, zmq.POLLIN)

    print("Load Balancer Ready")
    while True:
        socks = dict(poller.poll())

        if socks.get(zmq_frontend) == zmq.POLLIN:
            WORKLOADS.append(zmq_frontend.recv_json())

            # if WORKLOADS and not PROCESSES:  # criamos o primerio worker
            #     spawn_worker()

            # workloads_workers_ratio = len(WORKLOADS) / len(PROCESSES)
            # if workloads_workers_ratio > 5:
            #     spawn_worker()

            # else:
            #     if len(PROCESSES):
            #         kill_worker()

            zmq_frontend.send_json({"msg": "ACK"})

            print(f"{len(WORKLOADS)} workloads in queue.")
            print(f"{len(PROCESSES)} workers working.")

        if WORKLOADS:
            if socks.get(zmq_backend) == zmq.POLLIN:
                _ = zmq_backend.recv()
                print("sending workload")
                zmq_backend.send_json(WORKLOADS.pop())

                print(f"{len(WORKLOADS)} workloads in queue")


if __name__ == "__main__":
    main()
