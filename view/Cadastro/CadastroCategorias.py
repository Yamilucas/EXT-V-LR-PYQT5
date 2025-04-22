import sys
import os
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from recursivas.layouts.Areas_padrao_layout import BaseLayout
from recursivas.layouts.formulario_layout import FormularioLayout
from recursivas.layouts.botoes_cadastro import BotoesCadastro
from controller.Salva_bd.Salvar_e_limpar_Categoria import SL_BD_Categoria  

class CadastroCategoriasView(BaseLayout, FormularioLayout, SL_BD_Categoria):
    def __init__(self, parent=None):
        super().__init__()
        SL_BD_Categoria.__init__(self, parent)
        self.parent_window = parent
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Área Superior
        self.criar_area_superior(main_layout, "Cadastro de Categorias")

        # Área de Conteúdo
        content_widget, content_layout = self.criar_area_conteudo(
            main_layout,
            subtitulo="Preencha os dados da categoria"
        )

        # Campo do formulário
        self.campo_nome = QLineEdit()
        self.campo_nome.setPlaceholderText("Digite o nome da categoria")
        content_layout.addLayout(self.criar_linha("Nome da Categoria:", self.campo_nome))

        content_layout.addSpacing(10)

        # Botões (usando lógica herdada)
        botoes = BotoesCadastro(
            lambda: self.salvar_categoria(self.campo_nome.text().strip()),  # Chamada direta
            self.limpar_campos
        )
        content_layout.addLayout(botoes.criar_botoes())

        # Área Inferior
        self.criar_area_inferior(
         main_layout,
         parent_window=self.parent_window,
         mostrar_menu_principal=True,
        # mostrar_voltar_cadastro=True  
)

        self.setLayout(main_layout)