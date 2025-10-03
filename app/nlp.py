import os
import gc
from typing import Dict, List
import nltk
from nltk.corpus import stopwords
from transformers import pipeline

# NLTK setup
nltk.download("stopwords", quiet=True)
STOP_PT = set(stopwords.words("portuguese"))

from .config import Config

# Lazy init (carrega uma vez)
_zsl_cls = None
_intent_cls = None

LABELS_CATEGORY = ["Email produtivo que requer ação", "Email improdutivo sem necessidade de ação"]
LABELS_INTENT = [
    "Solicitação de status ou informações",
    "Envio de documentos ou arquivos",
    "Dúvida técnica ou suporte",
    "Agradecimento ou felicitação",
    "Conversa informal ou social",
    "Spam ou marketing"
]


def get_classifier():
    """Retorna o classificador zero-shot, inicializando apenas uma vez."""
    global _zsl_cls
    if _zsl_cls is None:
        try:
            _zsl_cls = pipeline(
                 "zero-shot-classification",
                 model=Config.ZSL_MODEL,
                 return_all_scores=True,
                 device=-1,  # CPU
             )
         except Exception as e:
             print(f"Erro ao carregar modelo principal {Config.ZSL_MODEL}: {e}")
             print(f"Tentando modelo fallback: {Config.ZSL_MODEL_FALLBACK}")
             try:
                 _zsl_cls = pipeline(
                     "zero-shot-classification",
                     model=Config.ZSL_MODEL_FALLBACK,
                     return_all_scores=True,
                     device=-1,  # CPU
                 )
            except Exception as e2:
                print(f"Erro ao carregar modelo fallback: {e2}")
                raise e2
        finally:
            # Limpeza de memória após carregamento
            gc.collect()
    return _zsl_cls


def preprocess(text: str) -> str:
    """Pré-processa o texto removendo stopwords em português."""
    # minify
    text = (text or "").strip()
    # remove stopwords simples mantendo semântica
    tokens = [t for t in text.split() if t.lower() not in STOP_PT]
    return " ".join(tokens) if tokens else text


def classify_email(text: str) -> Dict:
    """Classifica um e-mail em categoria e intenção usando zero-shot learning."""
    try:
        clf = get_classifier()
        processed = preprocess(text)

        # Categoria (binária)
        cat = clf(processed, LABELS_CATEGORY, multi_label=False)
        category_raw = cat["labels"][0]
        # Mapear para labels simples
        category = "Produtivo" if "produtivo que requer" in category_raw else "Improdutivo"
        cat_score = float(cat["scores"][0])

        # Intenção (top‑1)
        intent = clf(processed, LABELS_INTENT, multi_label=False)
        top_intent = intent["labels"][0]
        intent_score = float(intent["scores"][0])
        
        # Ajuste: emails de agradecimento/felicitação devem ser improdutivos
        if "agradecimento" in top_intent.lower() or "felicitação" in top_intent.lower():
            category = "Improdutivo"
        
        # Override: Se o texto contém palavras típicas de spam/marketing, forçar como improdutivo
        spam_keywords = ["oferta", "desconto", "promoção", "clique aqui", "não perca", "limitada", 
                         "imperdível", "apenas hoje", "corra", "vagas limitadas", "grátis", 
                         "ganhe", "prêmio", "sorteio", "urgente", "levando", "só hoje", "so hoje",
                         "computadores por", "aproveite", "última chance", "oferta especial",
                         "liquidação", "mega promoção", "super oferta", "imperdível"]
        text_lower = text.lower()
        spam_count = sum(1 for keyword in spam_keywords if keyword in text_lower)
        
        # Detecção mais rigorosa: se contém 2 ou mais palavras de spam OU padrões específicos
        promotional_patterns = ["por 1", "x 1", "computadores por", "levando so", "levando só"]
        has_promotional_pattern = any(pattern in text_lower for pattern in promotional_patterns)
        
        if spam_count >= 2 or has_promotional_pattern:  # Threshold reduzido para 2 palavras
            category = "Improdutivo"
            top_intent = "Spam ou marketing"

        return {
            "category": category,
            "category_score": cat_score,
            "intent": top_intent,
            "intent_score": intent_score,
            "processed": processed,
        }
    
    except Exception as e:
        print(f"Erro na classificação: {e}")
        return {
            "category": "Erro",
            "intent": "Erro no processamento",
            "category_score": 0.0,
            "intent_score": 0.0,
            "processed": "",
        }
    finally:
        # Limpeza de memória após classificação
        gc.collect()