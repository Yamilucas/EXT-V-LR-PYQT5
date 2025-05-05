import sys
import os
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QComboBox
from PyQt5.QtCore import Qt
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from recursivas.layouts.Areas_padrao_layout import BaseLayout
from recursivas.layouts.imagem_selecionar import GerenciadorImagem
from recursivas.layouts.formulario_layout import FormularioLayout
from recursivas.layouts.botoes_cadastro import BotoesCadastro
from controller.Salva_bd.Salvar_e_limpar_Produtos import SL_BD_Produtos  

class CadastroProdutosView(BaseLayout, FormularioLayout, SL_BD_Produtos):
    def __init__(self, parent=None):
        super().__init__()
        SL_BD_Produtos.__init__(self, parent) 
        self.parent_window = parent
        self.gerenciador_imagem = GerenciadorImagem(self)
        self.initUI()
        
    def initUI(self):
        produtos_layout = QVBoxLayout()
        
        # Área Superior
        self.criar_area_superior(produtos_layout, "Cadastro de Produtos")
        
        # Área de Conteúdo
        content_widget, content_layout = self.criar_area_conteudo(
            produtos_layout, 
            subtitulo="Preencha os dados do produto"
        )
        
        # Área da Imagem
        imagem_container = self.gerenciador_imagem.criar_area_imagem()
        content_layout.addWidget(imagem_container, alignment=Qt.AlignCenter)

        # Campos do Formulário
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        # Nome do Produto
        self.campo_nome = QLineEdit()
        self.campo_nome.setPlaceholderText("Digite o nome do produto")
        form_layout.addLayout(self.criar_linha("Nome do Produto:", self.campo_nome))

        # Combo de Categorias
        self.combo_categoria = QComboBox()
        form_layout.addLayout(self.criar_linha("Categoria:", self.combo_categoria))

        content_layout.addLayout(form_layout)

        # Botões (conectados aos métodos herdados)
        botoes = BotoesCadastro(
            lambda: self.salvar_produto(
                self.campo_nome.text().strip(),
                self.combo_categoria.currentData(),
                self.gerenciador_imagem.imagem_base64
            ),
            self.limpar_campos
        )
        content_layout.addLayout(botoes.criar_botoes())

        # Área Inferior
        self.criar_area_inferior(
         produtos_layout,
         parent_window=self.parent_window,
         mostrar_menu_principal=True,
       
)

        self.setLayout(produtos_layout)
        self.carregar_categorias()  