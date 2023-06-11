import zmq
import time
import sys

port = '5556'
if len(sys.argv) > 1:
    port = sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://*:%s' % port)

while True:
    message = socket.recv()
    print('Receive Requests: %s' %message)
    
    time.sleep(1)
    
    socket.send(b"World")