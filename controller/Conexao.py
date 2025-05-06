import firebase_admin
from firebase_admin import credentials, db
import os
def inicializar_firebase():
    try:
        if not firebase_admin._apps:
            # Caminho absoluto do arquivo de credenciais
            diretorio_atual = os.path.dirname(os.path.abspath(__file__))
            caminho_json = os.path.join(diretorio_atual, "extv-lr-firebase-adminsdk-fbsvc-1260f39b8e.json")
            
            cred = credentials.Certificate(caminho_json)
            
            # Configurar para Realtime Database
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://extv-lr-default-rtdb.firebaseio.com/'
            })
            print("✅ Firebase inicializado!")
        
        # Testa a conexão com uma operação simples
        ref = db.reference('teste_conexao')
        ref.get()  # Força uma operação de leitura
        return True
    
    except Exception as e:
        print(f"🚨 Erro: {str(e)}")
        return False