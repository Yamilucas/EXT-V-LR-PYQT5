import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Garante que o Python enxergue a raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controller.Referencias_firebase.Cadastro_Empresas_firebase import CadastroEmpresaFirebase
from model.model_empresas import Empresa

@pytest.fixture
def empresa_valida():
    empresa = MagicMock(spec=Empresa)
    empresa.get_nome_empresa.return_value = "Empresa Nova"
    empresa.get_logo.return_value = "logo_base64_nova"
    return empresa

@patch('controller.Referencias_firebase.Cadastro_Empresas_firebase.db')
def test_salvar_empresa_com_sucesso(mock_db, empresa_valida):
    # Mocks para simular Firebase
    mock_ref = MagicMock()
    mock_ref.get.return_value = {}  # Nenhuma empresa cadastrada
    mock_nova_ref = MagicMock()
    mock_ref.push.return_value = mock_nova_ref

    mock_db.reference.return_value = mock_ref

    # Executa
    controller = CadastroEmpresaFirebase()
    resultado = controller.salvar_empresa(empresa_valida)

    # Verificações
    assert resultado is True
    mock_ref.push.assert_called_once()
    mock_nova_ref.set.assert_called_once()


if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))