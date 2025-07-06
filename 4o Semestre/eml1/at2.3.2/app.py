from classificador.model import Model

# Carrega o modelo BERT pré-treinado (demora um tempinho)
print('Carregando modelo...')
model = Model()
print('Modelo carregado!')

# Vamos testar um exemplo qualquer
texto = "Você é muito ruim"
sentiment, confidence, probabilities = model.predict(texto)
print(sentiment)