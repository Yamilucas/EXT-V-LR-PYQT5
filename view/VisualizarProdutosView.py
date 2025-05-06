import sys
import os
import base64
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QComboBox, QLabel, 
                            QWidget, QGridLayout, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QCursor

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from recursivas.layouts.Areas_padrao_layout import BaseLayout
from recursivas.layouts.formulario_layout import FormularioLayout
from styles.sel_im import obter_estilo_borda, obter_estilo_preco, obter_estilo_logo_empresa
from controller.Referencias_firebase.Vincular_produtos_firebase import VincularProdutosFirebase
from controller.Referencias_firebase.Cadastro_Empresas_firebase import CadastroEmpresaFirebase
from controller.Referencias_firebase.Cadastro_Categorias_firebase import CadastroCategoriaFirebase
from controller.Referencias_firebase.Cadastro_NomeProdutos_firebase import CadastroNomeProdutosFirebase

class VisualizarProdutosView(BaseLayout, FormularioLayout):
    def __init__(self, parent=None):
        super().__init__()
        self.parent_window = parent
        self.categoria_db = CadastroCategoriaFirebase()
        self.produto_db = CadastroNomeProdutosFirebase()
        self.vinculo_db = VincularProdutosFirebase()
        self.empresa_db = CadastroEmpresaFirebase()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Área Superior
        self.criar_area_superior(main_layout, "Visualização de Produtos - Preencha os dados do Produto que deseja Vizualizar")
        
        # Área de Conteúdo
        content_widget, content_layout = self.criar_area_conteudo(main_layout)
        
        # Container principal
        container = QScrollArea()
        container.setWidgetResizable(True)
        container_widget = QWidget()
        container_layout = QVBoxLayout(container_widget)
        container_layout.setContentsMargins(30, 20, 30, 30)
        container_layout.setSpacing(25)

        # Comboboxes
        self.combo_categorias = QComboBox()
        self.combo_categorias.setFixedHeight(40)
        self.combo_categorias.currentIndexChanged.connect(self.carregar_produtos)
        container_layout.addLayout(self.criar_linha("Categoria do Produto:", self.combo_categorias))
        
        self.combo_produtos = QComboBox()
        self.combo_produtos.setFixedHeight(40)
        self.combo_produtos.currentIndexChanged.connect(self.carregar_detalhes_produto)
        container_layout.addLayout(self.criar_linha("Nome do Produto:", self.combo_produtos))

        # Área da Imagem
        self.img_container = QLabel()
        self.img_container.setObjectName("area_imagem")
        self.img_container.setStyleSheet(obter_estilo_borda())
        self.img_container.setAlignment(Qt.AlignCenter)
        self.img_container.setFixedSize(280, 280)
        container_layout.addWidget(self.img_container, alignment=Qt.AlignCenter)

        # Container de informações
        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)
        info_layout.setSpacing(15)
        
        # Preço e Promoção
        self.preco_label = QLabel("Preço: --")
        self.preco_label.setObjectName("preco_label")
        self.preco_label.setStyleSheet(obter_estilo_preco())
        self.preco_label.setAlignment(Qt.AlignCenter)
        
        self.promocao_label = QLabel("Promoção: Não")
        self.promocao_label.setStyleSheet("""
            QLabel {
                color: #FF4444;
                font: bold 14px;
                background-color: rgba(0, 0, 0, 0.7);
                border-radius: 5px;
                padding: 5px 10px;
            }
        """)
        self.promocao_label.setAlignment(Qt.AlignCenter)
        
        info_layout.addWidget(self.preco_label)
        info_layout.addWidget(self.promocao_label)
        container_layout.addWidget(info_container, alignment=Qt.AlignCenter)

        # Grid de Logos
        self.empresas_container = QWidget()
        self.empresas_layout = QGridLayout(self.empresas_container)
        self.empresas_layout.setHorizontalSpacing(25)
        self.empresas_layout.setVerticalSpacing(20)
        container_layout.addWidget(self.empresas_container)

        container.setWidget(container_widget)
        content_layout.addWidget(container)
        
        # Área Inferior
        self.criar_area_inferior(main_layout, self.parent_window, mostrar_menu_principal=True)
        
        self.setLayout(main_layout)
        self.carregar_categorias()

    def carregar_categorias(self):
        self.combo_categorias.clear()
        categorias = self.categoria_db.obter_nomes_categorias()
        for cat_id, nome in categorias:
            self.combo_categorias.addItem(nome, userData=cat_id)

    def carregar_produtos(self):
        self.combo_produtos.clear()
        cat_id = self.combo_categorias.currentData()
        if cat_id:
            produtos = self.produto_db.obter_produtos_por_categoria(cat_id)
            for prod_id, nome in produtos:
                self.combo_produtos.addItem(nome, userData=prod_id)

    def carregar_detalhes_produto(self):
        prod_id = self.combo_produtos.currentData()
        if prod_id:
            # Carrega imagem
            imagem_base64 = self.produto_db.obter_imagem_produto(prod_id)
            if imagem_base64:
                pixmap = QPixmap()
                pixmap.loadFromData(base64.b64decode(imagem_base64))
                
                scaled_pix = pixmap.scaled(
                    260, 260, 
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                )
                
                canvas = QPixmap(280, 280)
                canvas.fill(Qt.transparent)
                painter = QPainter(canvas)
                x = (280 - scaled_pix.width()) // 2
                y = (280 - scaled_pix.height()) // 2
                painter.drawPixmap(x, y, scaled_pix)
                painter.end()
                
                self.img_container.setPixmap(canvas)
            
            self.carregar_empresas_vinculadas(prod_id)
            self.preco_label.setText("Preço: --")
            self.promocao_label.setText("Promoção: Não")

    def carregar_empresas_vinculadas(self, produto_id):
        # Limpa layout
        for i in reversed(range(self.empresas_layout.count())):
            if widget := self.empresas_layout.itemAt(i).widget():
                widget.deleteLater()
        
        # Busca vinculações
        vinculacoes = self.vinculo_db.ref_produtos_vinculados.get() or {}
        empresas = [
            (k, v) for k, v in vinculacoes.items() 
            if v.get('produto_id') == produto_id
        ][:5]

        # Configurações visuais
        hand_cursor = QCursor(Qt.PointingHandCursor)
        
        # Exibe logos
        row = col = 0
        for vinculo_id, dados in empresas:
            empresa_id = dados.get('empresa_id')
            if logo_base64 := self.empresa_db.obter_logo_empresa(empresa_id):
                try:
                    logo_label = QLabel()
                    logo_label.setObjectName("logo_empresa")
                    logo_label.setStyleSheet(obter_estilo_logo_empresa())
                    logo_label.setCursor(hand_cursor)
                    logo_label.setFixedSize(120, 120)
                    
                    pixmap = QPixmap()
                    pixmap.loadFromData(base64.b64decode(logo_base64))
                    scaled_logo = pixmap.scaled(
                        110, 110, 
                        Qt.KeepAspectRatio, 
                        Qt.SmoothTransformation
                    )
                    
                    logo_label.setPixmap(scaled_logo)
                    logo_label.setToolTip(
                        f"{self.empresa_db.obter_todas_empresas()[empresa_id]['nome_empresa']}\n"
                        f"Preço: R$ {dados.get('preco_produto', 0):.2f}\n"
                        f"Promoção: {'Sim' if dados.get('promocao_produto') else 'Não'}"
                    )
                    
                    # Evento de clique
                    logo_label.mousePressEvent = lambda _, p=dados.get('preco_produto'), prom=dados.get('promocao_produto'): self.mostrar_preco(p, prom)
                    
                    self.empresas_layout.addWidget(logo_label, row, col)
                    col = (col + 1) % 2  # 2 colunas
                    row += 1 if col == 0 else 0
                    
                except Exception as e:
                    print(f"Erro ao carregar logo: {str(e)}")

    def mostrar_preco(self, preco, promocao):
        self.preco_label.setText(f"Preço: R$ {float(preco or 0):.2f}")
        
        if promocao:
            self.promocao_label.setText("Promoção: Sim ")
            self.promocao_label.setStyleSheet("""
                QLabel {
                    color: #00FF00;
                    font: bold 14px;
                    background-color: rgba(0, 0, 0, 0.7);
                    border-radius: 5px;
                    padding: 5px 10px;
                }
            """)
        else:
            self.promocao_label.setText("Promoção: Não")
            self.promocao_label.setStyleSheet("""
                QLabel {
                    color: #FF4444;
                    font: bold 14px;
                    background-color: rgba(0, 0, 0, 0.7);
                    border-radius: 5px;
                    padding: 5px 10px;
                }
            """)