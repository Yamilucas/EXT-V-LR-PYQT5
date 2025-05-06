import sys
import os
import base64
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QComboBox, 
                            QLabel, QWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from recursivas.layouts.Areas_padrao_layout import BaseLayout
from recursivas.layouts.formulario_layout import FormularioLayout
from controller.Referencias_firebase.Cadastro_Empresas_firebase import CadastroEmpresaFirebase

class ComparadorPrecosView(BaseLayout, FormularioLayout):
    def __init__(self, parent=None):
        super().__init__()
        self.parent_window = parent
        self.inf_empresas = CadastroEmpresaFirebase()
        self.initUI()
        self.carregar_logos()

    def initUI(self):
        main_layout = QVBoxLayout()
        
        # Área Superior
        self.criar_area_superior(main_layout, "Comparador de Preços")
        
        # Área de Conteúdo
        content_widget, content_layout = self.criar_area_conteudo(
            main_layout, subtitulo="Escolha os dados a serem comparados"
        )
        
        # Container principal
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(15)

        # Comboboxes
        self.combo_categorias = QComboBox()
        linha_categoria = self.criar_linha("Categoria do Produto:", self.combo_categorias)
        
        self.combo_produtos = QComboBox()
        linha_produto = self.criar_linha("Nome do Produto:", self.combo_produtos)

        container_layout.addLayout(linha_categoria)
        container_layout.addLayout(linha_produto)

        # Label de instrução
        lbl_instrucao = QLabel("Selecione 3 Empresas:")
        lbl_instrucao.setStyleSheet("""
            QLabel {
                color: white;
                font: bold 14px;
                padding: 10px 0;
                margin-top: 15px;
            }
        """)
        container_layout.addWidget(lbl_instrucao)

        # Área de logos centralizada
        self.logos_container = QWidget()
        self.logos_layout = QHBoxLayout(self.logos_container)
        self.logos_layout.setAlignment(Qt.AlignCenter)
        self.logos_layout.setSpacing(10)
        
        container_layout.addWidget(self.logos_container)

        # Adiciona à área de conteúdo
        content_layout.addWidget(container)

        # Área Inferior
        self.criar_area_inferior(
            main_layout,
            parent_window=self.parent_window,
            mostrar_menu_principal=True
        )
        
        self.setLayout(main_layout)

    def carregar_logos(self):
        empresas = self.inf_empresas.obter_todas_empresas()
        for empresa_id, dados in empresas.items():
            logo_base64 = self.inf_empresas.obter_logo_empresa(empresa_id)
            if logo_base64:
                try:
                    dados_imagem = base64.b64decode(logo_base64)
                    pixmap = QPixmap()
                    pixmap.loadFromData(dados_imagem)
                    
                    if not pixmap.isNull():
                        imagem_final = QPixmap(40, 40)
                        imagem_final.fill(Qt.transparent)
                       
                        comprimento_original = pixmap.width()
                        altura_original = pixmap.height()
                        proporcao = comprimento_original / altura_original
                        
                        
                        if proporcao > 1: 
                            novo_comprimento = 40
                            nova_altura = int(40 / proporcao)
                        else: 
                            nova_altura = 40
                            novo_comprimento = int(40 * proporcao)
                        
                       
                        imagem_redimensionada = pixmap.scaled(
                            novo_comprimento,
                            nova_altura,
                            Qt.KeepAspectRatio,
                            Qt.SmoothTransformation
                        )
                        
                        
                        empresa_visualizada = QPainter(imagem_final)
                        x_pos = (40 - imagem_redimensionada.width()) // 2
                        y_pos = (40 - imagem_redimensionada.height()) // 2
                        empresa_visualizada.drawPixmap(x_pos, y_pos, imagem_redimensionada)
                        empresa_visualizada.end()
                        
                        
                        logo_label = QLabel()
                        logo_label.setFixedSize(40, 40)
                        logo_label.setPixmap(imagem_final)
                        logo_label.setStyleSheet("""
                            QLabel {
                                border: 1px solid rgba(255, 255, 255, 0.2);
                                border-radius: 5px;
                                background-clip: padding-box;
                            }
                            QLabel:hover {
                                border-color: #FFA500;
                                background-color: rgba(255, 165, 0, 0.1);
                            }
                        """)
                        self.logos_layout.addWidget(logo_label)
                        
                except Exception as e:
                    print(f"Erro ao processar logo da empresa {dados.get('nome_empresa', '')}: {str(e)}")
                    continue