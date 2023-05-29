# from pprint import pprint

import zmq


def main():
    count = 0
    context = zmq.Context()
    socket = context.socket(zmq.PULL)

    socket.bind("tcp://0.0.0.0:5556")

    while True:
        result = socket.recv_json()
        count += 1

        # pprint(result)
        print(f"COUNT: {count}")


if __name__ == "__main__":
    main()
