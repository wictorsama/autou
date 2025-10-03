# Arquivos de Teste Temporários

Esta pasta contém arquivos de teste criados durante o desenvolvimento e demonstração do sistema AutoU.

## 📁 Conteúdo

### Arquivos de Teste de Email
- **`test_email.txt`** - Email de exemplo em formato texto
- **`test_email.pdf`** - Email de exemplo em formato PDF

### Scripts de Teste da API
- **`test_pdf_api.py`** - Testa processamento de arquivos PDF via API
- **`test_txt_api.py`** - Testa processamento de arquivos TXT via API
- **`test_promocao.py`** - Testa classificação de mensagens promocionais
- **`test_multiplos_spam.py`** - Testa múltiplos tipos de mensagens spam/promocionais

### Utilitários
- **`create_test_pdf.py`** - Script para gerar arquivos PDF de teste

## 🚀 Como Usar

### Executar Testes Individuais
```bash
# Testar processamento de PDF
py tests_temp/test_pdf_api.py

# Testar processamento de TXT
py tests_temp/test_txt_api.py

# Testar detecção de spam
py tests_temp/test_promocao.py

# Testar múltiplos tipos de mensagem
py tests_temp/test_multiplos_spam.py
```

### Gerar Novos PDFs de Teste
```bash
py tests_temp/create_test_pdf.py
```

## ⚠️ Nota

Estes arquivos são para **desenvolvimento e teste apenas**. Eles não são incluídos no build de produção (configurado no `.dockerignore`).

## 🧹 Limpeza

Para remover todos os arquivos de teste:
```bash
# Windows
rmdir /s tests_temp

# Linux/Mac
rm -rf tests_temp
```