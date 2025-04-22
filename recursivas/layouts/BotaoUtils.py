from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt  # Importação adicionada para resolver o erro

class BotaoUtils:
    @staticmethod
    def criar_botoes(botoes_info, layout, estilo, parent=None, fonte="Arial", tamanho_fonte=12, espacamento=20):
        for botao_info in botoes_info:
            botao = QPushButton(botao_info["texto"], parent)
            botao.setFont(QFont(fonte, tamanho_fonte))
            botao.setStyleSheet(estilo)
            botao.clicked.connect(botao_info["funcao"])
            layout.addWidget(botao, alignment=Qt.AlignCenter)  # Qt.AlignCenter agora está definido
            layout.addSpacing(espacamento)