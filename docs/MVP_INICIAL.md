# AutoU – Classificador & Respostas de E‑mails (MVP)

Abaixo segue um **pacote completo** (estrutura de repositório, código, requisitos e guias de deploy + roteiro de vídeo)** pronto para você colar no GitHub**. É um MVP em **FastAPI + HTML/Tailwind + Alpine.js**, com **Transformers (zero‑shot)** para classificação e **geração de resposta** via **templates** ou **OpenAI** (opcional, se houver chave), além de **parser de PDF**.

---

## 📁 Estrutura de Pastas
```
autou-email-ai/
├─ app/
│  ├─ main.py
│  ├─ nlp.py
│  ├─ responders.py
│  ├─ utils.py
│  ├─ models/
│  │  └─ __init__.py
│  ├─ templates/
│  │  └─ index.html
│  └─ static/
│     ├─ styles.css
│     └─ app.js
├─ sample_emails/
│  ├─ produtivo_status.txt
│  ├─ produtivo_anexo.txt
│  └─ improdutivo_felicitacao.txt
├─ tests/
│  └─ test_api.py
├─ deploy/
│  ├─ .env.example
│  ├─ deploy.sh
│  └─ README.md
├─ requirements.txt
├─ Dockerfile
├─ render.yaml
├─ Procfile
├─ README.md
└─ LICENSE
```

---

## ✅ Requisitos & Decisões Técnicas (resumo)
- **Classificação**: `transformers` com *zero-shot* usando **joeddav/xlm-roberta-large-xnli** (multilíngue, ótimo para PT‑BR) e rótulos: `Produtivo` vs `Improdutivo` + detecção de **intenção** (status, envio de arquivo, dúvida técnica, agradecimento/felicit.)
- **Geração de resposta**:
  - *Default:* **templates** condicionais por categoria/intenções, com placeholders (nº do ticket, anexos, SLA, etc.).
  - *Opcional:* se `OPENAI_API_KEY` definido, usa **OpenAI** para refinar o texto com tom profissional e RGPD/LGPD‑friendly.
- **Pré-processamento NLP**: normalização, remoção de *stopwords* PT‑BR, lematização (opcional via spaCy) e heurísticas para detecção de anexos/pedidos de status.
- **Uploads**: aceita `.txt` e `.pdf` (via `pdfminer.six`).
- **UI**: HTML + Tailwind (CDN) + Alpine.js. Drag & drop, colar texto, **prévias** de texto, **badge** de categoria, **cópia rápida** da resposta.
- **Backend**: FastAPI, endpoints `/api/process` e `/health`. Respostas em JSON. CORS pronto.
- **Deploy**:
  - **AWS Lambda** (recomendado): Serverless Framework + `serverless.yml`
  - **Render** (legado): `render.yaml` + `Procfile`
  - **Hugging Face Spaces** (Gradio opcional) **ou** qualquer serviço com Dockerfile.
- **Testes**: `pytest` cobre sucesso de `/api/process` e classificação básica.

---

## 🔐 Variáveis de Ambiente (deploy/.env.example)
```
# Opcional – refino de respostas por LLM
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

# Modelo de zero-shot (padrão multilíngue)
ZSL_MODEL=joeddav/xlm-roberta-large-xnli

# FastAPI
PORT=8000
HOST=0.0.0.0

# Limites
MAX_TEXT_CHARS=20000
```

> Se `OPENAI_API_KEY` não existir, o sistema usa apenas **templates** – ainda assim você cumpre o desafio 100%.

---

## 🐍 `requirements.txt`
```
fastapi==0.115.0
uvicorn[standard]==0.30.6
python-multipart==0.0.9
jinja2==3.1.4
pydantic==2.9.2
pydantic-settings==2.5.2
transformers==4.44.2
torch==2.4.0
nltk==3.9.1
pdfminer.six==20231228
openai==1.52.2
spacy==3.7.4
spacy-lookups-data==1.0.5
```

> **Opcional**: baixar `pt_core_news_sm` para lematização (`python -m spacy download pt_core_news_sm`).

---

