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

            resultado = self.controller.salvar_empresa(empresa)
            
            if resultado:
                QMessageBox.information(
                    self.parent_window, 
                    "Sucesso", 
                    "Dados da empresa salvos com sucesso!"
                )
                self.limpar_campos()  
                return True
            else:
                raise Exception("Falha na comunicação com o servidor")

        except ValueError as ve:
            mensagem = str(ve)
            
            if "Limite máximo" in mensagem:
                QMessageBox.critical(
                    self.parent_window,
                    "Limite Atingido",
                    "❌ Não é possível cadastrar mais empresas!\nLimite máximo de 10 empresas foi atingido."
                )
            elif "Já existe uma empresa com este nome" in mensagem:
                QMessageBox.warning(
                    self.parent_window,
                    "Nome Duplicado",
                    "⚠️ Já existe uma empresa cadastrada com este nome!\nPor favor, utilize um nome diferente."
                )
            elif "Esta imagem já está cadastrada" in mensagem:
                QMessageBox.warning(
                    self.parent_window,
                    "Imagem Repetida",
                    "🖼️ Esta imagem já está sendo usada por outra empresa!\nSelecione uma imagem diferente."
                )
            else:
                QMessageBox.warning(
                    self.parent_window,
                    "Validação",
                    f"⚠️ {mensagem}"
                )
            
            self.limpar_campos() 
            return False
                
        except Exception as e:
            QMessageBox.critical(
                self.parent_window, 
                "Erro Crítico", 
                f"⛔ Falha grave ao salvar os dados:\n{str(e)}"
            )
            self.limpar_campos()  
            return False

    def limpar_campos(self, *args): 
        if hasattr(self, 'campo_nome'):
            self.campo_nome.clear()
        if hasattr(self, 'gerenciador_imagem') and hasattr(self.gerenciador_imagem, 'limpar_imagem'):
            self.gerenciador_imagem.limpar_imagem()