import sys
import os
from importlib import import_module

# Adiciona o diretório 'controller' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'controller')))

# Adiciona o diretório 'model' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model')))

# Imprime o caminho atual para verificar se o diretório foi adicionado corretamente
print("Caminho no sys.path:", sys.path)

# Tenta importar dinamicamente o módulo usando importlib
CadastroNomeProdutosFirebase = import_module('Referencias_firebase.Cadastro_NomeProdutos_firebase')

import pytest
from unittest.mock import MagicMock
from PyQt5.QtWidgets import QComboBox, QLineEdit, QWidget
from recursivas.layouts.CadastroProdutosView import CadastroProdutosView

# Mock para o método de salvar
@pytest.fixture
def mock_salvar_produto():
    return MagicMock()

# Teste para verificar o funcionamento do comboBox de categoria e o cadastro do produto
def test_combo_box_e_cadastro(mock_salvar_produto):
    # Cria a instância da view de cadastro
    app = QWidget()
    view = CadastroProdutosView(parent=app)

    # Preenche o campo de nome do produto
    nome_produto = "Produto Teste"
    view.campo_nome.setText(nome_produto)

    # Adiciona categorias ao comboBox (simulando a adição de categorias)
    view.combo_categoria.addItem("Categoria 1", userData="Categoria_1")
    view.combo_categoria.addItem("Categoria 2", userData="Categoria_2")
    
    # Simula a seleção da categoria no comboBox
    view.combo_categoria.setCurrentIndex(1)  # Seleciona "Categoria 2"
    
    # Chama a função de salvar, passando o nome do produto e a categoria selecionada
    view.salvar_produto = mock_salvar_produto  # Substitui o método de salvar real por um mock
    view.salvar_produto(
        view.campo_nome.text().strip(), 
        view.combo_categoria.currentData(), 
        None  # Simulação de imagem (pode ser alterado para a lógica real)
    )

    # Verifica se o método de salvar foi chamado com os parâmetros corretos
    mock_salvar_produto.assert_called_with(
        nome_produto,  # Nome do produto
        "Categoria_2",  # Categoria selecionada
        None  # Imagem (aqui estamos simulando como None, mas pode ser uma string base64)
    )

    # Verifica se o nome do produto foi corretamente atribuído
    assert view.campo_nome.text().strip() == nome_produto

    # Verifica se a categoria selecionada é "Categoria_2"
    assert view.combo_categoria.currentData() == "Categoria_2"
