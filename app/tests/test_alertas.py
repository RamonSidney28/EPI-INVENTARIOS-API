import pytest
from datetime import date, timedelta
from app.utils import check_vencimento_proximo, check_estoque_minimo

@pytest.mark.asyncio
async def test_check_vencimento_proximo(mock_db):
    """Teste de verificação de EPIs próximos do vencimento"""
    # Criar EPI com validade próxima
    epi_data = {
        "nome": "Máscara de Proteção",
        "categoria": "Proteção Respiratória",
        "quantidade_minima": 10,
        "quantidade_estoque": 30,
        "data_validade": str(date.today() + timedelta(days=15)),  # 15 dias - deve alertar
        "fornecedor": "Fornecedor ABC",
        "numero_certificacao": "CER901234"
    }
    
    await mock_db.epis.insert_one(epi_data)
    
    alertas = await check_vencimento_proximo(mock_db)
    assert len(alertas) > 0
    assert alertas[0]["nome"] == "Máscara de Proteção"

@pytest.mark.asyncio
async def test_check_estoque_minimo(mock_db):
    """Teste de verificação de estoque mínimo"""
    # Criar EPI com estoque abaixo do mínimo
    epi_data = {
        "nome": "Protetor Auricular",
        "categoria": "Proteção Auditiva",
        "quantidade_minima": 20,
        "quantidade_estoque": 5,  # Abaixo do mínimo - deve alertar
        "data_validade": str(date.today() + timedelta(days=365)),
        "fornecedor": "Fornecedor XYZ",
        "numero_certificacao": "CER567890"
    }
    
    await mock_db.epis.insert_one(epi_data)
    
    alertas = await check_estoque_minimo(mock_db)
    assert len(alertas) > 0
    assert alertas[0]["nome"] == "Protetor Auricular"
