from firebase_admin import db
from controller.Conexao import inicializar_firebase
from model.model_empresas import Empresa

class CadastroEmpresaFirebase:
    def __init__(self):
        if inicializar_firebase():
            self.ref = db.reference('/empresas')
        else:
            raise Exception("Falha na inicialização do Firebase")

    def salvar_empresa(self, empresa: Empresa) -> bool:
        try:
            # Estrutura de dados otimizada para RTDB
            dados = {
                'nome_empresa': empresa.get_nome_empresa(),
                'logo_base64': empresa.get_logo(),
            }
            
            # Push + Set atômico
            nova_ref = self.ref.push()
            nova_ref.set(dados)
            
            print(f"🔥 Dados salvos sob ID: {nova_ref.key}")
            return True
            
        except db.ApiCallError as e:
            print(f"🚨 Erro de API: {e.detail}")
            return False
            
        except Exception as e:
            print(f"💥 Erro geral: {str(e)}")
            return False