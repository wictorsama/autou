import io
import gc
from typing import Tuple
from pdfminer.high_level import extract_text
from .config import Config

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
    
    try:
        if lower.endswith(".txt"):
            # Verificar se o conteúdo não é muito grande
            if len(content) > Config.MAX_PDF_SIZE:
                raise ValueError(f"Arquivo TXT muito grande. Máximo: {Config.MAX_PDF_SIZE // (1024*1024)}MB")
            
            text = content.decode("utf-8", errors="ignore")
            return text, "text/plain"
            
        elif lower.endswith(".pdf"):
            # Verificar tamanho do PDF
            if len(content) > Config.MAX_PDF_SIZE:
                raise ValueError(f"Arquivo PDF muito grande. Máximo: {Config.MAX_PDF_SIZE // (1024*1024)}MB")
            
            # Processar PDF com limpeza de memória
            pdf_buf = None
            try:
                pdf_buf = io.BytesIO(content)
                text = extract_text(pdf_buf) or ""
                
                # Limitar tamanho do texto extraído
                if len(text) > 50000:  # 50k caracteres máximo
                    text = text[:50000]
                    
            finally:
                if pdf_buf:
                    pdf_buf.close()
                pdf_buf = None
                gc.collect()
                
            return text, "application/pdf"
            
        else:
            raise ValueError("Formato de arquivo não suportado. Use .txt ou .pdf.")
            
    except Exception as e:
        # Limpeza em caso de erro
        gc.collect()
        raise e