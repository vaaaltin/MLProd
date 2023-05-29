import time
import zmq
import random
import tensorflow as tf


def heavyTask(i):
    lrn_rate = i.get("learning_rate") if i.get("learning_rate") else 0.001
    n_neurons = i.get("n_neurons") if i.get("n_neurons") else 128
    actv_fun = i.get("activation_fun") if i.get("activation_fun") else 'relu'
    n_epochs = i.get("n_epochs") if i.get("n_epochs") else 5
    
    # Load the dataset
    (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

    # Preprocess the data
    train_images = train_images / 255.0
    test_images = test_images / 255.0

    # Define the model architecture
    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(n_neurons, activation=actv_fun),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    # Compile the model
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=lrn_rate),
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

    # Train the model
    model.fit(train_images, train_labels, epochs=n_epochs)

    # Evaluate the model
    test_loss, test_acc = model.evaluate(test_images, test_labels)
    print('Test accuracy:', test_acc)
    
    return {"learning_rate":lrn_rate, "n_neurons":n_neurons, "activation_fun": actv_fun, "n_epochs":n_epochs, "test_acc": test_acc}

def consumer():
    consumer_id = random.randrange(1,100005)
    print("I am consumer #%s" %(consumer_id))
    
    context = zmq.Context()

    #receive work from producer
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect("tcp://0.0.0.0:8000")

    #send work to collector
    consumer_sender = context.socket(zmq.PUSH)
    consumer_sender.connect("tcp://0.0.0.0:8001")

    while True:
        work_message = consumer_receiver.recv_json()
        if work_message.get('nmb_hiperparams'):
            result = {'consumer': consumer_id, 'nmb_hiperparams': work_message['nmb_hiperparams']}
            consumer_sender.send_json(result)
        result = {'consumer': consumer_id, 'result': heavyTask(work_message)}
        print(result)

        consumer_sender.send_json(result)
    
consumer()