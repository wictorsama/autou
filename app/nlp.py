import os
from typing import Dict, List
import nltk
from nltk.corpus import stopwords
from transformers import pipeline

# NLTK setup
nltk.download("stopwords", quiet=True)
STOP_PT = set(stopwords.words("portuguese"))

ZSL_MODEL = os.getenv("ZSL_MODEL", "joeddav/xlm-roberta-large-xnli")

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
        _zsl_cls = pipeline("zero-shot-classification", model=ZSL_MODEL)
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
;    intent_score = float(intent["scores"][0])
    
    # Ajuste: emails de agradecimento/felicitação devem ser improdutivos
    if "agradecimento" in top_intent.lower() or "felicitação" in top_intent.lower():
        category = "Improdutivo"
    
    # Override: Se o texto contém palavras típicas de spam/marketing, forçar como improdutivo
    spam_keywords = ["oferta", "desconto", "promoção", "clique aqui", "não perca", "limitada", 
                     "imperdível", "apenas hoje", "corra", "vagas limitadas", "grátis", 
                     "ganhe", "prêmio", "sorteio", "urgente"]
    text_lower = text.lower()
    spam_count = sum(1 for keyword in spam_keywords if keyword in text_lower)
    
    if spam_count >= 3:  # Se contém 3 ou mais palavras de spam
        category = "Improdutivo"
        top_intent = "Spam ou marketing"

    return {
        "category": category,
        "category_score": cat_score,
        "intent": top_intent,
        "intent_score": intent_score,
        "processed": processed,
    }