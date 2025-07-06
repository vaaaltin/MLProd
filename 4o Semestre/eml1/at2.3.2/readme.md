# Como rodar o kafka(nessa versão não é mais necessario zookeeper):
1. Terminal1: bin/kafka-server-start.sh config/server.properties
2. Terminal2: bin/kafka-console-consumer.sh --topic chatbot --from-beginning --bootstrap-server localhost:9092
3. at2.3.1: source chatbot/bin/activate, python app.py
4. at2.3.2: pyenv activate analise-sentimentos, python app.py