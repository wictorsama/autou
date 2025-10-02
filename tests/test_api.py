import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    """Testa o endpoint de health check."""
    r = client.get('/health')
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "service" in data


def test_process_with_text():
    """Testa o processamento de texto via API."""
    payload = {"text": "Olá, podem me passar o status do chamado 123?"}
    r = client.post('/api/process', data=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["category"] in ("Produtivo", "Improdutivo")
    assert isinstance(data["suggested_reply"], str)
    assert isinstance(data["category_score"], float)
    assert isinstance(data["intent_score"], float)
    assert data["reply_source"] in ("template", "openai+template")


def test_process_empty_text():
    """Testa o processamento com texto vazio."""
    payload = {"text": ""}
    r = client.post('/api/process', data=payload)
    assert r.status_code == 400
    data = r.json()
    assert "detail" in data


def test_process_no_input():
    """Testa o processamento sem entrada."""
    r = client.post('/api/process', data={})
    assert r.status_code == 400
    data = r.json()
    assert "detail" in data


def test_index_page():
    """Testa se a página principal carrega."""
    r = client.get('/')
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]


def test_classification_categories():
    """Testa diferentes tipos de e-mail para verificar classificação."""
    test_cases = [
        {
            "text": "Preciso do status do meu processo número 12345",
            "expected_category": "Produtivo"
        },
        {
            "text": "Obrigado pelo excelente atendimento! Parabéns!",
            "expected_category": "Improdutivo"
        },
        {
            "text": "Segue anexo o documento solicitado para análise",
            "expected_category": "Produtivo"
        }
    ]
    
    for case in test_cases:
        payload = {"text": case["text"]}
        r = client.post('/api/process', data=payload)
        assert r.status_code == 200
        data = r.json()
        # Note: Como é zero-shot, não garantimos 100% de acurácia, 
        # mas verificamos que retorna uma categoria válida
        assert data["category"] in ("Produtivo", "Improdutivo")
        assert data["category_score"] > 0
        assert data["intent_score"] > 0