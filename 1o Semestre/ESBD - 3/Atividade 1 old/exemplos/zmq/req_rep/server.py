"""
Este modelo REQ-REP é muito utilizado em arquiteturas mais complexas
experimentem trocar os modelos (quem é servidor e quem é cliente) para
melhor entender o funcionamento.
https://zguide.zeromq.org/docs/chapter3/#The-REQ-to-REP-Combination
"""


import zmq
import time

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    socket.bind("tcp://*:5555")

    while True:
        _ = socket.recv_string()
        time.sleep(3)
        socket.send_string("PONG!")
        print("Sent PONG!")


if __name__ == "__main__":
    main()
