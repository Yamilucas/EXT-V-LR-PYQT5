import sys
import os
from PyQt5.QtWidgets import QVBoxLayout, QMessageBox
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles.Estilo_botoes_de_sellecao import obter_estilo
from recursivas.layouts.Areas_padrao_layout import BaseLayout
from recursivas.layouts.BotaoUtils import BotaoUtils 

class InicioView(BaseLayout):
    def __init__(self, parent=None):
        super().__init__()
        self.parent_window = parent
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        self.criar_area_superior(main_layout, "Página Inicial")
        content_widget, content_layout = self.criar_area_conteudo(
            main_layout, 
            subtitulo="Comparador de Preços Supermercado Marinho" 
        )
        self.criar_area_inferior(main_layout)

    
        botoes = [
            {"texto": "Cadastro", "funcao": lambda: self.parent_window.navigate_to('cadastro')},
            {"texto": "Visualizar Produtos", "funcao": self.aviso_visualizar_produtos},
            {"texto": "Comparar Produtos", "funcao": self.aviso_comparar_produtos}
        ]

        BotaoUtils.criar_botoes(
            botoes_info=botoes,
            layout=content_layout,
            estilo=obter_estilo(),
            parent=self
        )

        self.setLayout(main_layout)

    def aviso_visualizar_produtos(self):
        QMessageBox.information(self, "Aviso", "A funcionalidade de Visualizar Produtos ainda não está disponível.")

    def aviso_comparar_produtos(self):
        QMessageBox.information(self, "Aviso", "A funcionalidade de Comparar Produtos ainda não está disponível.")