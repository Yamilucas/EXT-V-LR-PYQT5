import sys
import os
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QComboBox
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from recursivas.layouts.Areas_padrao_layout import BaseLayout
from recursivas.layouts.formulario_layout import FormularioLayout
from recursivas.layouts.botoes_cadastro import BotoesCadastro
from controller.Salva_bd.Salvar_e_limpar_Vincular import SL_BD_Vincular  

class CadastroVincularView(BaseLayout, FormularioLayout, SL_BD_Vincular):
    def __init__(self, parent=None):
        super().__init__()
        SL_BD_Vincular.__init__(self, parent)  
        self.parent_window = parent
        self.initUI()
        self.carregar_empresas()  
        self.carregar_categorias()  

    def initUI(self):
        vincular_layout = QVBoxLayout()
        
        # Área Superior
        self.criar_area_superior(vincular_layout, "Vinculação de Produtos")
        
        # Área de Conteúdo
        content_widget, content_layout = self.criar_area_conteudo(
            vincular_layout,
            subtitulo="Relacione o produto ao mercado"
        )

        # Campos do Formulário
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

        # RadioButtons Promoção
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

        # Botões
        botoes = BotoesCadastro(
            self.salvar_dados,  
            self.limpar_campos  
        )
        content_layout.addLayout(botoes.criar_botoes())

        # Área Inferior
        self.criar_area_inferior(
         vincular_layout,
         parent_window=self.parent_window,
         mostrar_menu_principal=True,
        # mostrar_voltar_cadastro=True  
)

        self.setLayout(vincular_layout)