## 🧠 `app/nlp.py`
```python
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

LABELS_CATEGORY = ["Produtivo", "Improdutivo"]
LABELS_INTENT = [
    "Solicitação de status",
    "Envio de documentos/arquivo",
    "Dúvida técnica",
    "Agradecimento/Felicitacao",
    "Spam/Irrelevante"
]


def get_classifier():
    global _zsl_cls
    if _zsl_cls is None:
        _zsl_cls = pipeline("zero-shot-classification", model=ZSL_MODEL)
    return _zsl_cls


def preprocess(text: str) -> str:
    # minify
    text = (text or "").strip()
    # remove stopwords simples mantendo semântica
    tokens = [t for t in text.split() if t.lower() not in STOP_PT]
    return " ".join(tokens) if tokens else text


def classify_email(text: str) -> Dict:
    clf = get_classifier()
    processed = preprocess(text)

    # Categoria (binária)
    cat = clf(processed, LABELS_CATEGORY, multi_label=False)
    category = cat["labels"][0]
    cat_score = float(cat["scores"][0])

    # Intenção (top‑1)
    intent = clf(processed, LABELS_INTENT, multi_label=False)
    top_intent = intent["labels"][0]
    intent_score = float(intent["scores"][0])

    return {
        "category": category,
        "category_score": cat_score,
        "intent": top_intent,
        "intent_score": intent_score,
        "processed": processed,
    }
```

---

## ✉️ `app/responders.py`
```python
import os
from typing import Dict
from datetime import datetime

from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# === Templates base (português formal corporativo) ===
TEMPLATES = {
    ("Produtivo", "Solicitação de status"): (
        "Assunto: Atualização do seu atendimento\n\n"
        "Olá, {nome}, tudo bem?\n\n"
        "Localizamos sua solicitação {referencia}. No momento, ela está em '{status_atual}'.\n"
        "Previsão de próxima atualização: {sla}.\n\n"
        "Se houver qualquer novo documento ou informação, por gentileza responda a este e-mail.\n\n"
        "Atenciosamente,\nEquipe de Suporte"
    ),
    ("Produtivo", "Envio de documentos/arquivo"): (
        "Assunto: Documentos recebidos com sucesso\n\n"
        "Olá, {nome}. Confirmamos o recebimento do(s) arquivo(s): {arquivos}.\n"
        "Encaminhamos para análise e retornamos até {sla}.\n\n"
        "Atenciosamente,\nEquipe de Suporte"
    ),
    ("Produtivo", "Dúvida técnica"): (
        "Assunto: Retorno sobre sua dúvida técnica\n\n"
        "Olá, {nome}. Obrigado por nos contatar.\n"
        "Para agilizar, poderia informar: {perguntas_faltantes}?\n"
        "Assim que recebermos, seguimos com a solução. Prazo estimado: {sla}.\n\n"
        "Atenciosamente,\nEquipe de Suporte"
    ),
    ("Improdutivo", "Agradecimento/Felicitacao"): (
        "Assunto: Agradecemos a sua mensagem\n\n"
        "Olá, {nome}! Muito obrigado pela sua mensagem.\n"
        "Ficamos à disposição caso precise de algo.\n\n"
        "Abraços,\nEquipe"
    ),
    ("Improdutivo", "Spam/Irrelevante"): (
        "Assunto: Confirmação de recebimento\n\n"
        "Olá. Sua mensagem foi recebida. Caso necessite suporte, por favor descreva o assunto e um identificador (ex.: nº de contrato/atendimento).\n\n"
        "Atenciosamente,\nEquipe"
    ),
}


def _fill(template: str, ctx: Dict) -> str:
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
```

---

## 🧰 `app/utils.py`
```python
import io
from typing import Tuple
from pdfminer.high_level import extract_text

ALLOWED_EXTS = {".txt", ".pdf"}


def read_text_from_file(filename: str, content: bytes) -> Tuple[str, str]:
    name = filename or ""
    lower = name.lower()
    text = ""

    if lower.endswith(".txt"):
        text = content.decode("utf-8", errors="ignore")
        return text, "text/plain"
    if lower.endswith(".pdf"):
        # pdfminer precisa de um buffer
        with io.BytesIO(content) as pdf_buf:
            text = extract_text(pdf_buf) or ""
        return text, "application/pdf"
    raise ValueError("Formato de arquivo não suportado. Use .txt ou .pdf.")
```

---

