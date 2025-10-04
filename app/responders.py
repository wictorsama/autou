import os
from typing import Dict
from datetime import datetime

from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# === Templates base (português formal corporativo) ===
TEMPLATES = {
    # Templates para intenções produtivas
    ("Produtivo", "Solicitação de status ou acompanhamento"): (
        "Assunto: Atualização do seu atendimento\n\n"
        "Olá, {nome}, tudo bem?\n\n"
        "Localizamos sua solicitação {referencia}. No momento, ela está em '{status_atual}'.\n"
        "Previsão de próxima atualização: {sla}.\n\n"
        "Se houver qualquer novo documento ou informação, por gentileza responda a este e-mail.\n\n"
        "Atenciosamente,\nEquipe de Suporte"
    ),
    ("Produtivo", "Pedido de informações ou esclarecimentos"): (
        "Assunto: Informações solicitadas\n\n"
        "Olá, {nome}. Recebemos sua solicitação de informações.\n"
        "Estamos levantando os dados necessários e retornaremos até {sla}.\n\n"
        "Caso precise de algo mais específico, por favor detalhe sua necessidade.\n\n"
        "Atenciosamente,\nEquipe de Suporte"
    ),
    ("Produtivo", "Envio de documentos ou arquivos importantes"): (
        "Assunto: Documentos recebidos com sucesso\n\n"
        "Olá, {nome}. Confirmamos o recebimento do(s) arquivo(s): {arquivos}.\n"
        "Encaminhamos para análise e retornamos até {sla}.\n\n"
        "Atenciosamente,\nEquipe de Suporte"
    ),
    ("Produtivo", "Dúvida técnica ou solicitação de suporte"): (
        "Assunto: Retorno sobre sua dúvida técnica\n\n"
        "Olá, {nome}. Obrigado por nos contatar.\n"
        "Para agilizar, poderia informar: {perguntas_faltantes}?\n"
        "Assim que recebermos, seguimos com a solução. Prazo estimado: {sla}.\n\n"
        "Atenciosamente,\nEquipe de Suporte"
    ),
    ("Produtivo", "Agendamento de reunião ou compromisso"): (
        "Assunto: Confirmação de agendamento\n\n"
        "Olá, {nome}. Recebemos sua solicitação de agendamento.\n"
        "Verificaremos a disponibilidade e confirmaremos até {sla}.\n\n"
        "Por favor, informe se há alguma preferência de horário ou pauta específica.\n\n"
        "Atenciosamente,\nEquipe"
    ),
    ("Produtivo", "Aprovação ou autorização necessária"): (
        "Assunto: Solicitação em análise para aprovação\n\n"
        "Olá, {nome}. Recebemos sua solicitação de aprovação/autorização.\n"
        "Encaminhamos para o setor responsável. Prazo de retorno: {sla}.\n\n"
        "Manteremos você informado sobre o andamento.\n\n"
        "Atenciosamente,\nEquipe de Suporte"
    ),
    ("Produtivo", "Cobrança ou follow-up de pendências"): (
        "Assunto: Acompanhamento da sua solicitação\n\n"
        "Olá, {nome}. Recebemos seu follow-up sobre {referencia}.\n"
        "Verificaremos o status atual e retornaremos com uma atualização até {sla}.\n\n"
        "Agradecemos sua paciência e acompanhamento.\n\n"
        "Atenciosamente,\nEquipe de Suporte"
    ),
    ("Produtivo", "Solicitação de orçamento ou proposta"): (
        "Assunto: Solicitação de orçamento recebida\n\n"
        "Olá, {nome}. Recebemos sua solicitação de orçamento/proposta.\n"
        "Nossa equipe comercial analisará os requisitos e retornará até {sla}.\n\n"
        "Caso precise de esclarecimentos adicionais, estaremos à disposição.\n\n"
        "Atenciosamente,\nEquipe Comercial"
    ),
    
    # Templates para intenções improdutivas
    ("Improdutivo", "Agradecimento ou felicitação"): (
        "Assunto: Agradecemos a sua mensagem\n\n"
        "Olá, {nome}! Muito obrigado pela sua mensagem.\n"
        "Ficamos à disposição caso precise de algo.\n\n"
        "Abraços,\nEquipe"
    ),
    ("Improdutivo", "Confirmação ou comunicado informativo"): (
        "Assunto: Confirmação de recebimento\n\n"
        "Olá, {nome}. Confirmamos o recebimento da sua mensagem informativa.\n"
        "Agradecemos por nos manter atualizados.\n\n"
        "Atenciosamente,\nEquipe"
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
    ("Improdutivo", "Notificação automática do sistema"): (
        "Assunto: Notificação recebida\n\n"
        "Olá. Recebemos sua notificação automática.\n"
        "Caso seja necessária alguma ação de nossa parte, por favor entre em contato.\n\n"
        "Atenciosamente,\nEquipe de Suporte"
    ),
    ("Improdutivo", "Convite para evento ou treinamento"): (
        "Assunto: Agradecemos o convite\n\n"
        "Olá, {nome}. Agradecemos pelo convite para {evento}.\n"
        "Verificaremos a disponibilidade e retornaremos em breve.\n\n"
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