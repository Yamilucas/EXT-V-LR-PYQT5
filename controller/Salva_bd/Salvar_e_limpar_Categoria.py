from PyQt5.QtWidgets import QMessageBox
from controller.Referencias_firebase.Cadastro_Categorias_firebase import CadastroCategoriaFirebase
from model.model_categorias import Categoria

class SL_BD_Categoria:
    def __init__(self, parent=None):
        self.parent_window = parent
        self.controller = CadastroCategoriaFirebase()

    def salvar_categoria(self, nome_categoria: str):
        try:
            if not nome_categoria.strip():
                raise ValueError("O nome da categoria é obrigatório!")

            categoria = Categoria()
            categoria.set_nome_categoria(nome_categoria)

            if self.controller.salvar_categoria(categoria):
                QMessageBox.information(  
                    self.parent_window,
                    "Sucesso",
                    "Categoria salva com sucesso!"
                )
                self.limpar_campos()
                return True
            else:
                raise Exception("Falha ao comunicar com o servidor")

        except ValueError as ve:
            mensagem = str(ve)
            
            if "Limite máximo" in mensagem:
                QMessageBox.critical(
                    self.parent_window,
                    "Limite Atingido",
                    "❌ Não é possível cadastrar mais categorias!\nLimite máximo de 10 categorias foi atingido."
                )
            elif "Já existe uma categoria" in mensagem:
                QMessageBox.warning(
                    self.parent_window,
                    "Nome Duplicado",
                    "⚠️ Já existe uma categoria com este nome!\nUtilize um nome diferente."
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
                "Erro",
                f"⛔ Falha ao salvar categoria:\n{str(e)}"
            )
            self.limpar_campos()
            return False

    def limpar_campos(self, *args):
        if hasattr(self, 'campo_nome'):
            self.campo_nome.clear()