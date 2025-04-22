from PyQt5.QtWidgets import QMessageBox
from controller.Referencias_firebase.Cadastro_NomeProdutos_firebase import CadastroNomeProdutosFirebase
from model.model_nome_produtos import Produto

class SL_BD_Produtos:
    def __init__(self, parent=None):
        self.parent_window = parent
        self.controller = CadastroNomeProdutosFirebase()
        self.produto = Produto()

    def carregar_categorias(self):
        try:
            if hasattr(self, 'combo_categoria'):
                categorias = self.controller.obter_categorias()
                self.combo_categoria.clear()
                for cat_id, nome in categorias:
                    self.combo_categoria.addItem(nome, cat_id)
        except Exception as e:
            QMessageBox.critical(
                self.parent_window,
                "Erro", 
                f"Falha ao carregar categorias:\n{str(e)}"
            )

    def salvar_produto(self, nome: str, categoria_id: str, imagem_base64: str):
        try:
            if not nome.strip():
                raise ValueError("Nome do produto é obrigatório!")
            if not categoria_id:
                raise ValueError("Selecione uma categoria!")
            if not imagem_base64:
                raise ValueError("Selecione uma imagem!")

            self.produto.set_nome_produto(nome)
            self.produto.set_categoria_id(categoria_id)
            self.produto.set_imagem_produto(imagem_base64)

            if self.controller.salvar_produto(self.produto, categoria_id):
                QMessageBox.information(
                    self.parent_window,
                    "Sucesso",
                    "Produto salvo com sucesso!"
                )
                self.limpar_campos()
                return True
            else:
                raise Exception("Falha ao comunicar com o servidor")

        except Exception as e:
            QMessageBox.critical(
                self.parent_window,
                "Erro",
                f"Falha ao salvar produto:\n{str(e)}"
            )
            self.limpar_campos()
            return False

    def limpar_campos(self, *args):
        if hasattr(self, 'campo_nome'):
            self.campo_nome.clear()
        if hasattr(self, 'combo_categoria'):
            self.combo_categoria.setCurrentIndex(0)
        if hasattr(self, 'gerenciador_imagem') and hasattr(self.gerenciador_imagem, 'limpar_imagem'):
            self.gerenciador_imagem.limpar_imagem()
