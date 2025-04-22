# formulario_layout.py
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox
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

    def _aplicar_estilo_widget(self, widget):
        if isinstance(widget, QLineEdit):
            widget.setStyleSheet("""
                QLineEdit {
                    background-color: white;
                    color: black;
                    border: 1px solid #CCCCCC;
                    border-radius: 4px;
                    padding: 5px;
                }
            """)
            widget.setFixedWidth(300)

        elif isinstance(widget, (QComboBox, QSpinBox, QDoubleSpinBox)):
            widget.setStyleSheet("""
                background-color: white;
                color: black;
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
            """)
            widget.setFixedWidth(300)