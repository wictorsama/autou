import pytest
import tempfile
import os
from app.utils import read_text_from_file


def test_read_txt_file():
    """Testa leitura de arquivo .txt simples."""
    test_content = "Este é um teste de conteúdo em português."
    content_bytes = test_content.encode('utf-8')
    
    text, mime_type = read_text_from_file("test.txt", content_bytes)
    assert text == test_content
    assert mime_type == "text/plain"


def test_read_txt_file_with_encoding():
    """Testa leitura de arquivo .txt com caracteres especiais."""
    test_content = "Conteúdo com acentuação: ção, ã, é, ü"
    content_bytes = test_content.encode('utf-8')
    
    text, mime_type = read_text_from_file("test.txt", content_bytes)
    assert text == test_content
    assert mime_type == "text/plain"
    assert "ção" in text
    assert "ã" in text


def test_read_unsupported_file_type():
    """Testa leitura de tipo de arquivo não suportado."""
    content_bytes = b"conteudo"
    
    with pytest.raises(ValueError, match="Formato de arquivo não suportado"):
        read_text_from_file("arquivo.xyz", content_bytes)


def test_read_empty_txt_file():
    """Testa leitura de arquivo .txt vazio."""
    content_bytes = b""
    
    text, mime_type = read_text_from_file("empty.txt", content_bytes)
    assert text == ""
    assert mime_type == "text/plain"


def test_read_txt_file_multiline():
    """Testa leitura de arquivo .txt com múltiplas linhas."""
    multiline_content = """Linha 1
Linha 2 com acentos: ção
Linha 3

Linha 5 (linha 4 vazia)
Última linha"""
    content_bytes = multiline_content.encode('utf-8')
    
    text, mime_type = read_text_from_file("multiline.txt", content_bytes)
    assert text == multiline_content
    assert mime_type == "text/plain"
    lines = text.split('\n')
    assert len(lines) == 6
    assert lines[0] == "Linha 1"
    assert lines[1] == "Linha 2 com acentos: ção"
    assert lines[3] == ""  # linha vazia


# Nota: Testes para PDF requerem criação de PDFs válidos,
# o que é mais complexo. Por simplicidade, testamos apenas
# o comportamento com arquivos .txt neste MVP.