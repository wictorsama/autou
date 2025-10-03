import requests
import json

# URL da API
url = "http://127.0.0.1:8000/api/process"

# Testar arquivo TXT
with open('test_email.txt', 'rb') as f:
    files = {'file': ('test_email.txt', f, 'text/plain')}
    
    try:
        response = requests.post(url, files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Teste com TXT realizado com sucesso!")
            print("\n📄 Resultado da classificação (TXT):")
            print(f"Categoria: {result.get('category', 'N/A')}")
            print(f"Intenção: {result.get('intent', 'N/A')}")
            print(f"Confiança: {result.get('confidence', 'N/A')}")
        else:
            print(f"❌ Erro na requisição: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Erro: {e}")