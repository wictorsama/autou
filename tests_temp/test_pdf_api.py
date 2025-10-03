import requests
import json

# URL da API
url = "http://127.0.0.1:8000/api/process"

# Abrir e enviar o arquivo PDF
with open('test_email.pdf', 'rb') as f:
    files = {'file': ('test_email.pdf', f, 'application/pdf')}
    
    try:
        response = requests.post(url, files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Teste com PDF realizado com sucesso!")
            print("\n📄 Resultado da classificação:")
            print(f"Categoria: {result.get('category', 'N/A')}")
            print(f"Intenção: {result.get('intent', 'N/A')}")
            print(f"Confiança: {result.get('confidence', 'N/A')}")
            print(f"Resposta sugerida: {result.get('suggested_reply', 'N/A')}")
            
            if 'extracted_text' in result:
                print(f"\n📝 Texto extraído do PDF:")
                print(result['extracted_text'][:200] + "..." if len(result['extracted_text']) > 200 else result['extracted_text'])
        else:
            print(f"❌ Erro na requisição: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor. Verifique se a API está rodando.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")