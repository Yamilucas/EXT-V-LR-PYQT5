from PyQt5.QtWidgets import QMessageBox
from controller.Referencias_firebase.Cadastro_Empresas_firebase import CadastroEmpresaFirebase
from model.model_empresas import Empresa

class SL_BD_Empresas:
    def __init__(self, parent=None):
        self.parent_window = parent
        self.controller = CadastroEmpresaFirebase()

    def salvar_empresa(self, nome_empresa, logo_base64):
        try:
            if not nome_empresa:
                raise ValueError("O nome da empresa é obrigatório!")
                
            if not logo_base64:
                raise ValueError("Selecione uma imagem para a logo!")
            
            empresa = Empresa()
            empresa.set_nome_empresa(nome_empresa)
            empresa.set_logo(logo_base64)

            if self.controller.salvar_empresa(empresa):
                QMessageBox.information(
                    self.parent_window, 
                    "Sucesso", 
                    "Dados da empresa salvos com sucesso!"
                )
                self.limpar_campos()  # Chamada sem parâmetros
                return True
            else:
                raise Exception("Falha ao comunicar com o servidor")
                
        except Exception as e:
            QMessageBox.critical(
                self.parent_window, 
                "Erro", 
                f"Falha ao salvar os dados:\n{str(e)}"
            )
            self.limpar_campos()  # Chamada sem parâmetros
            return False

    def limpar_campos(self, *args):  # Aceita argumentos extras (ignora)
        # Acessa os campos diretamente da classe filha
        if hasattr(self, 'campo_nome'):
            self.campo_nome.clear()
        if hasattr(self, 'gerenciador_imagem') and hasattr(self.gerenciador_imagem, 'limpar_imagem'):
            self.gerenciador_imagem.limpar_imagem()