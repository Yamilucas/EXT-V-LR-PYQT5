from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont
from styles.Estilo_botoes_de_sellecao import obter_estilo

class BotoesCadastro:
    def __init__(self, acao_salvar, acao_limpar):
        self.acao_salvar = acao_salvar
        self.acao_limpar = acao_limpar

    def criar_botoes(self):
        layout_vertical = QVBoxLayout()
        layout_horizontal = QHBoxLayout()
        layout_horizontal.setSpacing(20)

        btn_limpar = QPushButton("Limpar")
        btn_limpar.setFixedSize(150, 40)
        btn_limpar.setFont(QFont("Arial", 12))
        btn_limpar.setStyleSheet(obter_estilo())
        btn_limpar.clicked.connect(self.acao_limpar)

        btn_salvar = QPushButton("Salvar")
        btn_salvar.setFixedSize(150, 40)
        btn_salvar.setFont(QFont("Arial", 12))
        btn_salvar.setStyleSheet(obter_estilo())
        btn_salvar.clicked.connect(self.acao_salvar)

        layout_horizontal.addWidget(btn_limpar)
        layout_horizontal.addWidget(btn_salvar)

        layout_vertical.addLayout(layout_horizontal)
     
        return layout_vertical
