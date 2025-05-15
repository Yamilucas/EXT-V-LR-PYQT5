import sys
import os
import pytest
from unittest.mock import patch

# Adiciona os diretórios necessários ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'controller')))

# Importações dos módulos
from model.model_vincular import ProdutoVinculado
from controller.Referencias_firebase.Vincular_produtos_firebase import VincularProdutosFirebase

# Fixture para instanciar e configurar um ProdutoVinculado
@pytest.fixture
def produto_vinculado():
    produto = ProdutoVinculado()
    produto.set_produto_id("produto_123")
    produto.set_preco(20.0)
    produto.set_promocao(True)
    produto.set_categoria_id("categoria_123")
    produto.set_empresa_id("empresa_123")
    return produto

#Teste 1: Verifica se todos os dados do produto foram corretamente atribuídos
def test_dados_produto_vinculado(produto_vinculado):
    assert produto_vinculado.get_produto_id() == "produto_123"
    assert produto_vinculado.get_preco() == 20.0
    assert produto_vinculado.get_promocao() is True
    assert produto_vinculado.get_categoria_id() == "categoria_123"
    assert produto_vinculado.get_empresa_id() == "empresa_123"

#Teste 2: Verifica se a vinculação foi chamada corretamente
@patch('Referencias_firebase.Vincular_produtos_firebase.VincularProdutosFirebase.vincular_produto')
def test_vinculacao_produto_com_mocking(mock_vincular_produto, produto_vinculado):
    firebase = VincularProdutosFirebase()

    # Executa o método que será testado
    firebase.vincular_produto(produto_vinculado)

    # Verifica se foi chamado exatamente uma vez com o produto correto
    mock_vincular_produto.assert_called_once_with(produto_vinculado)

if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
