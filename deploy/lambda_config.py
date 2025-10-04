#!/usr/bin/env python3
"""
Configurações específicas para AWS Lambda
Otimizações de memória e performance
"""

import os
import gc
import psutil
from functools import lru_cache
from typing import Optional

class LambdaConfig:
    """Configurações otimizadas para AWS Lambda"""
    
    def __init__(self):
        self.is_lambda = os.environ.get('AWS_LAMBDA_FUNCTION_NAME') is not None
        self.memory_limit = int(os.environ.get('AWS_LAMBDA_FUNCTION_MEMORY_SIZE', '3008'))
        
    @property
    def max_memory_mb(self) -> int:
        """Limite máximo de memória em MB"""
        return self.memory_limit
    
    @property
    def safe_memory_threshold(self) -> float:
        """Limite seguro de uso de memória (80% do total)"""
        return self.memory_limit * 0.8
    
    @property
    def critical_memory_threshold(self) -> float:
        """Limite crítico de uso de memória (90% do total)"""
        return self.memory_limit * 0.9
    
    def get_memory_usage(self) -> dict:
        """Retorna informações de uso de memória"""
        if self.is_lambda:
            # No Lambda, usar informações do sistema
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
            
            mem_total = 0
            mem_available = 0
            
            for line in meminfo.split('\n'):
                if 'MemTotal:' in line:
                    mem_total = int(line.split()[1]) // 1024  # KB para MB
                elif 'MemAvailable:' in line:
                    mem_available = int(line.split()[1]) // 1024  # KB para MB
            
            mem_used = mem_total - mem_available
            
            return {
                'total_mb': mem_total,
                'used_mb': mem_used,
                'available_mb': mem_available,
                'usage_percent': (mem_used / mem_total) * 100 if mem_total > 0 else 0
            }
        else:
            # Desenvolvimento local
            memory = psutil.virtual_memory()
            return {
                'total_mb': memory.total // (1024 * 1024),
                'used_mb': memory.used // (1024 * 1024),
                'available_mb': memory.available // (1024 * 1024),
                'usage_percent': memory.percent
            }
    
    def should_cleanup_memory(self) -> bool:
        """Verifica se deve fazer limpeza de memória"""
        memory_info = self.get_memory_usage()
        return memory_info['used_mb'] > self.safe_memory_threshold
    
    def force_cleanup_memory(self):
        """Força limpeza de memória"""
        gc.collect()
        
        # Limpar caches específicos se existirem
        if hasattr(self, '_model_cache'):
            self._model_cache.clear()
        
        # Forçar garbage collection múltiplas vezes
        for _ in range(3):
            gc.collect()

# Configurações específicas para diferentes modelos
MODEL_CONFIGS = {
    'openai': {
        'max_tokens': 1000,
        'temperature': 0.1,
        'timeout': 25,  # Deixar 5s de margem para o Lambda
        'max_retries': 1
    },
    'transformers': {
        'max_length': 512,
        'truncation': True,
        'padding': True,
        'device': 'cpu',  # Lambda não tem GPU
        'torch_dtype': 'float32'  # Mais compatível
    }
}

# Configurações de cache otimizadas para Lambda
CACHE_CONFIG = {
    'maxsize': 50,  # Reduzido para economizar memória
    'ttl': 300,     # 5 minutos
    'cleanup_interval': 60  # Limpeza a cada minuto
}

# Configurações de logging para Lambda
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '[%(levelname)s] %(asctime)s - %(name)s - %(message)s',
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'uvicorn': {'level': 'WARNING'},
        'transformers': {'level': 'WARNING'},
        'torch': {'level': 'WARNING'}
    }
}

# Configurações de timeout
TIMEOUT_CONFIG = {
    'classification': 20,  # 20 segundos para classificação
    'suggestion': 15,      # 15 segundos para sugestão
    'file_processing': 10, # 10 segundos para processar arquivo
    'total_request': 25    # 25 segundos total (5s de margem)
}

# Otimizações específicas para cold start
COLD_START_OPTIMIZATIONS = {
    'preload_models': False,  # Não pré-carregar modelos (economiza memória)
    'lazy_imports': True,     # Importações sob demanda
    'cache_tokenizers': True, # Cache de tokenizers
    'optimize_torch': True    # Otimizações do PyTorch
}

def optimize_for_lambda():
    """Aplica otimizações específicas para Lambda"""
    if os.environ.get('AWS_LAMBDA_FUNCTION_NAME'):
        # Configurar PyTorch para CPU
        os.environ['OMP_NUM_THREADS'] = '1'
        os.environ['MKL_NUM_THREADS'] = '1'
        os.environ['NUMEXPR_NUM_THREADS'] = '1'
        
        # Desabilitar paralelização desnecessária
        os.environ['TOKENIZERS_PARALLELISM'] = 'false'
        
        # Configurar garbage collection mais agressivo
        gc.set_threshold(100, 10, 10)
        
        print("🔧 Otimizações Lambda aplicadas")

def get_lambda_config() -> LambdaConfig:
    """Retorna configuração singleton para Lambda"""
    if not hasattr(get_lambda_config, '_instance'):
        get_lambda_config._instance = LambdaConfig()
    return get_lambda_config._instance

# Decorator para monitoramento de memória
def monitor_memory(func):
    """Decorator para monitorar uso de memória"""
    def wrapper(*args, **kwargs):
        config = get_lambda_config()
        
        # Memória antes
        mem_before = config.get_memory_usage()
        
        try:
            result = func(*args, **kwargs)
            
            # Memória depois
            mem_after = config.get_memory_usage()
            
            # Log se uso aumentou significativamente
            mem_diff = mem_after['used_mb'] - mem_before['used_mb']
            if mem_diff > 100:  # Mais de 100MB
                print(f"⚠️ Função {func.__name__} usou {mem_diff:.1f}MB adicionais")
            
            # Cleanup se necessário
            if config.should_cleanup_memory():
                print(f"🧹 Limpeza de memória ativada ({mem_after['used_mb']:.1f}MB usados)")
                config.force_cleanup_memory()
            
            return result
            
        except Exception as e:
            # Cleanup em caso de erro
            config.force_cleanup_memory()
            raise e
    
    return wrapper

# Aplicar otimizações na importação
optimize_for_lambda()