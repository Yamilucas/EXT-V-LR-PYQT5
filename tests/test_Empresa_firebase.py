import sys
import os
from unittest.mock import MagicMock
import pytest

# Adiciona a raiz do projeto ao sys.path para garantir que o módulo seja encontrado
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa a classe após ajustar o sys.path
from recursivas.layouts.CadastroEmpresasView import CadastroEmpresasView

@pytest.fixture
def setup_view():
    """Fixture para configurar o ambiente de teste."""
    view = CadastroEmpresasView()  # Cria uma instância da view
    view.salvar_empresa = MagicMock()  # Mocka a função de salvar
    return view

def test_salvar_empresa(setup_view):
    """Teste para verificar se a empresa foi cadastrada corretamente."""
    view = setup_view

    # Definir o nome da empresa que será usada no teste
    nome_empresa = "Empresa Teste"

    # Preencher o campo de nome
    view.campo_nome.setText(nome_empresa)

    # Simular o clique no botão de salvar
    view.salvar_empresa(view.campo_nome.text().strip(), view.gerenciador_imagem.imagem_base64)

    # Verificar se a função de salvar foi chamada com o nome da empresa
    view.salvar_empresa.assert_called_once_with(nome_empresa, view.gerenciador_imagem.imagem_base64)
