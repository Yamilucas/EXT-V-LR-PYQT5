import sys
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QApplication
from Inicio import InicioView
from view.Cadastro.Cadastro import CadastroView
from view.Cadastro.CadastroCategorias import CadastroCategoriasView
from view.Cadastro.CadastroEmpresas import CadastroEmpresasView
from view.Cadastro.CadastroVinculacao import CadastroVincularView
from view.Cadastro.CadastroProdutos import CadastroProdutosView
from view.ComparadorPrecos import ComparadorPrecosView
from controller.Conexao import inicializar_firebase
from VisualizarProdutosView import VisualizarProdutosView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Comparador de Preços - Supermercado Marinho")
        
        # Configuração do sistema de navegação
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Inicializa todas as views
        self.views = {
            'inicio': InicioView(self),
            'cadastro': CadastroView(self),
            'cadastro_categorias': CadastroCategoriasView(self),
            'cadastro_empresas': CadastroEmpresasView(self),
            'cadastro_produtos': CadastroProdutosView(self),
            'cadastro_produtos_vinculacao':CadastroVincularView(self),
            'comparador_precos': ComparadorPrecosView(self),
            'visualizar_produtos': VisualizarProdutosView(self)

        }
        
        for view in self.views.values():
            self.stacked_widget.addWidget(view)
        
        # Mostra a view principal inicialmente
        self.navigate_to('inicio')
        
    def navigate_to(self, view_name):
        self.stacked_widget.setCurrentWidget(self.views[view_name])

if __name__ == "__main__":
    if not inicializar_firebase():  
        sys.exit("❌ Falha na conexão com o Firebase. Verifique sua conexão com a internet.")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())