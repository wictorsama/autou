import os
from fastapi import FastAPI, UploadFile, Form, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.utils import read_text_from_file
from app.nlp import classify_email
from app.responders import suggest_reply

PORT = int(os.getenv("PORT", 8000))
MAX_CHARS = int(os.getenv("MAX_TEXT_CHARS", 20000))

app = FastAPI(title="AutoU Email Classifier", description="Sistema de classificação e resposta automática de e-mails")

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")


class ProcessResponse(BaseModel):
    """Modelo de resposta para o endpoint de processamento."""
    category: str
    category_score: float
    intent: str
    intent_score: float
    suggested_reply: str
    reply_source: str


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Página principal da aplicação."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health():
    """Endpoint de health check."""
    return {"status": "ok", "service": "AutoU Email Classifier"}


@app.post("/api/process", response_model=ProcessResponse)
async def process_email(
    file: UploadFile | None = File(default=None), 
    text: str | None = Form(default=None)
):
    """Processa um e-mail e retorna classificação e resposta sugerida.
    
    Args:
        file: Arquivo .txt ou .pdf (opcional)
        text: Texto do e-mail (opcional)
        
    Returns:
        ProcessResponse com classificação e resposta sugerida
    """
    raw = ""
    filename = None
    
    # Processar arquivo ou texto
    if file is not None:
        filename = file.filename
        content = await file.read()
        try:
            raw, _ = read_text_from_file(filename, content)
        except ValueError as e:
            return JSONResponse(
                {"detail": str(e)}, 
                status_code=400
            )
    elif text:
        raw = text
    else:
        return JSONResponse(
            {"detail": "Envie um arquivo .txt/.pdf ou cole o texto."}, 
            status_code=400
        )

    # Validar conteúdo
    if not raw.strip():
        return JSONResponse(
            {"detail": "Conteúdo vazio após leitura."}, 
            status_code=400
        )

    # Limitar tamanho do texto
    if len(raw) > MAX_CHARS:
        raw = raw[:MAX_CHARS]

    # Classificar e-mail
    try:
        clf = classify_email(raw)
    except Exception as e:
        return JSONResponse(
            {"detail": f"Erro na classificação: {str(e)}"}, 
            status_code=500
        )

    # Contexto para geração de resposta
    context = {
        "nome": "",
        "referencia": "",
        "status_atual": "em análise",
        "sla": "2 dias úteis",
        "arquivos": filename or "",
        "perguntas_faltantes": "ambiente, passos para reproduzir, prints/logs",
    }

    # Gerar resposta sugerida
    try:
        reply = suggest_reply(clf["category"], clf["intent"], context)
    except Exception as e:
        return JSONResponse(
            {"detail": f"Erro na geração de resposta: {str(e)}"}, 
            status_code=500
        )

    return ProcessResponse(
        category=clf["category"],
        category_score=clf["category_score"],
        intent=clf["intent"],
        intent_score=clf["intent_score"],
        suggested_reply=reply["reply"],
        reply_source=reply["source"],
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)