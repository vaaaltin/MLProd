from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import uuid
import nltk

# Download necessário para o bot
nltk.download('punkt_tab')

# Configuração da sessão de chat
sessao = uuid.uuid4()
nome_bot = "Robô"
chatbot = ChatBot(nome_bot, read_only=True)

# Treinando o robô
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train(
    "chatterbot.corpus.portuguese"
)

# Início da interação com o usuário
print("Sessão de chat iniciada: "+str(sessao))
nome = input('Digite o seu nome: ')

# Conversa principal
while True:
    # Lê pergunta do usuário
    pergunta = input(nome+': ')

    # Envia pergunta ao chatbot e obtém resposta
    resposta = chatbot.get_response(pergunta)

    # Imprime a conversa na tela
    print(nome_bot+': '+str(resposta)+'\n')