from firebase_admin import db
from model.model_empresas import Empresa

class CadastroEmpresaFirebase:
    def __init__(self):
        self.ref = db.reference('/empresas')
        self.MAX_EMPRESAS = 10

    def salvar_empresa(self, empresa: Empresa) -> bool:
        try:
            empresas = self.obter_todas_empresas()
            
            # Verificar limite máximo
            if len(empresas) >= self.MAX_EMPRESAS:
                raise ValueError("Limite máximo de empresas atingido!")

            novo_nome = empresa.get_nome_empresa().strip().lower()
            nova_logo = empresa.get_logo()

            # Verificar duplicatas
            for emp_id, emp in empresas.items():
                if emp['nome_empresa'].strip().lower() == novo_nome:
                    raise ValueError("Já existe uma empresa com este nome!")
                
                if emp['logo_base64'] == nova_logo:
                    raise ValueError("Esta imagem já está cadastrada para outra empresa!")

            # Se passou nas validações, salvar
            dados = {
                'nome_empresa': empresa.get_nome_empresa(),
                'logo_base64': empresa.get_logo(),
            }
            
            nova_ref = self.ref.push()
            nova_ref.set(dados)
            
            print(f"🔥 Dados salvos sob ID: {nova_ref.key}")
            return True
            
        except ValueError as ve:
            print(f"🚨 Validação: {str(ve)}")
            raise  
        except db.ApiCallError as e:
            print(f"🚨 Erro de API: {e.detail}")
            return False
        except Exception as e:
            print(f"💥 Erro geral: {str(e)}")
            return False

    def obter_todas_empresas(self):
        try:
            empresas = self.ref.get()
            return empresas if empresas else {}
        except Exception as e:
            print(f"💥 Erro ao obter empresas: {str(e)}")
            return {}

    def obter_nomes_empresas(self): 
        empresas = self.obter_todas_empresas()
        return [(key, emp['nome_empresa']) for key, emp in empresas.items()] if empresas else []

    def obter_logo_empresa(self, empresa_id: str) -> str:
        try:
            empresa = self.ref.child(empresa_id).get()
            return empresa.get('logo_base64', '') if empresa else ''
        except Exception as e:
            print(f"💥 Erro ao obter logo: {str(e)}")
            return ''