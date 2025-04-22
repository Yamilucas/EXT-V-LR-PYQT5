from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles.nav import obter_estilo_nav

class BaseLayout(QWidget):
    def __init__(self):
        super().__init__()
        
    def criar_area_superior(self, layout, titulo):
        area_superior = QWidget(self)
        area_superior.setStyleSheet("background-color: black;")
        area_superior.setFixedHeight(100)

        label_superior = QLabel(titulo, self)
        label_superior.setFont(QFont("Arial", 14, QFont.Bold))
        label_superior.setStyleSheet("color: white;")
        label_superior.setAlignment(Qt.AlignCenter)
        
        area_superior_layout = QVBoxLayout(area_superior)
        area_superior_layout.addWidget(label_superior)
        area_superior.setLayout(area_superior_layout)

        layout.addWidget(area_superior)
        return area_superior

    def criar_area_conteudo(self, layout, subtitulo=None):
        content_widget = QWidget(self)
        content_layout = QVBoxLayout(content_widget)
        content_widget.setStyleSheet("background-color: red;")  
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        if subtitulo:
            label_subtitulo = QLabel(subtitulo, self)
            label_subtitulo.setFont(QFont("Arial", 14, QFont.Bold))
            label_subtitulo.setStyleSheet("color: white;")
            label_subtitulo.setAlignment(Qt.AlignCenter)
            content_layout.addSpacing(40)
            content_layout.addWidget(label_subtitulo)
            content_layout.addSpacing(40)
        
        layout.addWidget(content_widget)
        return content_widget, content_layout

    def criar_area_inferior(self, layout, parent_window=None, mostrar_menu_principal=False):
        area_inferior = QWidget(self)
        area_inferior.setStyleSheet("background-color: black;")
        area_inferior.setFixedHeight(100)
        
        # Layout para centralização
        area_inferior_layout = QVBoxLayout(area_inferior)
        area_inferior_layout.setAlignment(Qt.AlignCenter)
        
        # Adiciona botão apenas se solicitado
        if mostrar_menu_principal and parent_window:
            botao_menu = QPushButton("Menu Principal", self)
            botao_menu.setFont(QFont("Arial", 12))
            botao_menu.setStyleSheet(obter_estilo_nav())
            botao_menu.clicked.connect(lambda: parent_window.navigate_to('inicio'))
            area_inferior_layout.addWidget(botao_menu)
        
        layout.addWidget(area_inferior)
        return area_inferior