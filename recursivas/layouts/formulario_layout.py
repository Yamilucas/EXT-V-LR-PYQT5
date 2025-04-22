from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QLineEdit, QComboBox, QRadioButton, QButtonGroup)
from PyQt5.QtGui import QFont

class FormularioLayout:
    def criar_linha(self, texto: str, widget):
        linha = QHBoxLayout()
        
        # Configuração padrão da label
        label = QLabel(texto)
        label.setFont(QFont("Arial", 12))
        label.setFixedWidth(150)
        label.setStyleSheet("color: white;")
        
        # Aplica estilização automática
        self._aplicar_estilo_widget(widget)
        
        linha.addWidget(label)
        linha.addWidget(widget)
        
        return linha

    def criar_linha_radio(self, texto: str, opcoes: list, grupo=None):
        linha = QHBoxLayout()
        label = QLabel(texto)
        label.setFont(QFont("Arial", 12))
        label.setFixedWidth(150)
        label.setStyleSheet("color: white;")
        
        grupo_radio = QButtonGroup(self) if grupo is None else grupo
        radio_layout = QHBoxLayout()
        
        for opcao in opcoes:
            rb = QRadioButton(opcao['texto'])
            rb.setStyleSheet("""
                QRadioButton {
                    color: white;
                    spacing: 5px;
                }
                QRadioButton::indicator {
                    width: 16px;
                    height: 16px;
                }
            """)
            if opcao.get('checked', False):
                rb.setChecked(True)
            if 'dados' in opcao:
                rb.setProperty('dados', opcao['dados'])
            grupo_radio.addButton(rb)
            radio_layout.addWidget(rb)
        
        linha.addWidget(label)
        linha.addLayout(radio_layout)
        return linha, grupo_radio

    def _aplicar_estilo_widget(self, widget):
        base_style = """
            background-color: white;
            color: black;
            border: 1px solid #CCCCCC;
            border-radius: 4px;
            padding: 5px;
        """
        
        if isinstance(widget, QLineEdit):
            widget.setStyleSheet(f"QLineEdit {{ {base_style} }}")
            widget.setFixedWidth(300)

        elif isinstance(widget, (QComboBox)):
            widget.setStyleSheet(base_style)
            widget.setFixedWidth(300)