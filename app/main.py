import os
import gc
from fastapi import FastAPI, UploadFile, Form, File, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.utils import read_text_from_file
from app.nlp import classify_email
from app.responders import suggest_reply
from app.config import Config

# Contador para limpeza de memória
_operation_count = 0

def cleanup_memory():
    """Força limpeza de memória quando necessário"""
    global _operation_count
    _operation_count += 1
    
    if Config.ENABLE_MEMORY_CLEANUP and _operation_count >= Config.GC_THRESHOLD:
        gc.collect()
        _operation_count = 0
        print(f"Limpeza de memória executada. Memória atual: {Config.get_memory_info()}")

PORT = Config.PORT
MAX_CHARS = Config.MAX_CHARS
MAX_FILE_SIZE = Config.MAX_FILE_SIZE

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
    cleanup_memory()
    memory_info = Config.get_memory_info()
    return {
        "status": "ok", 
        "service": "AutoU Email Classifier",
        "memory": memory_info
    }


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
    content = None
    
    try:
        # Processar arquivo ou texto
        if file is not None:
            # Verificar tamanho do arquivo
            if file.size and file.size > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=413,
                    detail=f"Arquivo muito grande. Máximo permitido: {MAX_FILE_SIZE // (1024*1024)}MB"
                )
            
            filename = file.filename
            content = await file.read()
            
            try:
                raw, _ = read_text_from_file(filename, content)
            except ValueError as e:
                return JSONResponse(
                    {"detail": str(e)}, 
                    status_code=400
                )
            finally:
                # Limpar conteúdo do arquivo da memória
                content = None
                gc.collect()
                
        elif text:
            # Verificar tamanho do texto
            if len(text) > MAX_CHARS:
                text = text[:MAX_CHARS]
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
    
    except Exception as e:
        # Log do erro e limpeza de memória
        gc.collect()
        return JSONResponse(
            {"detail": f"Erro interno do servidor: {str(e)}"}, 
            status_code=500
        )
    
    finally:
        # Limpeza final de memória
        cleanup_memory()
        raw = None
        content = None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)