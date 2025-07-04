import firebase_admin
import pickle
from firebase_admin import credentials
from firebase_admin import firestore


model = pickle.load(open('model.sav', 'rb'))

# substitua o nome do arquivo .json a seguir pela chave .json que você baixou
# do console do Firebase
cred = credentials.Certificate("../bookdevopsml1-5eb8c-firebase-adminsdk-fbsvc-e96fba635b.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

produtos_ref = db.collection('produtos')
docs = produtos_ref.stream()

for doc in docs:
    d = doc.to_dict()
    print('Descrição = {}\n   Categoria = {} '.format(d['descricao'], d['categoria']))

    # Monta a mensagem para servir de entrada ao modelo
    input_message = [d['descricao']] 

    # Aplica o preprocessamento na entrada
    input_message = model["vect"].transform(input_message) 

    # Realiza a predição
    final_prediction = model["clf"].predict(input_message)[0]

    # Obtém uma referência para o documento no BD
    doc_ref = db.collection('produtos').document(doc.id) 

    # Salva o resultado no banco de dados
    doc_ref.update({"categoria": final_prediction}) 