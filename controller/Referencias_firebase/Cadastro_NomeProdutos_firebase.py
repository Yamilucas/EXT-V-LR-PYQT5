from firebase_admin import db
from controller.Conexao import inicializar_firebase
from model.model_nome_produtos import Produto  # Import corrigido

class CadastroNomeProdutosFirebase:
    def __init__(self):
        if inicializar_firebase():
            self.ref_produtos = db.reference('/produtos')
            self.ref_categorias = db.reference('/categorias')
        else:
            raise Exception("Falha na inicialização do Firebase")

    def obter_categorias(self):
        try:
            categorias = self.ref_categorias.get()
            return [(key, cat['nome_categoria']) for key, cat in categorias.items()] if categorias else []
        except Exception as e:
            print(f"Erro ao buscar categorias: {str(e)}")
            return []

    def salvar_produto(self, produto: Produto, categoria_id: str) -> bool:
        try:
            dados = {
                'nome_produto': produto.get_nome_produto(),
                'imagem_base64': produto.get_imagem_produto(),
                'categoria_id': categoria_id
            }
            
            nova_ref = self.ref_produtos.push()
            nova_ref.set(dados)
            
            print(f"Produto salvo sob ID: {nova_ref.key}")
            return True
            
        except Exception as e:
            print(f"Erro ao salvar produto: {str(e)}")
            return False