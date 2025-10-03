import requests
import json

# URL da API
url = "http://127.0.0.1:8000/api/process"

# Diferentes tipos de mensagens promocionais para testar
textos_teste = [
    "Promoção de 12 computadores por 1 LEVANDO SO HOJE!",
    "Oferta imperdível! Desconto de 50% apenas hoje!",
    "Não perca esta oportunidade única! Clique aqui!",
    "Mega liquidação! Aproveite enquanto há tempo!",
    "Parabéns! Você ganhou um prêmio incrível!",
    "Prezado cliente, segue em anexo o relatório solicitado.",
    "Obrigado pela reunião de hoje. Foi muito produtiva!",
    "Preciso de ajuda com o sistema. Não consigo acessar."
]

print("🔍 Testando múltiplos tipos de mensagens:\n")

for i, texto in enumerate(textos_teste, 1):
    try:
        data = {'text': texto}
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            result = response.json()
            categoria = result.get('category', 'N/A')
            intencao = result.get('intent', 'N/A')
            
            # Emoji baseado na categoria
            emoji = "✅" if categoria == "Improdutivo" and ("spam" in intencao.lower() or "marketing" in intencao.lower() or "felicitação" in intencao.lower()) else "⚠️" if categoria == "Produtivo" else "✅"
            
            print(f"{i}. {emoji} {texto[:50]}...")
            print(f"   Categoria: {categoria} | Intenção: {intencao}")
            print()
            
        else:
            print(f"{i}. ❌ Erro na requisição: {response.status_code}")
            
    except Exception as e:
        print(f"{i}. ❌ Erro: {e}")

print("\n📊 Legenda:")
print("✅ = Classificação correta")
print("⚠️ = Possível problema na classificação")