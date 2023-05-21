"""
Este modelo REQ-REP é muito utilizado em arquiteturas mais complexas
experimentem trocar os modelos (quem é servidor e quem é cliente) para
melhor entender o funcionamento.
https://zguide.zeromq.org/docs/chapter3/#The-REQ-to-REP-Combination
"""

import zmq


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    socket.connect("tcp://0.0.0.0:5555")

    while True:
        _ = input("press [ENTER] to send")
        socket.send_string("PING!")
        print("Sent PING!")
        print("Recieved", socket.recv_string())


if __name__ == "__main__":
    main()
