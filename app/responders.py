import os
from typing import Dict
from datetime import datetime

from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# === Templates base (português formal corporativo) ===
TEMPLATES = {
    ("Produtivo", "Solicitação de status ou informações"): (
        "Assunto: Atualização do seu atendimento\n\n"
        "Olá, {nome}, tudo bem?\n\n"
        "Localizamos sua solicitação {referencia}. No momento, ela está em '{status_atual}'.\n"
        "Previsão de próxima atualização: {sla}.\n\n"
        "Se houver qualquer novo documento ou informação, por gentileza responda a este e-mail.\n\n"
        "Atenciosamente,\nEquipe de Suporte"
    ),
    ("Produtivo", "Envio de documentos ou arquivos"): (
        "Assunto: Documentos recebidos com sucesso\n\n"
        "Olá, {nome}. Confirmamos o recebimento do(s) arquivo(s): {arquivos}.\n"
        "Encaminhamos para análise e retornamos até {sla}.\n\n"
        "Atenciosamente,\nEquipe de Suporte"
    ),
    ("Produtivo", "Dúvida técnica ou suporte"): (
        "Assunto: Retorno sobre sua dúvida técnica\n\n"
        "Olá, {nome}. Obrigado por nos contatar.\n"
        "Para agilizar, poderia informar: {perguntas_faltantes}?\n"
        "Assim que recebermos, seguimos com a solução. Prazo estimado: {sla}.\n\n"
        "Atenciosamente,\nEquipe de Suporte"
    ),
    ("Improdutivo", "Agradecimento ou felicitação"): (
        "Assunto: Agradecemos a sua mensagem\n\n"
        "Olá, {nome}! Muito obrigado pela sua mensagem.\n"
        "Ficamos à disposição caso precise de algo.\n\n"
        "Abraços,\nEquipe"
    ),
    ("Improdutivo", "Conversa informal ou social"): (
        "Assunto: Retorno da sua mensagem\n\n"
        "Olá, {nome}! Obrigado pela mensagem.\n"
        "Ficamos à disposição para assuntos relacionados ao suporte.\n\n"
        "Abraços,\nEquipe"
    ),
    ("Improdutivo", "Spam ou marketing"): (
        "Assunto: Confirmação de recebimento\n\n"
        "Olá. Sua mensagem foi recebida. Caso necessite suporte, por favor descreva o assunto e um identificador (ex.: nº de contrato/atendimento).\n\n"
        "Atenciosamente,\nEquipe"
    ),
}


def _fill(template: str, ctx: Dict) -> str:
    """Preenche o template com os valores do contexto."""
    defaults = dict(
        nome="",
        referencia="(ID não informado)",
        status_atual="em análise",
        sla=datetime.utcnow().strftime("%d/%m/%Y"),
        arquivos="(não especificado)",
        perguntas_faltantes="ambiente, passos para reproduzir e prints/logs",
    )
    defaults.update({k: v for k, v in ctx.items() if v})
    try:
        return template.format(**defaults)
    except Exception:
        return template


def suggest_reply(category: str, intent: str, context: Dict) -> Dict:
    """Sugere uma resposta baseada na categoria e intenção classificadas."""
    base = TEMPLATES.get((category, intent))
    if not base:
        # fallback
        base = (
            "Assunto: Retorno da sua mensagem\n\n"
            "Olá. Recebemos seu contato referente a '{intent}'. Em breve retornaremos.\n\n"
            "Atenciosamente, Equipe"
        )
        base = base.replace("{intent}", intent)

    filled = _fill(base, context or {})

    # Se houver OpenAI, refinamos o tom
    if OPENAI_API_KEY:
        client = OpenAI()
        prompt = (
            "Revise e melhore a mensagem abaixo com tom profissional e claro, mantendo o conteúdo.\n\n"
            f"Mensagem:\n{filled}\n\nSaída final apenas com o texto revisado."
        )
        try:
            resp = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            improved = resp.choices[0].message.content.strip()
            return {"reply": improved, "source": "openai+template"}
        except Exception:
            pass

    return {"reply": filled, "source": "template"}