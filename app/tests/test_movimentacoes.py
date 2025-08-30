import pytest
from datetime import date, timedelta

@pytest.mark.asyncio
async def test_movimentacao_entrada(client, mock_db):
    """Teste de entrada no estoque"""
    # Primeiro cria um EPI
    epi_data = {
        "nome": "Luvas de Proteção",
        "categoria": "Proteção de Mãos",
        "quantidade_minima": 20,
        "quantidade_estoque": 50,
        "data_validade": str(date.today() + timedelta(days=180)),
        "fornecedor": "Fornecedor XYZ",
        "numero_certificacao": "CER789012"
    }
    
    create_response = await client.post("/epis/", json=epi_data)
    epi_id = create_response.json()["id"]
    
    # Agora faz uma entrada
    entrada_data = {
        "epi_id": epi_id,
        "quantidade": 25,
        "numero_lote": "LOTE202401",
        "motivo": "Compra mensal"
    }
    
    response = await client.post("/movimentacoes/entrada", json=entrada_data)
    assert response.status_code == 200
    
    # Verifica se o estoque foi atualizado
    epi_response = await client.get(f"/epis/{epi_id}")
    assert epi_response.json()["quantidade_estoque"] == 75

@pytest.mark.asyncio
async def test_movimentacao_saida(client, mock_db):
    """Teste de saída do estoque"""
    # Primeiro cria um EPI
    epi_data = {
        "nome": "Óculos de Proteção",
        "categoria": "Proteção Ocular",
        "quantidade_minima": 10,
        "quantidade_estoque": 50,
        "data_validade": str(date.today() + timedelta(days=365)),
        "fornecedor": "Fornecedor ABC",
        "numero_certificacao": "CER123456"
    }
    
    create_response = await client.post("/epis/", json=epi_data)
    epi_id = create_response.json()["id"]
    
    # Agora faz uma saída
    saida_data = {
        "epi_id": epi_id,
        "quantidade": 15,
        "motivo": "Distribuição para equipe",
        "destinatario": "João Silva"
    }
    
    response = await client.post("/movimentacoes/saida", json=saida_data)
    assert response.status_code == 200
    
    # Verifica se o estoque foi atualizado
    epi_response = await client.get(f"/epis/{epi_id}")
    assert epi_response.json()["quantidade_estoque"] == 35
