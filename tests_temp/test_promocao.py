import requests
import json

# URL da API
url = "http://127.0.0.1:8000/api/process"

# Texto promocional para testar
texto_promocional = "Promoção de 12 computadores por 1 LEVANDO SO HOJE!"

try:
    # Enviar requisição
    data = {'text': texto_promocional}
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        result = response.json()
        print("\n📄 Resultado da classificação:")
        print(f"Texto: {texto_promocional}")
        print(f"Categoria: {result.get('category', 'N/A')}")
        print(f"Intenção: {result.get('intent', 'N/A')}")
        print(f"Confiança: {result.get('confidence', 'N/A')}")
        print(f"\nResposta sugerida:")
        print(result.get('suggested_reply', 'N/A'))
        
        # Análise do resultado
        if result.get('category') == 'Produtivo':
            print("\n⚠️  ATENÇÃO: Mensagem promocional foi classificada como PRODUTIVA!")
            print("Isso pode indicar um problema na classificação.")
        else:
            print("\n✅ Classificação correta: Mensagem promocional identificada como improdutiva.")
            
    else:
        print(f"❌ Erro na requisição: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Erro: {e}")