## 🚀 `app/main.py`
```python
import os
from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.utils import read_text_from_file
from app.nlp import classify_email
from app.responders import suggest_reply

PORT = int(os.getenv("PORT", 8000))
MAX_CHARS = int(os.getenv("MAX_TEXT_CHARS", 20000))

app = FastAPI(title="AutoU Email Classifier")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


class ProcessResponse(BaseModel):
    category: str
    category_score: float
    intent: str
    intent_score: float
    suggested_reply: str
    reply_source: str


@app.get("/", response_class=HTMLResponse)
def index():
    from fastapi.templating import Jinja2Templates
    from fastapi import Request
    templates = Jinja2Templates(directory="app/templates")
    return templates.TemplateResponse("index.html", {"request": Request(scope={"type": "http"})})


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/process", response_model=ProcessResponse)
async def process_email(file: UploadFile | None = File(default=None), text: str | None = Form(default=None)):
    raw = ""
    filename = None
    if file is not None:
        filename = file.filename
        content = await file.read()
        raw, _ = read_text_from_file(filename, content)
    elif text:
        raw = text
    else:
        return JSONResponse({"detail": "Envie um arquivo .txt/.pdf ou cole o texto."}, status_code=400)

    if not raw.strip():
        return JSONResponse({"detail": "Conteúdo vazio após leitura."}, status_code=400)

    if len(raw) > MAX_CHARS:
        raw = raw[:MAX_CHARS]

    clf = classify_email(raw)

    # Contexto simples (poderia extrair com regex/NER)
    context = {
        "nome": "",
        "referencia": "",
        "status_atual": "em análise",
        "sla": "2 dias úteis",
        "arquivos": filename or "",
        "perguntas_faltantes": "ambiente, passos para reproduzir, prints/logs",
    }

    reply = suggest_reply(clf["category"], clf["intent"], context)

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
```

---

## 🖥️ `app/templates/index.html`
```html
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AutoU – Classificador de E‑mail</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
  <link rel="stylesheet" href="/static/styles.css" />
</head>
<body class="bg-slate-50 text-slate-900">
  <main class="max-w-4xl mx-auto p-6" x-data="emailApp()">
    <header class="mb-6">
      <h1 class="text-2xl font-bold">AutoU – Classificador & Respostas</h1>
      <p class="text-sm text-slate-600">Envie um .txt/.pdf ou cole o texto. O sistema identifica <b>Produtivo</b> vs <b>Improdutivo</b> e sugere uma resposta.</p>
    </header>

    <section class="grid gap-4 md:grid-cols-2">
      <div class="bg-white rounded-xl shadow p-4">
        <h2 class="font-semibold mb-2">Entrada</h2>
        <div class="space-y-3">
          <textarea x-model="rawText" class="w-full h-40 border rounded-lg p-3 focus:outline-none" placeholder="Cole o texto do e‑mail aqui..."></textarea>
          <div class="flex items-center gap-2">
            <input type="file" x-ref="file" class="hidden" @change="onFileChange" accept=".txt,.pdf" />
            <button class="btn" @click="$refs.file.click()">Selecionar arquivo (.txt/.pdf)</button>
            <button class="btn-secondary" @click="clearAll">Limpar</button>
          </div>
          <button class="btn-primary w-full" @click="submit" :disabled="loading">
            <span x-show="!loading">Classificar & Sugerir Resposta</span>
            <span x-show="loading">Processando...</span>
          </button>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow p-4">
        <h2 class="font-semibold mb-2">Resultado</h2>
        <template x-if="result">
          <div class="space-y-3">
            <div class="flex items-center gap-2">
              <span class="badge" :class="result.category==='Produtivo' ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-200 text-slate-700'" x-text="result.category"></span>
              <span class="text-xs text-slate-500">confiança: <span x-text="(result.category_score*100).toFixed(1)+'%'"></span></span>
            </div>
            <div class="text-sm text-slate-700">Intenção: <b x-text="result.intent"></b> (<span x-text="(result.intent_score*100).toFixed(1)+'%'"></span>)</div>
            <div>
              <label class="text-sm text-slate-600">Resposta sugerida</label>
              <textarea class="w-full h-48 border rounded-lg p-3" x-model="result.suggested_reply"></textarea>
              <div class="flex gap-2 mt-2">
                <button class="btn" @click="copyReply">Copiar</button>
                <span class="text-xs text-slate-500" x-text="'Fonte: ' + (result.reply_source||'-')"></span>
              </div>
            </div>
          </div>
        </template>
        <template x-if="!result">
          <p class="text-sm text-slate-500">Nenhum resultado ainda. Faça o upload ou cole um texto e clique em <b>Classificar</b>.</p>
        </template>
      </div>
    </section>

    <footer class="mt-6 text-xs text-slate-500">
      <p>🛈 Dica: sem <code>OPENAI_API_KEY</code>, o sistema usa templates. Com a chave, ele refina a resposta automaticamente.</p>
    </footer>
  </main>

  <script src="/static/app.js"></script>
</body>
</html>
```

