from firebase_admin import db
from model.model_vincular import ProdutoVinculado

class VincularProdutosFirebase:
    def __init__(self):
        self.ref_produtos_vinculados = db.reference('/produtos_vinculados')
        self.MAX_EMPRESAS_POR_PRODUTO = 5

    def vincular_produto(self, produto_vinculado: ProdutoVinculado) -> bool:
        try:
            vinculados = self.obter_todos_vinculados()
            produto_id = produto_vinculado.get_produto_id()
            empresa_id = produto_vinculado.get_empresa_id()

        
            vinculacoes_produto = [v for v in vinculados if v[1]['produto_id'] == produto_id]
            if len(vinculacoes_produto) >= self.MAX_EMPRESAS_POR_PRODUTO:
                raise ValueError("Limite de 5 empresas por produto atingido!")

           
            if any(v[1]['empresa_id'] == empresa_id for v in vinculacoes_produto):
                raise ValueError("Produto já vinculado a esta empresa!")

            dados = {
                'empresa_id': empresa_id,
                'categoria_id': produto_vinculado.get_categoria_id(),
                'produto_id': produto_id,
                'preco_produto': produto_vinculado.get_preco(),
                'promocao_produto': produto_vinculado.get_promocao()
            }

            nova_ref = self.ref_produtos_vinculados.push()
            nova_ref.set(dados)

            print(f"✅ Produto vinculado salvo sob ID: {nova_ref.key}")
            return True

        except ValueError as ve:
            print(f"🔴 Validação: {str(ve)}")
            raise
        except Exception as e:
            print(f"🔴 Erro ao vincular produto: {str(e)}")
            return False

  
    def obter_todos_vinculados(self):
        try:
            vinculados = self.ref_produtos_vinculados.get()
            return [(key, vinculo) for key, vinculo in vinculados.items()] if vinculados else []
        except Exception as e:
            print(f"🔴 Erro ao buscar vinculados: {str(e)}")
            return []

    def obter_empresas_vinculadas(self):
        vinculados = self.obter_todos_vinculados()
        return [(key, vinculo['empresa_id']) for key, vinculo in vinculados] if vinculados else []

    def obter_categorias_vinculadas(self):
        vinculados = self.obter_todos_vinculados()
        return [(key, vinculo['categoria_id']) for key, vinculo in vinculados] if vinculados else []

    def obter_produtos_vinculados(self):
        vinculados = self.obter_todos_vinculados()
        return [(key, vinculo['produto_id']) for key, vinculo in vinculados] if vinculados else []

    def obter_precos_vinculados(self):
        vinculados = self.obter_todos_vinculados()
        return [(key, vinculo['preco_produto']) for key, vinculo in vinculados] if vinculados else []

    def obter_promocoes_vinculadas(self):
        vinculados = self.obter_todos_vinculados()
        return [(key, vinculo['promocao_produto']) for key, vinculo in vinculados] if vinculados else []