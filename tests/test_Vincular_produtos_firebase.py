import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Adiciona o diretório 'model' e 'controller' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'controller')))

# Agora podemos importar corretamente
from model_vincular import ProdutoVinculado
from Referencias_firebase.Vincular_produtos_firebase import VincularProdutosFirebase

# Fixture para criar uma instância de ProdutoVinculado
@pytest.fixture
def produto_vinculado():
    produto = ProdutoVinculado()
    produto.set_produto_id("produto_123")
    produto.set_preco(20.0)
    produto.set_promocao(True)
    produto.set_categoria_id("categoria_123")
    produto.set_empresa_id("empresa_123")
    return produto

# Teste com mock
@patch('Referencias_firebase.Vincular_produtos_firebase.VincularProdutosFirebase.vincular_produto')
def test_vinculacao_produto_com_mocking(mock_vincular_produto, produto_vinculado):
    firebase = VincularProdutosFirebase()
    firebase.vincular_produto(produto_vinculado)
    mock_vincular_produto.assert_called_once_with(produto_vinculado)