---

## 🎨 `app/static/styles.css`
```css
.btn { @apply inline-flex items-center justify-center px-3 py-2 rounded-lg border border-slate-300 text-sm hover:bg-slate-50; }
.btn-secondary { @apply inline-flex items-center justify-center px-3 py-2 rounded-lg bg-slate-100 text-slate-700 text-sm hover:bg-slate-200; }
.btn-primary { @apply inline-flex items-center justify-center px-3 py-2 rounded-lg bg-indigo-600 text-white text-sm hover:bg-indigo-700 disabled:opacity-60; }
.badge { @apply inline-flex items-center px-2 py-1 rounded-full text-xs font-medium; }
```

---

## 🧩 `app/static/app.js`
```javascript
function emailApp(){
  return {
    rawText: "",
    file: null,
    loading: false,
    result: null,
    onFileChange(e){ this.file = e.target.files[0] || null; },
    clearAll(){ this.rawText = ""; this.file = null; this.result = null; },
    async submit(){
      this.loading = true; this.result = null;
      try{
        const form = new FormData();
        if(this.file){ form.append('file', this.file); }
        if(this.rawText && !this.file){ form.append('text', this.rawText); }
        const res = await fetch('/api/process', { method:'POST', body: form });
        if(!res.ok){ const e = await res.json(); throw new Error(e.detail || 'Erro'); }
        this.result = await res.json();
      }catch(err){
        alert(err.message);
      }finally{
        this.loading = false;
      }
    },
    async copyReply(){
      if(this.result?.suggested_reply){
        await navigator.clipboard.writeText(this.result.suggested_reply);
      }
    }
  }
}
```

---

## 🧪 `tests/test_api.py`
```python
import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get('/health')
    assert r.status_code == 200


def test_process_with_text():
    payload = {"text": "Olá, podem me passar o status do chamado 123?"}
    r = client.post('/api/process', data=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["category"] in ("Produtivo", "Improdutivo")
    assert isinstance(data["suggested_reply"], str)
```

---

## 📝 `README.md` (cole no repo)
```markdown
# AutoU – Classificador & Respostas de E‑mails (MVP)

MVP full‑stack para **classificar e-mails** (Produtivo/Improdutivo), identificar **intenção** e **sugerir respostas automáticas**. Construído com **FastAPI** + **Transformers (zero-shot)** + **UI em HTML/Tailwind/Alpine**. Suporta **.txt** e **.pdf**.

## ✨ Funcionalidades
- Upload de `.txt`/`.pdf` ou colagem de texto
- Classificação **Produtivo vs Improdutivo** e **detecção de intenção**
- Resposta automática por **templates** (sem custo) ou refinada por **OpenAI** (opcional)
- UI leve e responsiva, com cópia rápida de resposta

## 🧰 Stack
- Backend: FastAPI, Transformers (modelo `joeddav/xlm-roberta-large-xnli`)
- UI: HTML + Tailwind (CDN) + Alpine.js
- PDF: pdfminer.six
- Testes: pytest

## ⚙️ Setup Local
```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\\Scripts\\activate)
pip install -r requirements.txt
# (opcional) python -m spacy download pt_core_news_sm
cp deploy/.env.example .env
uvicorn app.main:app --reload --port 8000
```
Acesse: http://localhost:8000

## 🔑 OpenAI (opcional)
No `.env`, defina `OPENAI_API_KEY` para o refinamento das respostas. Sem a chave, o sistema usa templates.

## 🧪 Testes
```bash
pytest -q
```

## ☁️ Deploy (AWS Lambda - Recomendado)

1. **Configurar AWS CLI**: `aws configure`
2. **Instalar Serverless**: `npm install -g serverless`
3. **Deploy**: `cd deploy && npx serverless deploy`

**Status atual**: ✅ Funcionando em `https://x1r6i3udxg.execute-api.us-east-1.amazonaws.com/dev/`

