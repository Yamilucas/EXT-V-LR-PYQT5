from PyQt5.QtWidgets import QMessageBox
from controller.Referencias_firebase.Vincular_produtos_firebase import VincularProdutosFirebase
from controller.Referencias_firebase.Cadastro_Empresas_firebase import CadastroEmpresaFirebase
from controller.Referencias_firebase.Cadastro_Categorias_firebase import CadastroCategoriaFirebase
from controller.Referencias_firebase.Cadastro_NomeProdutos_firebase import CadastroNomeProdutosFirebase  
from model.model_vincular import ProdutoVinculado

class SL_BD_Vincular(CadastroCategoriaFirebase):
    def __init__(self, parent=None):
        super().__init__()  
        self.parent_window = parent
        self.vincular_controller = VincularProdutosFirebase()  
        self.empresa_controller = CadastroEmpresaFirebase()  
        self.produtos_controller = CadastroNomeProdutosFirebase() 
        self.radio_group = None

    def carregar_empresas(self):
        try:
            if hasattr(self, 'combo_empresa'):
                empresas = self.empresa_controller.obter_nomes_empresas()  
                self.combo_empresa.clear()
                for empresa_id, nome in empresas:
                    self.combo_empresa.addItem(nome, empresa_id)
        except Exception as e:
            QMessageBox.critical(self.parent_window, "Erro", f"Falha ao carregar empresas:\n{str(e)}")

    def carregar_categorias(self):
        try:
            if hasattr(self, 'combo_categoria'):
                categorias = self.obter_nomes_categorias()  
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
                produtos = self.produtos_controller.obter_produtos_por_categoria(categoria_id) 
                self.combo_produto.clear()
                for prod_id, nome in produtos:
                    self.combo_produto.addItem(nome, prod_id)
        except Exception as e:
            QMessageBox.critical(self.parent_window, "Erro", f"Falha ao carregar produtos:\n{str(e)}")

    def salvar_dados(self):
        try:
            # Obter dados dos campos
            empresa_id = self.combo_empresa.currentData() if hasattr(self, 'combo_empresa') else None
            categoria_id = self.combo_categoria.currentData() if hasattr(self, 'combo_categoria') else None
            produto_id = self.combo_produto.currentData() if hasattr(self, 'combo_produto') else None
            preco = self.campo_preco.text().strip() if hasattr(self, 'campo_preco') else ""

            # Validar campos obrigatórios
            if not all([empresa_id, categoria_id, produto_id, preco]):
                raise ValueError("Preencha todos os campos obrigatórios!")

            # Validar preço numérico
            try:
                preco_float = float(preco)
            except:
                raise ValueError("Preço deve ser um valor numérico!")

            # Obter status da promoção
            promocao = next((rb.property('dados') for rb in self.radio_group.buttons() if rb.isChecked()), False) \
                if hasattr(self, 'radio_group') else False

            # Configurar objeto
            produto_vinculado = ProdutoVinculado()
            produto_vinculado.set_empresa_id(empresa_id)
            produto_vinculado.set_categoria_id(categoria_id)
            produto_vinculado.set_produto_id(produto_id)
            produto_vinculado.set_preco(preco_float)
            produto_vinculado.set_promocao(promocao)

            # Tentar vincular
            if self.vincular_controller.vincular_produto(produto_vinculado):
                QMessageBox.information(
                    self.parent_window, 
                    "Sucesso", 
                    "Vinculação realizada com sucesso!"
                )
                self.limpar_campos()
                return True
            else:
                raise Exception("Falha na comunicação com o servidor")

        except ValueError as ve:
            erro = str(ve)
            # Tratamento específico para erros
            if "Limite de 5 empresas" in erro:
                QMessageBox.critical(
                    self.parent_window,
                    "Limite Atingido",
                    "❌ Este produto já está vinculado a 5 empresas diferentes!"
                )
            elif "já vinculado" in erro:
                QMessageBox.warning(
                    self.parent_window,
                    "Vinculação Duplicada",
                    "⚠️ Este produto já está cadastrado para esta empresa! A vinculação só pode ser feita 1 vez por empresa"
                )
            elif "Preço deve ser" in erro:
                QMessageBox.warning(
                    self.parent_window,
                    "Formato Inválido",
                    "🔢 O preço deve conter apenas números e ponto decimal!"
                )
            else:
                QMessageBox.warning(
                    self.parent_window,
                    "Validação",
                    f"⚠️ {erro}"
                )
            self.limpar_campos()
            return False

        except Exception as e:
            QMessageBox.critical(
                self.parent_window, 
                "Erro Crítico", 
                f"⛔ Falha grave ao salvar:\n{str(e)}"
            )
            self.limpar_campos()
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