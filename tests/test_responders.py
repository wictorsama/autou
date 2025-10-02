import pytest
from unittest.mock import patch, MagicMock
from app.responders import suggest_reply


def test_suggest_reply_status():
    """Testa sugestão de resposta para solicitação de status."""
    classification = {
        "category": "Produtivo",
        "intent": "Solicitação de Status"
    }
    
    result = suggest_reply(classification)
    
    assert "reply" in result
    assert "source" in result
    assert isinstance(result["reply"], str)
    assert len(result["reply"]) > 0
    assert result["source"] in ["template", "openai+template"]
    
    # Verifica se contém elementos esperados para status
    reply_lower = result["reply"].lower()
    assert any(word in reply_lower for word in ["status", "andamento", "processo", "chamado"])


def test_suggest_reply_document():
    """Testa sugestão de resposta para envio de documento."""
    classification = {
        "category": "Produtivo", 
        "intent": "Envio de Documento"
    }
    
    result = suggest_reply(classification)
    
    assert "reply" in result
    assert "source" in result
    assert isinstance(result["reply"], str)
    assert len(result["reply"]) > 0
    
    # Verifica se contém elementos esperados para documento
    reply_lower = result["reply"].lower()
    assert any(word in reply_lower for word in ["documento", "recebido", "anexo", "análise"])


def test_suggest_reply_unproductive():
    """Testa sugestão de resposta para e-mail improdutivo."""
    classification = {
        "category": "Improdutivo",
        "intent": "Felicitação"
    }
    
    result = suggest_reply(classification)
    
    assert "reply" in result
    assert "source" in result
    assert isinstance(result["reply"], str)
    assert len(result["reply"]) > 0
    
    # Verifica se contém elementos esperados para felicitação
    reply_lower = result["reply"].lower()
    assert any(word in reply_lower for word in ["obrigado", "agradecemos", "feliz"])


def test_suggest_reply_unknown_intent():
    """Testa sugestão de resposta para intent desconhecido."""
    classification = {
        "category": "Produtivo",
        "intent": "Intent Inexistente"
    }
    
    result = suggest_reply(classification)
    
    assert "reply" in result
    assert "source" in result
    assert isinstance(result["reply"], str)
    assert len(result["reply"]) > 0
    
    # Deve usar template genérico
    reply_lower = result["reply"].lower()
    assert any(word in reply_lower for word in ["recebemos", "contato", "retorno"])


def test_suggest_reply_unknown_category():
    """Testa sugestão de resposta para categoria desconhecida."""
    classification = {
        "category": "Categoria Inexistente",
        "intent": "Solicitação de Status"
    }
    
    result = suggest_reply(classification)
    
    assert "reply" in result
    assert "source" in result
    assert isinstance(result["reply"], str)
    assert len(result["result"]) > 0


@patch('app.responders.openai')
def test_suggest_reply_with_openai(mock_openai):
    """Testa sugestão de resposta com OpenAI habilitado."""
    # Mock da resposta do OpenAI
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Resposta refinada pelo OpenAI"
    mock_openai.ChatCompletion.create.return_value = mock_response
    
    classification = {
        "category": "Produtivo",
        "intent": "Solicitação de Status"
    }
    
    # Simula que há API key configurada
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
        result = suggest_reply(classification)
    
    assert "reply" in result
    assert "source" in result
    assert result["source"] == "openai+template"
    assert "OpenAI" in result["reply"]


def test_suggest_reply_empty_classification():
    """Testa sugestão de resposta com classificação vazia."""
    classification = {}
    
    result = suggest_reply(classification)
    
    assert "reply" in result
    assert "source" in result
    assert isinstance(result["reply"], str)
    assert len(result["reply"]) > 0


def test_suggest_reply_none_classification():
    """Testa sugestão de resposta com classificação None."""
    with pytest.raises((TypeError, AttributeError)):
        suggest_reply(None)