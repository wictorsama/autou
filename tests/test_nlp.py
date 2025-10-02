import pytest
from app.nlp import classify_email, preprocess


def test_preprocess_text():
    """Testa o pré-processamento de texto."""
    text = "Olá, como está? Preciso de uma informação sobre o processo."
    processed = preprocess(text)
    
    # Verifica se o texto foi processado (removeu stopwords)
    assert isinstance(processed, str)
    assert len(processed) > 0
    # Stopwords como "como", "de", "o" devem ser removidas
    assert "como" not in processed.lower()
    assert "preciso informação processo" in processed.lower()


def test_classify_email_productive():
    """Testa classificação de e-mail produtivo."""
    text = "Preciso do status do chamado número 12345. Quando será resolvido?"
    result = classify_email(text)
    
    assert "category" in result
    assert "intent" in result
    assert "category_score" in result
    assert "intent_score" in result
    
    # Verifica tipos de dados
    assert isinstance(result["category"], str)
    assert isinstance(result["intent"], str)
    assert isinstance(result["category_score"], float)
    assert isinstance(result["intent_score"], float)
    
    # Verifica se as pontuações estão no intervalo válido
    assert 0 <= result["category_score"] <= 1
    assert 0 <= result["intent_score"] <= 1
    
    # Verifica se a categoria está nas opções válidas
    assert result["category"] in ["Produtivo", "Improdutivo"]


def test_classify_email_unproductive():
    """Testa classificação de e-mail improdutivo."""
    text = "Parabéns pelo excelente trabalho! Feliz aniversário para toda equipe!"
    result = classify_email(text)
    
    assert "category" in result
    assert "intent" in result
    assert "category_score" in result
    assert "intent_score" in result
    
    # Verifica se a categoria está nas opções válidas
    assert result["category"] in ["Produtivo", "Improdutivo"]


def test_classify_empty_text():
    """Testa classificação com texto vazio."""
    with pytest.raises(ValueError):
        classify_email("")


def test_classify_none_text():
    """Testa classificação com texto None."""
    with pytest.raises(ValueError):
        classify_email(None)


def test_classify_very_short_text():
    """Testa classificação com texto muito curto."""
    result = classify_email("Ok")
    
    # Mesmo com texto curto, deve retornar uma classificação válida
    assert "category" in result
    assert result["category"] in ["Produtivo", "Improdutivo"]


def test_classify_long_text():
    """Testa classificação com texto longo."""
    long_text = """Prezados,
    
    Espero que estejam bem. Gostaria de solicitar informações sobre o andamento 
    do meu processo número 98765. Já faz algumas semanas que enviei a documentação 
    solicitada e gostaria de saber se há alguma pendência ou se preciso enviar 
    algum documento adicional. 
    
    Agradeço desde já pela atenção e aguardo retorno.
    
    Atenciosamente,
    João Silva
    """
    
    result = classify_email(long_text)
    
    assert "category" in result
    assert "intent" in result
    assert result["category"] in ["Produtivo", "Improdutivo"]