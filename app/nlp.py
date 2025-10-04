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
# Intenções mais específicas e convencionais para emails corporativos
LABELS_INTENT = [
    # Produtivos - Requerem ação
    "Solicitação de status ou acompanhamento",
    "Pedido de informações ou esclarecimentos", 
    "Envio de documentos ou arquivos importantes",
    "Dúvida técnica ou solicitação de suporte",
    "Agendamento de reunião ou compromisso",
    "Aprovação ou autorização necessária",
    "Cobrança ou follow-up de pendências",
    "Solicitação de orçamento ou proposta",
    
    # Improdutivos - Informativos ou sociais
    "Agradecimento ou felicitação",
    "Confirmação ou comunicado informativo",
    "Conversa informal ou social",
    "Spam ou marketing",
    "Notificação automática do sistema",
    "Convite para evento ou treinamento"
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
        
        # Refinamento inteligente baseado em palavras-chave específicas
        text_lower = text.lower()
        
        # Detecção de intenções produtivas específicas
        if any(word in text_lower for word in ["status", "andamento", "situação", "acompanhamento", "posição"]):
            top_intent = "Solicitação de status ou acompanhamento"
            category = "Produtivo"
        elif any(word in text_lower for word in ["reunião", "meeting", "agendar", "marcar", "disponibilidade", "horário"]):
            top_intent = "Agendamento de reunião ou compromisso"
            category = "Produtivo"
        elif any(word in text_lower for word in ["aprovar", "aprovação", "autorizar", "autorização", "validar", "confirmar aprovação"]):
            top_intent = "Aprovação ou autorização necessária"
            category = "Produtivo"
        elif any(word in text_lower for word in ["orçamento", "proposta", "cotação", "preço", "valor", "custo"]):
            top_intent = "Solicitação de orçamento ou proposta"
            category = "Produtivo"
        elif any(word in text_lower for word in ["cobrança", "pendência", "follow-up", "followup", "prazo", "vencimento"]):
            top_intent = "Cobrança ou follow-up de pendências"
            category = "Produtivo"
        elif any(word in text_lower for word in ["convite", "evento", "treinamento", "curso", "workshop", "palestra"]):
            top_intent = "Convite para evento ou treinamento"
            category = "Improdutivo"
        elif any(word in text_lower for word in ["notificação", "automático", "sistema", "noreply", "no-reply"]):
            top_intent = "Notificação automática do sistema"
            category = "Improdutivo"
        
        # Ajuste: emails de agradecimento/felicitação devem ser improdutivos
        if "agradecimento" in top_intent.lower() or "felicitação" in top_intent.lower():
            category = "Improdutivo"
        
        # Detecção adicional de agradecimentos baseada no conteúdo do texto
        gratitude_keywords = ["obrigado", "obrigada", "agradeço", "agradecemos", "grato", "grata", 
                             "muito obrigado", "muito obrigada", "excelente", "perfeito", "perfeitamente",
                             "parabéns", "felicitações", "sucesso", "ótimo trabalho", "bom trabalho"]
        
        # Palavras que indicam conclusão/resolução (não solicitação)
        resolution_keywords = ["resolvido", "solucionado", "concluído", "finalizado", "problema foi", 
                              "tudo certo", "está ok", "funcionando"]
        
        text_lower = text.lower()
        gratitude_count = sum(1 for keyword in gratitude_keywords if keyword in text_lower)
        resolution_count = sum(1 for keyword in resolution_keywords if keyword in text_lower)
        
        # Se contém múltiplas palavras de agradecimento OU agradecimento + resolução
        if gratitude_count >= 2 or (gratitude_count >= 1 and resolution_count >= 1):
            category = "Improdutivo"
            top_intent = "Agradecimento ou felicitação"
        
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