import io
from typing import Tuple
from pdfminer.high_level import extract_text

ALLOWED_EXTS = {".txt", ".pdf"}


def read_text_from_file(filename: str, content: bytes) -> Tuple[str, str]:
    """Lê texto de um arquivo .txt ou .pdf.
    
    Args:
        filename: Nome do arquivo
        content: Conteúdo do arquivo em bytes
        
    Returns:
        Tuple com (texto_extraído, tipo_mime)
        
    Raises:
        ValueError: Se o formato do arquivo não for suportado
    """
    name = filename or ""
    lower = name.lower()
    text = ""

    if lower.endswith(".txt"):
        text = content.decode("utf-8", errors="ignore")
        return text, "text/plain"
    if lower.endswith(".pdf"):
        # pdfminer precisa de um buffer
        with io.BytesIO(content) as pdf_buf:
            text = extract_text(pdf_buf) or ""
        return text, "application/pdf"
    raise ValueError("Formato de arquivo não suportado. Use .txt ou .pdf.")