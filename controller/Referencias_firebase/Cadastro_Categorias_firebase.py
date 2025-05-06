from firebase_admin import db
from model.model_categorias import Categoria

class CadastroCategoriaFirebase:
    def __init__(self):
        self.ref = db.reference('/categorias')
        self.MAX_CATEGORIAS = 10

    def salvar_categoria(self, categoria: Categoria) -> bool:
        try:
            categorias = self.obter_todas_categorias()
            
            # Verificar limite máximo
            if len(categorias) >= self.MAX_CATEGORIAS:
                raise ValueError("Limite máximo de categorias atingido!")

            novo_nome = categoria.get_nome_categoria().strip().lower()
            
            # Verificar duplicatas
            for cat_id, cat in categorias.items():
                if cat['nome_categoria'].strip().lower() == novo_nome:
                    raise ValueError("Já existe uma categoria com este nome!")

            dados = {
                'nome_categoria': categoria.get_nome_categoria(),
            }
            
            nova_ref = self.ref.push()
            nova_ref.set(dados)
            
            print(f"✅ Categoria salva sob ID: {nova_ref.key}")
            return True
            
        except ValueError as ve:
            print(f"🔴 Validação: {str(ve)}")
            raise 
        except Exception as e:
            print(f"🔴 Erro ao salvar categoria: {str(e)}")
            return False

    def obter_todas_categorias(self):
        try:
            categorias = self.ref.get()
            return categorias if categorias else {}
        except Exception as e:
            print(f"🔴 Erro ao obter categorias: {str(e)}")
            return {}

    def obter_nomes_categorias(self):
        categorias = self.obter_todas_categorias()
        return [(key, cat['nome_categoria']) for key, cat in categorias.items()] if categorias else []