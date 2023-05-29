import zmq

context = zmq.Context()

#pull the results
results_receiver = context.socket(zmq.PULL)
results_receiver.bind("tcp://0.0.0.0:8001")

result = results_receiver.recv_json()
lista = []
best_acc = 0

for x in range(result['nmb_hiperparams']):
    result = results_receiver.recv_json()
    if result['result']['test_acc']>best_acc:
        best_acc = result['result']['test_acc']
        best_hiper = result['result']
    print(result)
    lista.append(result['result'])

print("The best hiperparameters is", best_hiper, "with the best accuracy that is: ", best_acc)