# subscriber.py
import json
import time
from pprint import pprint

import redis
import zmq


def main():
    r = redis.Redis(host="localhost", port=6379, db=0)

    p = r.pubsub()
    p.subscribe("transactions")

    context = zmq.Context()
    socket = context.socket(zmq.PUSH)

    socket.bind("tcp://*:5555")

    while True:
        message = p.get_message()
        if message:
            print(message)
            if isinstance(message["data"], bytes):
                message = json.loads(message["data"])
                # _ = socket.recv_string()
                socket.send_string(json.dumps(message))
                print("MSG sent to worker")

        time.sleep(0.1)


if __name__ == "__main__":
    main()
