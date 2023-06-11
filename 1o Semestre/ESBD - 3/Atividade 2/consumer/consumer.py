import time
import zmq
import random
import joblib
import pandas as pd

model = joblib.load("svm.joblib")

#verifica se é fraude, se for manda para o tópico se não for não faz nada
def heavyTask(msg):
    input_arr = pd.array(msg["vals"]).reshape(1, -1)
    fraud = model.predict(input_arr)

    if fraud:
        fraud = True
    else:
        fraud = False
    retorno = {"transactionId": msg["id"], "fraud": fraud}
    
    return(retorno)

def consumer():
    consumer_id = random.randrange(1,100005)
    print("I am consumer #%s" %(consumer_id))
    
    context = zmq.Context()

    #receive work from producer
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect("tcp://0.0.0.0:5345")

    #send work to collector
    consumer_sender = context.socket(zmq.PUSH)
    consumer_sender.connect("tcp://0.0.0.0:5346")
    count = 1
    while True:
        work_message = consumer_receiver.recv_json()
        result = heavyTask(work_message)
        if result['fraud']:
            print(f"Fraud detected and sended to database: {result}")
        else:
            print(f"Message {count} not a fraud.")
        count+=1

        consumer_sender.send_json(result)
    
consumer()