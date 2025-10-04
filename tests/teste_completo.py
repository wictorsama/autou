#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste completo para validar todas as funcionalidades
antes do deploy no Render.
"""

import requests
import json
import os
from pathlib import Path

# Configurações
BASE_URL = "http://localhost:8000"
EXEMPLOS_DIR = Path("../exemplos_teste")

# Exemplos esperados
EXPECTED_RESULTS = {
    "exemplo_status.txt": {
        "categoria": "Produtivo",
        "intencao": "Solicitação de status ou acompanhamento",
        "keywords": ["status", "chamado"]
    },
    "exemplo_reuniao.txt": {
        "categoria": "Produtivo", 
        "intencao": "Agendamento de reunião ou compromisso",
        "keywords": ["agendar", "reunião", "disponibilidade"]
    },
    "exemplo_aprovacao.txt": {
        "categoria": "Produtivo",
        "intencao": "Aprovação ou autorização necessária",
        "keywords": ["aprovação", "autorizar"]
    },
    "exemplo_orcamento.txt": {
        "categoria": "Produtivo",
        "intencao": "Solicitação de orçamento ou proposta",
        "keywords": ["orçamento", "proposta"]
    },
    "exemplo_convite.txt": {
        "categoria": "Improdutivo",
        "intencao": "Convite para evento ou treinamento",
        "keywords": ["convite", "workshop"]
    },
    "exemplo_notificacao.txt": {
        "categoria": "Improdutivo",
        "intencao": "Notificação automática do sistema",
        "keywords": ["notificação", "automática", "senha"]
    }
}

def test_health_endpoint():
    """Testa se o servidor está funcionando."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check falhou: {e}")
        return False

def test_classification(filename, content):
    """Testa a classificação de um email."""
    try:
        response = requests.post(
            f"{BASE_URL}/api/process",
            data={"text": content}
        )
        
        if response.status_code == 200:
            result = response.json()
            expected = EXPECTED_RESULTS.get(filename, {})
            
            print(f"\n📧 Testando: {filename}")
            print(f"   Resposta completa: {result}")
            print(f"   Categoria: {result.get('category')} (esperado: {expected.get('categoria')})")
            print(f"   Intenção: {result.get('intent')} (esperado: {expected.get('intencao')})")
            print(f"   Confiança: {result.get('category_score', 0):.2f}")
            
            # Verificar se a classificação está correta
            categoria_ok = result.get('category') == expected.get('categoria')
            intencao_ok = result.get('intent') == expected.get('intencao')
            
            if categoria_ok and intencao_ok:
                print(f"   ✅ Classificação correta")
                return True
            else:
                print(f"   ❌ Classificação incorreta")
                return False
        else:
            print(f"❌ Erro na classificação de {filename}: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar {filename}: {e}")
        return False

def main():
    """Executa todos os testes."""
    print("🚀 Iniciando testes completos da aplicação...\n")
    
    # Teste 1: Health check
    if not test_health_endpoint():
        print("❌ Servidor não está funcionando. Abortando testes.")
        return
    
    # Teste 2: Classificações
    total_tests = 0
    passed_tests = 0
    
    for filename in EXPECTED_RESULTS.keys():
        filepath = EXEMPLOS_DIR / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            total_tests += 1
            if test_classification(filename, content):
                passed_tests += 1
        else:
            print(f"⚠️  Arquivo não encontrado: {filename}")
    
    # Resultado final
    print(f"\n📊 Resultado dos testes:")
    print(f"   Total: {total_tests}")
    print(f"   Passou: {passed_tests}")
    print(f"   Falhou: {total_tests - passed_tests}")
    print(f"   Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 Todos os testes passaram! Aplicação pronta para deploy.")
    else:
        print("\n⚠️  Alguns testes falharam. Revisar antes do deploy.")

if __name__ == "__main__":
    main()