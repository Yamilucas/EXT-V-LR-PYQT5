from firebase_admin import db
from controller.Conexao import inicializar_firebase
from model.model_vincular import ProdutoVinculado

class VincularProdutosFirebase:
    def __init__(self):
        if inicializar_firebase():
            self.ref_empresas = db.reference('/empresas')
            self.ref_categorias = db.reference('/categorias')
            self.ref_produtos = db.reference('/produtos')
            self.ref_produtos_vinculados = db.reference('/produtos_vinculados')
        else:
            raise Exception("Falha na inicialização do Firebase")

    def obter_empresas(self):
        try:
            empresas = self.ref_empresas.get()
            return [(key, empresa['nome_empresa']) for key, empresa in empresas.items()] if empresas else []
        except Exception as e:
            print(f"Erro ao buscar empresas: {str(e)}")
            return []

    def obter_categorias(self):
        try:
            categorias = self.ref_categorias.get()
            return [(key, categoria['nome_categoria']) for key, categoria in categorias.items()] if categorias else []
        except Exception as e:
            print(f"Erro ao buscar categorias: {str(e)}")
            return []

    def obter_produtos_por_categoria(self, categoria_id: str):
        try:
            produtos = self.ref_produtos.get()
            return [(key, produto['nome_produto']) for key, produto in produtos.items() if produto.get('categoria_id') == categoria_id] if produtos else []
        except Exception as e:
            print(f"Erro ao buscar produtos: {str(e)}")
            return []

    def vincular_produto(self, produto_vinculado: ProdutoVinculado) -> bool:
        try:
            dados = {
                'empresa_id': produto_vinculado.get_empresa_id(),
                'categoria_id': produto_vinculado.get_categoria_id(),
                'produto_id': produto_vinculado.get_produto_id(),
                'preco_produto': produto_vinculado.get_preco(),
                'promocao_produto': produto_vinculado.get_promocao()
            }

            nova_ref = self.ref_produtos_vinculados.push()
            nova_ref.set(dados)

            print(f"Produto vinculado salvo sob ID: {nova_ref.key}")
            return True
        except Exception as e:
            print(f"Erro ao vincular produto: {str(e)}")
            return False