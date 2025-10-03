import os

# Configurações de memória e performance
class Config:
    # Limites de arquivo e texto
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 5 * 1024 * 1024))  # 5MB
    MAX_CHARS = int(os.getenv("MAX_CHARS", 10000))  # 10k caracteres
    MAX_PDF_SIZE = int(os.getenv("MAX_PDF_SIZE", 10 * 1024 * 1024))  # 10MB para PDFs
    
    # Configurações de modelo NLP
    ZSL_MODEL = os.getenv("ZSL_MODEL", "facebook/bart-large-mnli")
    ZSL_MODEL_FALLBACK = os.getenv("ZSL_MODEL_FALLBACK", "typeform/distilbert-base-uncased-mnli")
    
    # Configurações de servidor
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    # Configurações de memória
    ENABLE_MEMORY_CLEANUP = os.getenv("ENABLE_MEMORY_CLEANUP", "true").lower() == "true"
    GC_THRESHOLD = int(os.getenv("GC_THRESHOLD", 100))  # Força GC a cada N operações
    
    # Configurações de cache
    CACHE_MODEL = os.getenv("CACHE_MODEL", "true").lower() == "true"
    
    # Configurações de logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def get_memory_info(cls):
        """Retorna informações sobre uso de memória"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        return {
            "rss": memory_info.rss / 1024 / 1024,  # MB
            "vms": memory_info.vms / 1024 / 1024,  # MB
            "percent": process.memory_percent(),
            "available": psutil.virtual_memory().available / 1024 / 1024  # MB
        }