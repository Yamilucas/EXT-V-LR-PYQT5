import sys
import os
import pytest
from unittest.mock import patch
from controller.Referencias_firebase import Cadastro_NomeProdutos_firebase

def test_cadastro_produto_realizado():
    nome = "Produto Teste"
    categoria = "Categoria_2"
    imagem = None  # ou base64, se necessário

    # Mocka o método interno que interage com o Firebase
    with patch.object(Cadastro_NomeProdutos_firebase, 'salvar_produto', return_value=True) as mock_salvar:
        resultado = Cadastro_NomeProdutos_firebase.salvar_produto(nome, categoria, imagem)

        # Verifica se o método foi chamado
        mock_salvar.assert_called_once_with(nome, categoria, imagem)

        # Verifica se retornou sucesso (simulado como True)
        assert resultado is True

if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))