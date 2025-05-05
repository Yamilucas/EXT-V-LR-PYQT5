from firebase_admin import db
from model.model_nome_produtos import Produto

class CadastroNomeProdutosFirebase:
    def __init__(self):
        self.ref_produtos = db.reference('/produtos')
        self.MAX_PRODUTOS_POR_CATEGORIA = 10

    
    def obter_todos_produtos(self):
        try:
            produtos = self.ref_produtos.get()
            return produtos if produtos else {}
        except Exception as e:
            print(f"🔴 Erro ao obter produtos: {str(e)}")
            return {}

    def obter_nomes_produtos(self):
        produtos = self.obter_todos_produtos()
        return [(key, prod['nome_produto']) for key, prod in produtos.items()] if produtos else []

    def obter_imagem_produto(self, produto_id: str) -> str:
        try:
            produto = self.ref_produtos.child(produto_id).get()
            return produto.get('imagem_base64', '') if produto else ''
        except Exception as e:
            print(f"🔴 Erro ao obter imagem: {str(e)}")
            return ''

    def obter_categoria_produto(self, produto_id: str) -> str:
        try:
            produto = self.ref_produtos.child(produto_id).get()
            return produto.get('categoria_id', '') if produto else ''
        except Exception as e:
            print(f"🔴 Erro ao obter categoria: {str(e)}")
            return ''

    def obter_produtos_por_categoria(self, categoria_id: str):
        try:
            produtos = self.obter_todos_produtos()
            return [
                (key, prod['nome_produto'])
                for key, prod in produtos.items()
                if prod.get('categoria_id') == categoria_id
            ] if produtos else []
        except Exception as e:
            print(f"🔴 Erro ao filtrar produtos: {str(e)}")
            return []

  
    def _verificar_limite_categoria(self, categoria_id: str):
        produtos = self.obter_produtos_por_categoria(categoria_id)
        if len(produtos) >= self.MAX_PRODUTOS_POR_CATEGORIA:
            raise ValueError("Limite de 10 produtos por categoria atingido!")

    def verificar_duplicatas(self, nome: str, imagem: str, categoria_id: str):
        produtos = self.obter_todos_produtos()
        nome = nome.strip().lower()
        
        for prod_id, prod in produtos.items():
            if prod.get('categoria_id') == categoria_id:
                if prod['nome_produto'].strip().lower() == nome:
                    raise ValueError("Nome já existe na categoria!")
                if prod['imagem_base64'] == imagem:
                    raise ValueError("Imagem já cadastrada na categoria!")

    def salvar_produto(self, produto: Produto, categoria_id: str) -> bool:
        try:
            # Validações
            self._verificar_limite_categoria(categoria_id)
            self.verificar_duplicatas(
                produto.get_nome_produto(),
                produto.get_imagem_produto(),
                categoria_id
            )

           
            dados = {
                'nome_produto': produto.get_nome_produto(),
                'imagem_base64': produto.get_imagem_produto(),
                'categoria_id': categoria_id
            }
            
            nova_ref = self.ref_produtos.push()
            nova_ref.set(dados)
            
            print(f"✅ Produto salvo sob ID: {nova_ref.key}")
            return True

        except ValueError as ve:
            print(f"🔴 Validação: {str(ve)}")
            raise
        except Exception as e:
            print(f"🔴 Erro geral: {str(e)}")
            return False