import sys
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QApplication
from Inicio import InicioView
from view.Cadastro.Cadastro import CadastroView
from view.Cadastro.CadastroCategorias import CadastroCategoriasView
from view.Cadastro.CadastroEmpresas import CadastroEmpresasView
from view.Cadastro.CadastroVinculacao import CadastroVincularView
from view.Cadastro.CadastroProdutosGerais import CadastroProdutosGeraisView

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
            'cadastro_produtos': CadastroVincularView(self),
            'cadastro_produtos_gerais': CadastroProdutosGeraisView(self)
        }
        
        for view in self.views.values():
            self.stacked_widget.addWidget(view)
        
        # Mostra a view principal inicialmente
        self.navigate_to('inicio')
        
    def navigate_to(self, view_name):
        self.stacked_widget.setCurrentWidget(self.views[view_name])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())