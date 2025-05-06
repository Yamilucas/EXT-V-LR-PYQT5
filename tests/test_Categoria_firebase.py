import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Corrige o caminho para importar os módulos do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'controller')))

from Referencias_firebase.Vincular_produtos_firebase import VincularProdutosFirebase
from model.model_vincular import ProdutoVinculado

@pytest.fixture
def produto_vinculado():
    produto = ProdutoVinculado()
    produto.set_produto_id("produto_123")
    produto.set_nome_produto("Produto Teste")
    produto.set_preco(20.0)
    produto.set_promocao(True)
    produto.set_categoria_id("categoria_123")
    produto.set_empresa_id("empresa_123")
    return produto

@patch('Referencias_firebase.Vincular_produtos_firebase.VincularProdutosFirebase.vincular_produto')
def test_vinculacao_produto_com_mocking(mock_vincular_produto, produto_vinculado):
    firebase = VincularProdutosFirebase()
    firebase.vincular_produto(produto_vinculado)
    mock_vincular_produto.assert_called_once_with(produto_vinculado)
