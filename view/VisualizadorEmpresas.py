import sys
import os
import base64
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QComboBox,  QLabel, QMessageBox)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from firebase_admin import db

# Adicionar caminho raiz ao Python Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controller.Conexao import inicializar_firebase

class VisualizadorEmpresas(QWidget):
    def __init__(self):
        super().__init__()
        self.empresas = {}
        self.initUI()
        self.carregar_dados()

    def initUI(self):
        self.setWindowTitle("Visualizador de Empresas")
        self.setMinimumSize(600, 500)
        self.setStyleSheet("background-color: #F0F0F0;")

        # Layout principal centralizado
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # ComboBox para seleção
        self.combo_empresas = QComboBox()
        self.combo_empresas.setFixedWidth(300)
        self.combo_empresas.setStyleSheet("""
            QComboBox {
                padding: 8px;
                font-size: 14px;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
            }
        """)
        self.combo_empresas.currentIndexChanged.connect(self.exibir_dados)
        layout.addWidget(self.combo_empresas)

        # Área da imagem
        self.lbl_imagem = QLabel()
        self.lbl_imagem.setFixedSize(300, 300)
        self.lbl_imagem.setStyleSheet("""
            border: 2px solid #CCCCCC;
            border-radius: 8px;
            background-color: white;
        """)
        layout.addWidget(self.lbl_imagem)

        # Label do nome
        self.lbl_nome = QLabel()
        self.lbl_nome.setFont(QFont("Arial", 14, QFont.Bold))
        self.lbl_nome.setStyleSheet("color: #333333;")
        layout.addWidget(self.lbl_nome)

       
        self.setLayout(layout)

    def carregar_dados(self):
        try:
            ref = db.reference('/empresas')
            snapshot = ref.get()
            
            if not snapshot:
                QMessageBox.warning(self, "Aviso", "Nenhuma empresa encontrada!")
                return
            
            self.empresas = snapshot
            self.combo_empresas.clear()
            
            for empresa_id, dados in self.empresas.items():
                if 'nome_empresa' in dados:
                    self.combo_empresas.addItem(dados['nome_empresa'], empresa_id)
            
            self.exibir_dados()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar dados:\n{str(e)}")

    def exibir_dados(self):
        empresa_id = self.combo_empresas.currentData()
        if not empresa_id or empresa_id not in self.empresas:
            self.lbl_imagem.clear()
            self.lbl_nome.clear()
            return

        empresa = self.empresas[empresa_id]
        
        # Exibir nome
        self.lbl_nome.setText(empresa.get('nome_empresa', 'Nome não disponível'))
        self.lbl_nome.setAlignment(Qt.AlignCenter)
        
        # Exibir imagem
        imagem_base64 = empresa.get('logo_base64', '')
        if imagem_base64:
            try:
                # Decodificar e redimensionar
                pixmap = QPixmap()
                pixmap.loadFromData(base64.b64decode(imagem_base64))
                
                scaled_pixmap = pixmap.scaled(
                    self.lbl_imagem.width() - 20,
                    self.lbl_imagem.height() - 20,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                
                self.lbl_imagem.setPixmap(scaled_pixmap)
                self.lbl_imagem.setAlignment(Qt.AlignCenter)
                
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Falha ao carregar imagem:\n{str(e)}")
                self.lbl_imagem.clear()
        else:
            self.lbl_imagem.clear()

if __name__ == "__main__":
    if inicializar_firebase():
        app = QApplication(sys.argv)
        window = VisualizadorEmpresas()
        window.showMaximized()
        sys.exit(app.exec_())
    else:
        QMessageBox.critical(None, "Erro", "Falha na conexão com o Firebase!")