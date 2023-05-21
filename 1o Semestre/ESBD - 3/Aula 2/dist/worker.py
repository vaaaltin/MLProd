import json
from time import sleep

import zmq


def main():
    context = zmq.Context()
    print(context)
    socket = context.socket(zmq.PULL)

    socket.connect("tcp://0.0.0.0:5555")

    while True:
        # socket.send_string("RDY")
        msg = json.loads(socket.recv_string())
        print("Recieved", msg)
        sleep(msg["data"]["value"] / 50)


if __name__ == "__main__":
    main()