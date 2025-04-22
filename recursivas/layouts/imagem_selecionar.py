import base64
from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QPushButton,  QFileDialog, QMessageBox, QSizePolicy)
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QRect
from styles.sel_im import obter_estilo_borda, obter_estilo_botao_circular

class GerenciadorImagem:
    def __init__(self, parent):
        self.parent = parent
        self.imagem_base64 = ""
        self.original_pixmap = None
        
    def criar_area_imagem(self, container_size=240):
        container = QWidget()
        container.setFixedSize(container_size, container_size)
        layout = QGridLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        self.lbl_imagem = QLabel()
        self.lbl_imagem.setObjectName("area_imagem")
        self.lbl_imagem.setStyleSheet(obter_estilo_borda())
        self.lbl_imagem.setAlignment(Qt.AlignCenter)
        self.lbl_imagem.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.lbl_imagem)

        self.btn_add_imagem = QPushButton("+")
        self.btn_add_imagem.setObjectName("botao_mais")
        self.btn_add_imagem.setStyleSheet(obter_estilo_botao_circular())
        self.btn_add_imagem.clicked.connect(self.selecionar_imagem)
        layout.addWidget(self.btn_add_imagem, 0, 0, alignment=Qt.AlignCenter)

        return container

    def selecionar_imagem(self):
        try:
            arquivo, _ = QFileDialog.getOpenFileName(
                self.parent, 
                "Selecionar Imagem", 
                "", 
                "Imagens (*.png *.jpg *.jpeg)"
            )
            
            if arquivo:
                with open(arquivo, "rb") as f:
                    img_data = f.read()
                    self.imagem_base64 = base64.b64encode(img_data).decode("utf-8")
                
                self.original_pixmap = QPixmap(arquivo)
                self.atualizar_tamanho_imagem()
                self.btn_add_imagem.hide()
                
        except Exception as e:
            QMessageBox.critical(self.parent, "Erro", f"Falha ao carregar imagem:\n{str(e)}")

    def atualizar_tamanho_imagem(self):
     if self.original_pixmap and not self.original_pixmap.isNull():
         # Tamanho máximo da área de exibição (200x200)
         comprimento_maximo = 200
         altura_maxima = 200
        
         # Obter proporções originais
         comprimento_original = self.original_pixmap.width()
         altura_original = self.original_pixmap.height()
         proporcao = comprimento_original / altura_original

         # Calcular novas dimensões mantendo proporção
         if comprimento_original > altura_original:
             novo_comprimento = min(comprimento_original, comprimento_maximo)
             nova_altura = int(novo_comprimento / proporcao)
         else:
             nova_altura = min(altura_original, altura_maxima)
             novo_comprimento = int(nova_altura * proporcao)

         # Redimensionar suavemente
         imagem_escalada = self.original_pixmap.scaled(
             novo_comprimento,
             nova_altura,
             Qt.KeepAspectRatio,
             Qt.SmoothTransformation
         )

         # Criar canvas com fundo transparente
         Imagem_final = QPixmap(240, 240)
         Imagem_final.fill(Qt.transparent)
        
         Pintura_visual_na_view = QPainter(Imagem_final)
        
         # Calcular posição de desenho centralizada
         x_offset = (240 - imagem_escalada.width()) // 2
         y_offset = (240 - imagem_escalada.height()) // 2
        
         Pintura_visual_na_view.drawPixmap(x_offset, y_offset, imagem_escalada)
         Pintura_visual_na_view.end()

         self.lbl_imagem.setPixmap(Imagem_final)

    def limpar_imagem(self):
        self.lbl_imagem.clear()
        self.btn_add_imagem.show()
        self.imagem_base64 = ""
        self.original_pixmap = None