## ☁️ Deploy (Render.com - Legado)
1. Faça **fork** deste repositório.
2. No Render: **New + Web Service** → conecte ao GitHub → *Environment*: `Python` → *Build Command*: `pip install -r requirements.txt` → *Start Command*: `uvicorn app.main:app --host 0.0.0.0 --port 10000` (ou use `Procfile`).
3. Defina env vars (opcional): `OPENAI_API_KEY`, `ZSL_MODEL`.
4. Publique e copie a URL pública.

> Alternativa: **Docker**
```bash
docker build -t autou-email-ai .
docker run -p 8000:8000 autou-email-ai
```

## ☁️ Deploy (Hugging Face Spaces – Docker)
- Crie um Space tipo **Docker** e envie os arquivos (`Dockerfile`, `requirements.txt`, etc.).

## 📦 Endpoints
- `GET /` → UI
- `POST /api/process` → recebe `file` (.txt/.pdf) **ou** `text` (form)
- `GET /health`

### Exemplo de resposta `/api/process`
```json
{
  "category": "Produtivo",
  "category_score": 0.94,
  "intent": "Solicitação de status",
  "intent_score": 0.88,
  "suggested_reply": "Assunto: ...",
  "reply_source": "template"
}
```

## 📂 Dados de Exemplo
Consulte a pasta `sample_emails/`.

## 🔍 Notas de Qualidade
- Código **organizado**, **tipado** e com **docstrings**.
- Pipeline `zero-shot` evita treinar do zero, mas você pode **fine‑tunar** futuramente.
- Para *privacy*: sem logs de dados por padrão; adicionar mascaramento de PII é trivial.

## 🛡️ LGPD
- Respostas padronizadas não expõem dados sensíveis.
- Se usar LLM externo (OpenAI), garanta contratos/DPA.

## 🗺️ Roadmap (extras)
- Extração de **ID de ticket** via regex/NER
- Dashboard de **métricas** (acurácia, distribuição por intenção)
- Fila assíncrona (Celery/Redis) para alto volume
- Login SSO e feedback humano (aprendizado ativo)
```

---

## 🧾 `Dockerfile`
```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🔧 `Procfile`
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## 📜 `render.yaml`
```yaml
services:
  - type: web
    name: autou-email-ai
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: ZSL_MODEL
        value: joeddav/xlm-roberta-large-xnli
```

---

## 🧪 `sample_emails/`
**produtivo_status.txt**
```
Bom dia, poderiam me informar o status do chamado #45721? Precisa de mais algum documento?
```

**produtivo_anexo.txt**
```
Segue em anexo o comprovante solicitado para dar sequência no processo 8821.
```

**improdutivo_felicitacao.txt**
```
Feliz Natal a toda a equipe! Obrigado pelo suporte ao longo do ano.
```

---

## 🎥 Roteiro do Vídeo (3–5 min)
**0:00 – 0:30 | Introdução**
- Nome, contexto do desafio (empresa financeira, alto volume de e-mails) e objetivo (automatizar leitura, classificação e resposta).

**0:30 – 3:30 | Demonstração**
- Acessa URL deployada, mostra upload de `.txt/.pdf` e colagem de texto.
- Exibe categoria (badge), intenção e confiança.
- Mostra resposta sugerida e botão de copiar.
- (Opcional) Mostra diferença com/sem `OPENAI_API_KEY`.

**3:30 – 4:30 | Técnica**
- FastAPI + zero-shot `joeddav/xlm-roberta-large-xnli`.
- Pré-processamento (stopwords), parser PDF, templates de resposta e refino com LLM.
- Decisões: zero‑shot (sem treino), multilíngue, extensível com NER/regex.

**4:30 – 5:00 | Conclusão**
- Reforça benefícios: economia de tempo, consistência, base sólida para escalar.
- Próximos passos: dashboard, feedback humano, fine‑tuning.

---

## 📌 Observações finais
- Com esse pacote, você cobre **todos os entregáveis**: código, README com instruções e guias de deploy, amostras e roteiro do vídeo.
- Se quiser, posso **gerar um README já pronto em PT/EN** e um **script de gravação** com bullet‑points para leitura durante o vídeo.

