import time
import zmq
import random

hiperparams_train = {
    "learning_rate" : [0.0001, 0.001, 0.01],
    "n_neurons": [32, 64, 128],
    "activation_fun": ['relu', 'tanh'],
    "n_epochs": [5, 10, 15, 20]
}


def producer():
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.bind("tcp://0.0.0.0:8000")

    sum = 0
    for x in hiperparams_train.items():
        sum += len(x[1])

    work_message = {'nmb_hiperparams': sum}
    zmq_socket.send_json(work_message)
    print(work_message)
    for keys, values in hiperparams_train.items():
        for valores in values:
            work_message = {keys:valores}
            zmq_socket.send_json(work_message)
            print(work_message)
            time.sleep(1)


producer()