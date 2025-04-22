from PyQt5.QtWidgets import QMessageBox
from controller.Referencias_firebase.Vincular_produtos_firebase import VincularProdutosFirebase
from model.model_vincular import ProdutoVinculado

class SL_BD_Vincular:
    def __init__(self, parent=None):
        self.parent_window = parent
        self.controller = VincularProdutosFirebase()
        self.radio_group = None

    def carregar_empresas(self):
        try:
            if hasattr(self, 'combo_empresa'):
                empresas = self.controller.obter_empresas()
                self.combo_empresa.clear()
                for empresa_id, nome in empresas:
                    self.combo_empresa.addItem(nome, empresa_id)
        except Exception as e:
            QMessageBox.critical(self.parent_window, "Erro", f"Falha ao carregar empresas:\n{str(e)}")

    def carregar_categorias(self):
        try:
            if hasattr(self, 'combo_categoria'):
                categorias = self.controller.obter_categorias()
                self.combo_categoria.clear()
                for cat_id, nome in categorias:
                    self.combo_categoria.addItem(nome, cat_id)
                if categorias:
                    self.carregar_produtos_por_categoria()
        except Exception as e:
            QMessageBox.critical(self.parent_window, "Erro", f"Falha ao carregar categorias:\n{str(e)}")

    def carregar_produtos_por_categoria(self):
        try:
            if hasattr(self, 'combo_categoria') and hasattr(self, 'combo_produto'):
                categoria_id = self.combo_categoria.currentData()
                produtos = self.controller.obter_produtos_por_categoria(categoria_id)
                self.combo_produto.clear()
                for prod_id, nome in produtos:
                    self.combo_produto.addItem(nome, prod_id)
        except Exception as e:
            QMessageBox.critical(self.parent_window, "Erro", f"Falha ao carregar produtos:\n{str(e)}")

    def salvar_dados(self):
        try:
            empresa_id = self.combo_empresa.currentData() if hasattr(self, 'combo_empresa') else None
            categoria_id = self.combo_categoria.currentData() if hasattr(self, 'combo_categoria') else None
            produto_id = self.combo_produto.currentData() if hasattr(self, 'combo_produto') else None
            preco = self.campo_preco.text().strip() if hasattr(self, 'campo_preco') else ""

            # Validação genérica
            if not all([empresa_id, categoria_id, produto_id, preco]):
                raise ValueError("Preencha todos os campos obrigatórios!")

            # Obter promoção
            promocao = next((rb.property('dados') for rb in self.radio_group.buttons() if rb.isChecked()), False) \
                if hasattr(self, 'radio_group') else False

            produto = ProdutoVinculado()
            produto.set_empresa_id(empresa_id)
            produto.set_categoria_id(categoria_id)
            produto.set_produto_id(produto_id)
            produto.set_preco(float(preco))
            produto.set_promocao(promocao)

            if self.controller.vincular_produto(produto):
                QMessageBox.information(self.parent_window, "Sucesso", "Vinculação realizada!")
                self.limpar_campos()
                return True
            else:
                raise Exception("Erro na comunicação com o servidor")

        except ValueError as ve:
            QMessageBox.warning(self.parent_window, "Aviso", str(ve))
            return False
        except Exception as e:
            QMessageBox.critical(self.parent_window, "Erro", f"Falha crítica:\n{str(e)}")
            return False

    def limpar_campos(self, *args):
        if hasattr(self, 'campo_preco'):
            self.campo_preco.clear()
        if hasattr(self, 'combo_categoria'):
            self.combo_categoria.setCurrentIndex(0)
        if hasattr(self, 'combo_empresa'):
            self.combo_empresa.setCurrentIndex(0)
        if hasattr(self, 'radio_group'):
            for rb in self.radio_group.buttons():
                if rb.property('dados') == False:
                    rb.setChecked(True)
                    break