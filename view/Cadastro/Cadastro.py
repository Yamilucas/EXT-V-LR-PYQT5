import sys
import os
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import Qt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles.Estilo_botoes_de_sellecao import obter_estilo
from recursivas.layouts.BotaoUtils import BotaoUtils  
from recursivas.layouts.Areas_padrao_layout import BaseLayout

class CadastroView(BaseLayout):
    def __init__(self, parent=None):
        super().__init__()
        self.parent_window = parent 
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
     
        self.criar_area_superior(main_layout, "Opções de Cadastro")
        
        # Área de Conteúdo Principal
        content_widget, content_layout = self.criar_area_conteudo(
            main_layout, 
            subtitulo="Escolha o Cadastro" 
        )
        
        # Adiciona Botões de Cadastro
        botoes = [
            {"texto": "Concorrentes", "funcao": lambda: self.parent_window.navigate_to('cadastro_empresas')},
            {"texto": "Categorias", "funcao": lambda: self.parent_window.navigate_to('cadastro_categorias')},
            {"texto": "Nome de um Produto", "funcao": lambda: self.parent_window.navigate_to('cadastro_produtos_gerais')},
            {"texto": "Vinculação de Produtos", "funcao": lambda: self.parent_window.navigate_to('cadastro_produtos')}
        ]

        BotaoUtils.criar_botoes(
            botoes_info=botoes,
            layout=content_layout,
            estilo=obter_estilo(),
            parent=self
        )


        self.criar_area_inferior(
            main_layout,
            parent_window=self.parent_window,
            mostrar_menu_principal=True  
        )

        self.setLayout(main_layout)