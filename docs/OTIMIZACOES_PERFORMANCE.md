# Otimizações de Memória - AutoU Email Classifier

## Resumo das Otimizações Implementadas

Este documento descreve as otimizações de memória implementadas para melhorar a performance da aplicação em ambientes de produção.

## 1. Configurações Centralizadas

### Arquivo: `app/config.py`
- Configurações centralizadas para limites de memória
- Monitoramento de uso de memória com `psutil`
- Configurações flexíveis via variáveis de ambiente

### Principais Configurações:
- `MAX_FILE_SIZE`: 5MB (reduzido)
- `MAX_CHARS`: 10.000 caracteres (reduzido de 20.000)
- `MAX_PDF_SIZE`: 10MB para PDFs
- `GC_THRESHOLD`: Limpeza automática a cada 100 operações

## 2. Otimizações no Processamento de Arquivos

### Arquivo: `app/utils.py`
- Verificação de tamanho antes do processamento
- Limpeza explícita de buffers PDF
- Limitação de texto extraído (50.000 caracteres)
- Tratamento de erro robusto com limpeza de memória

## 3. Otimizações no Modelo NLP

### Arquivo: `app/nlp.py`
- Modelo principal otimizado: `facebook/bart-large-mnli`
- Modelo fallback menor: `typeform/distilbert-base-uncased-mnli`
- Limpeza de memória após carregamento e classificação
- Tratamento de erro com fallback automático

## 4. Limpeza Automática de Memória

### Arquivo: `app/main.py`
- Função `cleanup_memory()` para limpeza automática
- Contador de operações para trigger de limpeza
- Monitoramento de memória no endpoint `/health`
- Limpeza após cada processamento de arquivo

## 5. Dependências Otimizadas

### Arquivo: `requirements.txt`
- Versões específicas para evitar atualizações problemáticas
- Remoção da dependência `openai` não utilizada
- Adição do `psutil` para monitoramento
- Versões otimizadas do PyTorch e Transformers

## 6. Monitoramento de Memória

### Endpoint `/health`
Agora retorna informações de memória:
```json
{
  "status": "ok",
  "service": "AutoU Email Classifier",
  "memory": {
    "rss": 150.5,
    "vms": 300.2,
    "percent": 12.3,
    "available": 1024.0
  }
}
```

## 7. Variáveis de Ambiente

Para configurar em produção:

```bash
# Limites de arquivo
MAX_FILE_SIZE=5242880  # 5MB
MAX_CHARS=10000
MAX_PDF_SIZE=10485760  # 10MB

# Configurações de memória
ENABLE_MEMORY_CLEANUP=true
GC_THRESHOLD=50  # Mais agressivo em produção

# Modelo NLP (opcional)
ZSL_MODEL=typeform/distilbert-base-uncased-mnli  # Usar modelo menor

# Logging
LOG_LEVEL=INFO
```

## 8. Benefícios Esperados

1. **Redução de 40-60% no uso de memória**
2. **Prevenção de vazamentos de memória**
3. **Processamento mais estável**
4. **Monitoramento em tempo real**
5. **Recuperação automática de erros**

## 9. Próximos Passos

1. Testar em ambiente de produção
2. Monitorar métricas de memória
3. Ajustar `GC_THRESHOLD` conforme necessário
4. Considerar cache de modelo se necessário

## 10. Troubleshooting

### Se ainda houver problemas de memória:
1. Reduzir `MAX_CHARS` para 5000
2. Usar apenas o modelo fallback menor
3. Reduzir `GC_THRESHOLD` para 25
4. Aumentar os recursos da instância se possível