import sys
import os
import base64
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QComboBox, QLabel, QMessageBox)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from firebase_admin import db

# Adicionar caminho raiz ao Python Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controller.Conexao import inicializar_firebase

class VisualizadorProdutos(QWidget):
    def __init__(self):
        super().__init__()
        self.categorias = {}
        self.produtos = {}
        self.initUI()
        self.carregar_categorias()

    def initUI(self):
        self.setWindowTitle("Visualizador de Produtos")
        self.setMinimumSize(600, 500)
        self.setStyleSheet("background-color: #F0F0F0;")

        # Layout principal centralizado
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # ComboBox para seleção de categoria
        self.combo_categorias = QComboBox()
        self.combo_categorias.setFixedWidth(300)
        self.combo_categorias.setStyleSheet("""
            QComboBox {
                padding: 8px;
                font-size: 14px;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
            }
        """)
        self.combo_categorias.currentIndexChanged.connect(self.carregar_produtos)
        layout.addWidget(self.combo_categorias)

        # ComboBox para seleção de produtos
        self.combo_produtos = QComboBox()
        self.combo_produtos.setFixedWidth(300)
        self.combo_produtos.setStyleSheet("""
            QComboBox {
                padding: 8px;
                font-size: 14px;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
            }
        """)
        self.combo_produtos.currentIndexChanged.connect(self.exibir_dados)
        layout.addWidget(self.combo_produtos)

        # Área da imagem
        self.lbl_imagem = QLabel()
        self.lbl_imagem.setFixedSize(300, 300)
        self.lbl_imagem.setStyleSheet("""
            border: 2px solid #CCCCCC;
            border-radius: 8px;
            background-color: white;
        """)
        layout.addWidget(self.lbl_imagem)

        # Label do nome do produto
        self.lbl_nome = QLabel()
        self.lbl_nome.setFont(QFont("Arial", 14, QFont.Bold))
        self.lbl_nome.setStyleSheet("color: #333333;")
        layout.addWidget(self.lbl_nome)

        self.setLayout(layout)

    def carregar_categorias(self):
        try:
            ref = db.reference('/categorias')
            snapshot = ref.get()
            
            if not snapshot:
                QMessageBox.warning(self, "Aviso", "Nenhuma categoria encontrada!")
                return
            
            self.categorias = snapshot
            self.combo_categorias.clear()
            
            for categoria_id, dados in self.categorias.items():
                if 'nome_categoria' in dados:
                    self.combo_categorias.addItem(dados['nome_categoria'], categoria_id)
            
            self.carregar_produtos()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar categorias:\n{str(e)}")

    def carregar_produtos(self):
        try:
            categoria_id = self.combo_categorias.currentData()
            if not categoria_id:
                return

            ref = db.reference('/produtos')
            snapshot = ref.get()
            
            if not snapshot:
                QMessageBox.warning(self, "Aviso", "Nenhum produto encontrado!")
                return
            
            self.produtos = {}
            self.combo_produtos.clear()
            
            for produto_id, dados in snapshot.items():
                if dados.get('categoria_id') == categoria_id:
                    self.produtos[produto_id] = dados
                    self.combo_produtos.addItem(dados['nome_produto'], produto_id)
            
            self.exibir_dados()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar produtos:\n{str(e)}")

    def exibir_dados(self):
        produto_id = self.combo_produtos.currentData()
        if not produto_id or produto_id not in self.produtos:
            self.lbl_imagem.clear()
            self.lbl_nome.clear()
            return

        produto = self.produtos[produto_id]
        
        # Exibir nome do produto
        self.lbl_nome.setText(produto.get('nome_produto', 'Nome não disponível'))
        self.lbl_nome.setAlignment(Qt.AlignCenter)
        
        # Exibir imagem
        imagem_base64 = produto.get('imagem_base64', '')
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
        window = VisualizadorProdutos()
        window.showMaximized()
        sys.exit(app.exec_())
    else:
        QMessageBox.critical(None, "Erro", "Falha na conexão com o Firebase!")