import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest import mock
import firebase_admin
from firebase_admin import db
from controller.Conexao import inicializar_firebase

# Teste 1: Verificar se a inicialização ocorre sem erro
def test_inicializar_firebase_sucesso(monkeypatch):
    # Garantir que _apps está vazio
    monkeypatch.setattr(firebase_admin, '_apps', {})

    # Mockar funções necessárias
    monkeypatch.setattr(firebase_admin, 'initialize_app', mock.Mock())
    monkeypatch.setattr(db, 'reference', lambda path: mock.Mock(get=lambda: {}))

    resultado = inicializar_firebase()
    assert resultado == True

# Teste 2: Verificar se a inicialização trata erro corretamente
def test_inicializar_firebase_erro(monkeypatch):
    # Garantir que _apps está vazio
    monkeypatch.setattr(firebase_admin, '_apps', {})

    # Mockar initialize_app para simular erro
    monkeypatch.setattr(firebase_admin, 'initialize_app', mock.Mock(side_effect=Exception("Falha ao conectar")))
    
    resultado = inicializar_firebase()
    assert resultado == False

# Teste 3: Verificar se NÃO reinicializa se já tem app
def test_inicializar_firebase_nao_reinicializa(monkeypatch):
    # Simular que já existe uma conexão inicializada
    monkeypatch.setattr(firebase_admin, '_apps', {'algum_app': True})

    # Criar mocks
    mock_inicializar = mock.Mock()
    ref_mock = mock.Mock()
    get_mock = mock.Mock(return_value={})
    ref_mock.get = get_mock

    monkeypatch.setattr(firebase_admin, 'initialize_app', mock_inicializar)
    monkeypatch.setattr(db, 'reference', lambda path: ref_mock)

    resultado = inicializar_firebase()

    # initialize_app NÃO deve ser chamado
    mock_inicializar.assert_not_called()
    assert resultado == True


if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
