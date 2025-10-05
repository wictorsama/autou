from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

app = FastAPI(
    title="AutoU Email Classifier",
    description="Classificador inteligente de emails",
    version="1.0.0"
)

# Serve static files
static_path = os.path.join(os.path.dirname(__file__), '..', 'app', 'static')
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

class TextRequest(BaseModel):
    text: str

class ClassificationResponse(BaseModel):
    classification: str
    confidence: float
    category: str
    message: str

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML page"""
    template_path = os.path.join(os.path.dirname(__file__), '..', 'app', 'templates', 'index.html')
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>AutoU Email Classifier - AWS Lambda Version</h1><p>Frontend not available in this deployment.</p>")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "autou-email-classifier", "version": "aws-lambda"}

@app.post("/api/process", response_model=ClassificationResponse)
async def process_text(request: TextRequest):
    """Process text classification - simplified version for AWS Lambda"""
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text is required")
    
    text = request.text.strip().lower()
    
    # Simple rule-based classification for AWS Lambda version
    if any(word in text for word in ['reunião', 'meeting', 'encontro', 'agenda']):
        classification = "produtivo"
        category = "reuniao"
        confidence = 0.85
        message = "Email classificado como reunião/encontro"
    elif any(word in text for word in ['aprovação', 'aprovar', 'autorização', 'autorizar']):
        classification = "produtivo"
        category = "aprovacao"
        confidence = 0.80
        message = "Email classificado como solicitação de aprovação"
    elif any(word in text for word in ['orçamento', 'proposta', 'cotação', 'valor']):
        classification = "produtivo"
        category = "orcamento"
        confidence = 0.75
        message = "Email classificado como orçamento/proposta"
    elif any(word in text for word in ['status', 'andamento', 'progresso', 'atualização']):
        classification = "produtivo"
        category = "status"
        confidence = 0.70
        message = "Email classificado como atualização de status"
    elif any(word in text for word in ['spam', 'promoção', 'oferta', 'desconto', 'grátis']):
        classification = "improdutivo"
        category = "spam"
        confidence = 0.90
        message = "Email classificado como spam/promoção"
    else:
        classification = "produtivo"
        category = "geral"
        confidence = 0.60
        message = "Email classificado como produtivo (classificação geral)"
    
    return ClassificationResponse(
        classification=classification,
        confidence=confidence,
        category=category,
        message=message
    )

@app.get("/favicon.ico")
async def favicon():
    """Serve favicon"""
    icon_path = os.path.join(os.path.dirname(__file__), '..', 'app', 'static', 'icon.svg')
    if os.path.exists(icon_path):
        return FileResponse(icon_path)
    return {"message": "Favicon not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)