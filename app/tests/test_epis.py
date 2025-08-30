import pytest
from datetime import date, timedelta
from app.schemas import EpiCreate, EpiResponse

def test_epi_schema_validation():
    """Teste de validação do schema de EPI"""
    # Teste de dados válidos
    valid_data = {
        "nome": "Óculos de Proteção",
        "categoria": "Proteção Ocular",
        "quantidade_minima": 10,
        "quantidade_estoque": 50,
        "data_validade": str(date.today() + timedelta(days=365)),
        "fornecedor": "Fornecedor ABC",
        "numero_certificacao": "CER123456"
    }
    
    epi = EpiCreate(**valid_data)
    assert epi.nome == "Óculos de Proteção"
    assert epi.quantidade_minima == 10

def test_epi_schema_validation_invalid():
    """Teste de validação com dados inválidos"""
    invalid_data = {
        "nome": "Óculos de Proteção",
        "categoria": "Proteção Ocular",
        "quantidade_minima": -5,  # Quantidade negativa - deve falhar
        "quantidade_estoque": 50,
        "data_validade": "2023-01-01",  # Data no passado - deve falhar
        "fornecedor": "Fornecedor ABC",
        "numero_certificacao": "CER123456"
    }
    
    with pytest.raises(ValueError):
        EpiCreate(**invalid_data)

@pytest.mark.asyncio
async def test_criar_epi(client, mock_db):
    """Teste de criação de EPI"""
    epi_data = {
        "nome": "Luvas de Proteção",
        "categoria": "Proteção de Mãos",
        "quantidade_minima": 20,
        "quantidade_estoque": 100,
        "data_validade": str(date.today() + timedelta(days=180)),
        "fornecedor": "Fornecedor XYZ",
        "numero_certificacao": "CER789012"
    }
    
    response = client.post("/epis/", json=epi_data)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == epi_data["nome"]
    assert data["quantidade_estoque"] == epi_data["quantidade_estoque"]
    assert "id" in data

@pytest.mark.asyncio
async def test_listar_epis(client, mock_db):
    """Teste de listagem de EPIs"""
    # Primeiro cria alguns EPIs
    epi_data = {
        "nome": "Capacete de Segurança",
        "categoria": "Proteção da Cabeça",
        "quantidade_minima": 15,
        "quantidade_estoque": 45,
        "data_validade": str(date.today() + timedelta(days=365)),
        "fornecedor": "Fornecedor ABC",
        "numero_certificacao": "CER345678"
    }
    
    await client.post("/epis/", json=epi_data)
    
    # Agora lista
    response = client.get("/epis/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
