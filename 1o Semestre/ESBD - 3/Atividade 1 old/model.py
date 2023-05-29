# Exemplo de código para solução proposta

# Importe as bibliotecas necessárias
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from keras.datasets import cifar10
from keras.utils import to_categorical
import pickle
import zmq
import os
from minio import Minio

# Função para treinamento e otimização de hiperparâmetros
def train_and_optimize(X_train, y_train, params):
    model = SVC()
    grid_search = GridSearchCV(model, params)
    grid_search.fit(X_train, y_train)
    return grid_search.best_params_, grid_search.best_score_


# Função para comunicação ZMQ entre os nós distribuídos
def zmq_communication():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    # Envie uma mensagem para solicitar tarefas
    socket.send(b"Send task")
    message = socket.recv()
    
    # Envie uma mensagem para informar a conclusão da tarefa
    socket.send(b"Task completed")
    socket.recv()

    socket.close()
    context.term()

# Código principal
if __name__ == "__main__":
    # Carregue os dados de treinamento
    (X_train, y_train), (X_test, y_test) = cifar10.load_data()
    X_train = to_categorical(X_train)
    y_train = to_categorical(y_train)
    X_train = X_train.astype('float32')/255.0
    y_train = y_train.astype('float32')/255.0
    
    # Defina a grade de hiperparâmetros a serem explorados
    params = {'C': [0.1, 1, 10], 'kernel': ['linear', 'rbf']}

    # Execute a otimização de hiperparâmetros e treinamento
    best_params, best_score = train_and_optimize(X_train, y_train, params)
    best_model = SVC(**best_params)
    best_model.fit(X_train, y_train)

    
    # Inicie a comunicação ZMQ em um novo processo ou em um nó distribuído
    zmq_communication()

    # Código para salvar o modelo no MinIO
    client = Minio("localhost:9000", access_key="minio", secret_key="minio123", secure=False)
    pickled_object = pickle.dumps(best_model)
    client.put_object(bucket_name="models",object_name="best_model.pkl",data=pickled_object,length=len(pickled_object),content_type="application/octet-stream")

    # Download and unpickle
    data = client.get_object(
        bucket_name="models",
        object_name="best_model.pkl"
    )

    pickled_object = data.read()
    charged_model = pickle.loads(pickled_object)

    #evaluate from pickle
    loss_test, accuracy_test = charged_model.evaluate(X_test, y_test)
    print('Accuracy: ', accuracy_test, ' Loss: ', loss_test)