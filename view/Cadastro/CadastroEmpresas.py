from PyQt5.QtWidgets import QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from recursivas.layouts.Areas_padrao_layout import BaseLayout
from recursivas.layouts.imagem_selecionar import GerenciadorImagem
from recursivas.layouts.formulario_layout import FormularioLayout
from recursivas.layouts.botoes_cadastro import BotoesCadastro
from controller.Salva_bd.Salvar_e_limpar_Empresas import SL_BD_Empresas

class CadastroEmpresasView(BaseLayout, FormularioLayout, SL_BD_Empresas):
    def __init__(self, parent=None):
        super().__init__()
        SL_BD_Empresas.__init__(self, parent)
        self.parent_window = parent
        self.gerenciador_imagem = GerenciadorImagem(self)
        self.initUI()

    def initUI(self):
        empresa_layout = QVBoxLayout()
        self.criar_area_superior(empresa_layout, "Cadastro de Empresas Concorrentes")

        content_widget, content_layout = self.criar_area_conteudo(
            empresa_layout, subtitulo="Preencha os dados da empresa"
        )

        logo_container = self.gerenciador_imagem.criar_area_imagem()
        content_layout.addWidget(logo_container, alignment=Qt.AlignCenter)
        content_layout.addSpacing(10)

        self.campo_nome = QLineEdit()
        self.campo_nome.setPlaceholderText("Digite o nome da empresa")

        form_container = QVBoxLayout()
        form_container.setSpacing(20)
        form_container.addLayout(self.criar_linha("Nome da Empresa:", self.campo_nome))
        content_layout.addLayout(form_container)
        content_layout.addSpacing(10)

        botoes = BotoesCadastro(
            lambda: super(CadastroEmpresasView, self).salvar_empresa(self.campo_nome.text().strip(), self.gerenciador_imagem.imagem_base64),
            lambda: super(CadastroEmpresasView, self).limpar_campos(self.campo_nome, self.gerenciador_imagem)
        )
        content_layout.addLayout(botoes.criar_botoes())

        self.criar_area_inferior(
         empresa_layout,
         parent_window=self.parent_window,
         mostrar_menu_principal=True,
        # mostrar_voltar_cadastro=True  
)
        self.setLayout(empresa_layout)
