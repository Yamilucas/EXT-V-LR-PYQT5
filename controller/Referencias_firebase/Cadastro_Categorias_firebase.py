from firebase_admin import db
from controller.Conexao import inicializar_firebase
from model.model_categorias import Categoria

class CadastroCategoriaFirebase:
    def __init__(self):
        if inicializar_firebase():
            self.ref = db.reference('/categorias')
        else:
            raise Exception("Falha na inicialização do Firebase")

    def salvar_categoria(self, categoria: Categoria) -> bool:
        try:
            dados = {
                'nome_categoria': categoria.get_nome_categoria(),
            }
            
            nova_ref = self.ref.push()
            nova_ref.set(dados)
            
            print(f"Categoria salva sob ID: {nova_ref.key}")
            return True
            
        except Exception as e:
            print(f"Erro ao salvar categoria: {str(e)}")
            return False
        
        