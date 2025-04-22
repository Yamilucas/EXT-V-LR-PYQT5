import sys
import os
from PyQt5.QtWidgets import ( QVBoxLayout, QLineEdit,QComboBox, QMessageBox)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controller.Vincular_produtos_firebase import VincularProdutosFirebase
from model.model_vincular import ProdutoVinculado
from recursivas.layouts.Areas_padrao_layout import BaseLayout
from recursivas.layouts.formulario_layout import FormularioLayout
from recursivas.layouts.botoes_cadastro import BotoesCadastro 

class CadastroProdutosView(BaseLayout, FormularioLayout):
    def __init__(self, parent=None):
        super().__init__()
        self.parent_window = parent
        self.controller = VincularProdutosFirebase()
        self.radio_group = None
        self.initUI()
        self.carregar_empresas()
        self.carregar_categorias()

    def initUI(self):
        main_layout = QVBoxLayout()
        
        # Área Superior
        self.criar_area_superior(main_layout, "Vinculação de Produtos")
        
        # Área de Conteúdo
        content_widget, content_layout = self.criar_area_conteudo(
            main_layout,
            subtitulo="Relacione o produto ao mercado"
        )

        # Campos do formulário
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        # Combobox Empresas
        self.combo_empresa = QComboBox()
       
        form_layout.addLayout(self.criar_linha("Empresa:", self.combo_empresa))

        # Combobox Categorias
        self.combo_categoria = QComboBox()
        self.combo_categoria.currentIndexChanged.connect(self.carregar_produtos_por_categoria)
        form_layout.addLayout(self.criar_linha("Categoria:", self.combo_categoria))

        # Combobox Produtos
        self.combo_produto = QComboBox()
        form_layout.addLayout(self.criar_linha("Produto:", self.combo_produto))

        # Campo Preço
        self.campo_preco = QLineEdit()
        self.campo_preco.setPlaceholderText("R$ 0.00")
        form_layout.addLayout(self.criar_linha("Preço:", self.campo_preco))

        # RadioButtons Promoção usando o novo método
        linha_promo, self.radio_group = self.criar_linha_radio(
            "Promoção:",
            [
                {'texto': 'Sim', 'dados': True},
                {'texto': 'Não', 'dados': False, 'checked': True}
            ]
        )
        form_layout.addLayout(linha_promo)

        content_layout.addLayout(form_layout)

        content_layout.addSpacing(10)

       # Botões usando classe reutilizável
        botoes = BotoesCadastro(self.salvar_dados, self.limpar_campos)
        button_container = botoes.criar_botoes()
        content_layout.addLayout(button_container)

        # Área Inferior
        self.criar_area_inferior(
            main_layout,
            parent_window=self.parent_window,
            mostrar_menu_principal=True
        )

        self.setLayout(main_layout)

    def carregar_empresas(self):
        try:
            empresas = self.controller.obter_empresas()
            self.combo_empresa.clear()
            for empresa_id, empresa_nome in empresas:
                self.combo_empresa.addItem(empresa_nome, empresa_id)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar empresas:\n{str(e)}")

    def carregar_categorias(self):
        try:
            categorias = self.controller.obter_categorias()
            self.combo_categoria.clear()
            for categoria_id, categoria_nome in categorias:
                self.combo_categoria.addItem(categoria_nome, categoria_id)
            
            if categorias:
                self.carregar_produtos_por_categoria()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar categorias:\n{str(e)}")

    def carregar_produtos_por_categoria(self):
        try:
            categoria_id = self.combo_categoria.currentData()
            if not categoria_id:
                return

            produtos = self.controller.obter_produtos_por_categoria(categoria_id)
            self.combo_produto.clear()
            for produto_id, produto_nome in produtos:
                self.combo_produto.addItem(produto_nome, produto_id)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar produtos:\n{str(e)}")

    def salvar_dados(self):
        try:
            empresa_id = self.combo_empresa.currentData()
            categoria_id = self.combo_categoria.currentData()
            produto_id = self.combo_produto.currentData()
            preco = self.campo_preco.text()
            
            if not all([empresa_id, categoria_id, produto_id, preco]):
                raise ValueError("Preencha todos os campos obrigatórios!")

            # Obter valor do radio button
            promocao = next((rb.property('dados') for rb in self.radio_group.buttons() if rb.isChecked()), False)

            produto = ProdutoVinculado()
            produto.set_empresa_id(empresa_id)
            produto.set_categoria_id(categoria_id)
            produto.set_produto_id(produto_id)
            produto.set_preco(float(preco))
            produto.set_promocao(promocao)

            if self.controller.vincular_produto(produto):
                QMessageBox.information(self, "Sucesso", "Vinculação realizada!")
                self.limpar_campos()
            else:
                raise Exception("Erro na comunicação com o servidor")

        except ValueError as ve:
            QMessageBox.warning(self, "Aviso", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha crítica:\n{str(e)}")

    def limpar_campos(self):
        self.campo_preco.clear()
        self.combo_categoria.setCurrentIndex(0)
        self.combo_empresa.setCurrentIndex(0)
        self.carregar_produtos_por_categoria()
        for rb in self.radio_group.buttons():
            if rb.property('dados') == False:
                rb.setChecked(True)
                break