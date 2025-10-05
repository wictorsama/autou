import json
import sys
import os
import base64
import re

# Add the parent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def lambda_handler(event, context):
    """
    AWS Lambda handler function - Direct API Gateway integration
    Replicates the exact local frontend functionality
    """
    
    # CORS headers
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    }
    
    try:
        # Handle OPTIONS requests (CORS preflight)
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        # Get path and method
        path = event.get('path', '/')
        method = event.get('httpMethod', 'GET')
        
        # Health check endpoint
        if path == '/health' and method == 'GET':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'status': 'healthy',
                    'service': 'autou-email-classifier',
                    'version': 'aws-lambda-direct'
                })
            }
        
        # Static files (simplified)
        if path.startswith('/static/'):
            if path == '/static/icon.svg':
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'image/svg+xml'},
                    'body': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#4f46e5"><path d="M12 2L2 7v10c0 5.55 3.84 9.74 9 11 5.16-1.26 9-5.45 9-11V7l-10-5z"/></svg>'''
                }
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Static file not found'})
            }
        
        # Main page - Exact replica of local frontend
        if path == '/' and method == 'GET':
            html_content = '''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AutoU – Classificador de E‑mail</title>
  
  <!-- PWA Meta Tags -->
  <meta name="description" content="Sistema inteligente para classificação e resposta automática de e-mails">
  <meta name="theme-color" content="#4f46e5">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <meta name="apple-mobile-web-app-title" content="AutoU">
  
  <!-- PWA Icons -->
  <link rel="icon" type="image/svg+xml" href="/dev/static/icon.svg">
  
  <script src="https://cdn.tailwindcss.com"></script>
  <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
  <style>
    .dark-mode-toggle {
      position: fixed;
      top: 1rem;
      right: 1rem;
      z-index: 50;
      padding: 0.5rem;
      border-radius: 9999px;
      background-color: rgba(255, 255, 255, 0.9);
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
      transition: all 0.3s;
      cursor: pointer;
      border: none;
    }
    .dark-mode-toggle:hover {
      transform: scale(1.1);
      box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .dark .dark-mode-toggle {
      background-color: rgba(31, 41, 55, 0.9);
    }
    .card {
      transition: all 0.3s ease;
    }
    .card:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }
    .btn-modern {
      padding: 0.75rem 1.5rem;
      border-radius: 0.75rem;
      font-weight: 500;
      transition: all 0.2s;
      border: 1px solid transparent;
    }
    .btn-primary {
      background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
      color: white;
    }
    .btn-primary:hover:not(:disabled) {
      transform: translateY(-1px);
      box-shadow: 0 8px 25px rgba(79, 70, 229, 0.3);
    }
    .btn-outline {
      border-color: #e5e7eb;
      background: white;
      color: #374151;
    }
    .btn-outline:hover {
      background: #f9fafb;
      border-color: #d1d5db;
    }
    .badge {
      padding: 0.25rem 0.75rem;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 500;
    }
    .animate-fade-in {
      animation: fadeIn 0.5s ease-in;
    }
    .animate-slide-in {
      animation: slideIn 0.3s ease-out;
    }
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    @keyframes slideIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .dark {
      background-color: #0f172a;
      color: #f1f5f9;
    }
    .dark .bg-white {
      background-color: #1e293b !important;
    }
    .dark .text-slate-900 {
      color: #f1f5f9 !important;
    }
    .dark .text-slate-600 {
      color: #94a3b8 !important;
    }
    .dark .border {
      border-color: #334155 !important;
    }
    .dark textarea, .dark input {
      background-color: #334155;
      color: #f1f5f9;
      border-color: #475569;
    }
  </style>
</head>
<body class="bg-slate-50 text-slate-900" x-data="emailApp()" x-init="init()" :class="{ 'dark': darkMode }">
  <!-- Dark Mode Toggle -->
  <button class="dark-mode-toggle" @click="toggleDarkMode()" title="Alternar modo escuro">
    <span x-show="!darkMode">🌙</span>
    <span x-show="darkMode">☀️</span>
  </button>

  <!-- Auto-refresh Toggle -->
  <button @click="toggleAutoRefresh()" 
          class="fixed top-4 right-16 p-2 rounded-full transition-all duration-300 z-50 shadow-lg hover:shadow-xl transform hover:scale-110"
          :class="autoRefresh ? 'bg-green-500 text-white hover:bg-green-600' : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-600'"
          title="Auto-refresh: Atualiza resultados automaticamente">
    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
    </svg>
  </button>

  <main class="max-w-4xl mx-auto p-6 animate-fade-in">
    <header class="mb-6">
      <h1 class="text-2xl font-bold">AutoU – Classificador & Respostas</h1>
      <p class="text-sm text-slate-600">Envie um .txt/.pdf ou cole o texto. O sistema identifica <b>Produtivo</b> vs <b>Improdutivo</b> e sugere uma resposta.</p>
    </header>

    <section class="grid gap-4 md:grid-cols-2">
      <div class="bg-white rounded-xl shadow p-4 card">
        <h2 class="font-semibold mb-2">Entrada</h2>
        <div class="space-y-3">
          <textarea x-model="rawText" class="w-full h-40 border rounded-lg p-3 focus:outline-none" placeholder="Cole o texto do e‑mail aqui..."></textarea>
          <!-- Botões de Ação Principal -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-6">
            <input type="file" x-ref="file" class="hidden" @change="onFileChange" accept=".txt,.pdf" />
            <button class="btn-modern btn-outline" @click="$refs.file.click()" title="Selecionar arquivo de texto ou PDF para análise">
              Selecionar Arquivo
            </button>
            <button class="btn-modern btn-outline" @click="clearAll()" title="Limpar o texto digitado e arquivo selecionado (Ctrl+L)">
              Limpar
            </button>
            <button class="btn-modern btn-primary" @click="submit" :disabled="loading || (!rawText && !file)" title="Analisar o texto e gerar resposta sugerida (Ctrl+Enter)">
              <span x-show="!loading">Classificar & Sugerir</span>
              <span x-show="loading" class="flex items-center justify-center">
                <svg class="animate-spin -ml-1 mr-3 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processando...
              </span>
            </button>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow p-4 card">
        <h2 class="font-semibold mb-2">Resultado</h2>
        <template x-if="result">
          <div class="space-y-3 animate-slide-in">
            <!-- Categoria com gráfico de confiança -->
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <span class="badge animate-fade-in" :class="result.category==='Produtivo' ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'" x-text="result.category"></span>
                <span class="text-xs font-medium" :class="getConfidenceColor(result.category_score)" x-text="(result.category_score*100).toFixed(1)+'%'"></span>
              </div>
              
              <!-- Gráfico de confiança da categoria -->
              <div class="space-y-1">
                <div class="flex justify-between text-xs text-slate-500">
                  <span>Confiança da Classificação</span>
                  <span x-text="result.category_score >= 0.8 ? 'Alta' : result.category_score >= 0.6 ? 'Média' : 'Baixa'"></span>
                </div>
                <div class="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
                  <div class="h-full rounded-full transition-all duration-700 ease-out" 
                       :class="result.category_score >= 0.8 ? 'bg-gradient-to-r from-green-400 to-green-600' : 
                               result.category_score >= 0.6 ? 'bg-gradient-to-r from-yellow-400 to-yellow-600' : 
                               'bg-gradient-to-r from-red-400 to-red-600'" 
                       :style="`width: ${result.category_score*100}%`"></div>
                </div>
              </div>
            </div>
            
            <!-- Intenção com gráfico de confiança -->
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-slate-700">Intenção: <b x-text="result.intent"></b></span>
                <span class="text-xs font-medium" :class="getConfidenceColor(result.intent_score)" x-text="(result.intent_score*100).toFixed(1)+'%'"></span>
              </div>
              
              <!-- Gráfico de confiança da intenção -->
              <div class="space-y-1">
                <div class="flex justify-between text-xs text-slate-500">
                  <span>Confiança da Intenção</span>
                  <span x-text="result.intent_score >= 0.8 ? 'Alta' : result.intent_score >= 0.6 ? 'Média' : 'Baixa'"></span>
                </div>
                <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div class="h-full rounded-full transition-all duration-700 ease-out" 
                       :class="result.intent_score >= 0.8 ? 'bg-gradient-to-r from-blue-400 to-blue-600' : 
                               result.intent_score >= 0.6 ? 'bg-gradient-to-r from-purple-400 to-purple-600' : 
                               'bg-gradient-to-r from-gray-400 to-gray-600'" 
                       :style="`width: ${result.intent_score*100}%`"></div>
                </div>
              </div>
            </div>
            
            <!-- Resumo visual das métricas -->
            <div class="bg-slate-50 rounded-lg p-3 space-y-2">
              <h4 class="text-xs font-semibold text-slate-600 uppercase tracking-wide">Análise de Confiança</h4>
              <div class="grid grid-cols-2 gap-4 text-xs">
                <div class="text-center">
                  <div class="text-lg font-bold" :class="getConfidenceColor(result.category_score)" x-text="(result.category_score*100).toFixed(0)+'%'"></div>
                  <div class="text-slate-500">Categoria</div>
                </div>
                <div class="text-center">
                  <div class="text-lg font-bold" :class="getConfidenceColor(result.intent_score)" x-text="(result.intent_score*100).toFixed(0)+'%'"></div>
                  <div class="text-slate-500">Intenção</div>
                </div>
              </div>
              
              <!-- Indicador de qualidade geral -->
              <div class="pt-2 border-t border-slate-200">
                <div class="flex items-center justify-between">
                  <span class="text-xs text-slate-500">Qualidade da Análise:</span>
                  <span class="text-xs font-medium" 
                        :class="((result.category_score + result.intent_score) / 2) >= 0.8 ? 'text-green-600' : 
                                ((result.category_score + result.intent_score) / 2) >= 0.6 ? 'text-yellow-600' : 'text-red-600'"
                        x-text="((result.category_score + result.intent_score) / 2) >= 0.8 ? '🟢 Excelente' : 
                                ((result.category_score + result.intent_score) / 2) >= 0.6 ? '🟡 Boa' : '🔴 Baixa'"></span>
                </div>
              </div>
            </div>
            <div>
              <label class="text-sm text-slate-600">Resposta sugerida</label>
              <textarea class="w-full h-48 border rounded-lg p-3" x-model="result.suggested_reply"></textarea>
              <div class="flex gap-2 mt-2">
                <button class="btn-modern btn-outline" @click="copyReply" title="Copiar resposta sugerida para a área de transferência (Ctrl+Shift+C)" :disabled="!result?.suggested_reply">
                   Copiar
                 </button>
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

    <!-- Histórico -->
    <section class="mt-8" x-show="history.length > 0">
      <div class="bg-white rounded-xl shadow p-4 card">
        <div class="flex items-center justify-between mb-4">
          <h2 class="font-semibold">Histórico de Classificações</h2>
          <button class="btn-modern btn-outline text-xs" @click="clearHistory" title="Remover todas as classificações do histórico" :disabled="history.length === 0">
             Limpar Histórico
           </button>
        </div>
        <div class="space-y-2 max-h-64 overflow-y-auto">
          <template x-for="(entry, index) in history" :key="index">
            <div class="border rounded-lg p-3 hover:bg-slate-50 cursor-pointer transition-colors" @click="loadFromHistory(entry)">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <span class="badge text-xs" :class="entry.result.category==='Produtivo' ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'" x-text="entry.result.category"></span>
                  <span class="text-xs" :class="getConfidenceColor(entry.result.category_score)" x-text="(entry.result.category_score*100).toFixed(1)+'%'"></span>
                </div>
                <div class="flex items-center gap-2">
                  <div x-show="entry.autoGenerated" class="flex items-center text-xs text-green-600">
                    <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
                    </svg>
                    Auto
                  </div>
                  <span class="text-xs text-slate-400" x-text="formatTimestamp(entry.timestamp)"></span>
                </div>
              </div>
              <p class="text-sm text-slate-600 mt-1 truncate" x-text="entry.text.substring(0, 100) + (entry.text.length > 100 ? '...' : '')"></p>
            </div>
          </template>
        </div>
      </div>
    </section>

    <footer class="mt-6 text-xs text-slate-500">
      <p>🛈 Dica: sem <code>OPENAI_API_KEY</code>, o sistema usa templates. Com a chave, ele refina a resposta automaticamente.</p>
      <p class="mt-1">💡 Clique nos itens do histórico para recarregar uma classificação anterior.</p>
    </footer>
  </main>

  <!-- Notificação -->
  <div x-show="notification.show" x-transition:enter="transition ease-out duration-300" x-transition:enter-start="opacity-0 transform translate-y-2" x-transition:enter-end="opacity-100 transform translate-y-0" x-transition:leave="transition ease-in duration-200" x-transition:leave-start="opacity-100 transform translate-y-0" x-transition:leave-end="opacity-0 transform translate-y-2" class="fixed bottom-4 right-4 z-50 max-w-sm sm:max-w-md">
    <div class="rounded-lg px-4 py-3 shadow-lg max-w-sm" :class="notification.type === 'success' ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' : notification.type === 'error' ? 'bg-red-50 text-red-800 border border-red-200' : 'bg-blue-50 text-blue-800 border border-blue-200'">
      <div class="flex items-center">
        <div class="flex-shrink-0">
          <template x-if="notification.type === 'success'">
            <svg class="h-5 w-5 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
            </svg>
          </template>
          <template x-if="notification.type === 'error'">
            <svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
            </svg>
          </template>
          <template x-if="notification.type === 'info'">
            <svg class="h-5 w-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
            </svg>
          </template>
        </div>
        <div class="ml-3">
          <p class="text-sm font-medium" x-text="notification.message"></p>
        </div>
      </div>
    </div>
  </div>

  <script>
    function emailApp(){
      return {
        rawText: "",
        file: null,
        loading: false,
        result: null,
        darkMode: localStorage.getItem('darkMode') === 'true',
        history: JSON.parse(localStorage.getItem('emailHistory') || '[]'),
        autoRefresh: localStorage.getItem('autoRefresh') === 'true',
        refreshTimeout: null,
        lastProcessedText: '',
        notification: {
          show: false,
          message: "",
          type: "info" // success, error, info
        },
        
        init() {
          // Aplicar dark mode no carregamento
          if (this.darkMode) {
            document.documentElement.classList.add('dark');
          }
          
          // Configurar auto-refresh se habilitado
          if (this.autoRefresh) {
            this.setupAutoRefresh();
          }
        },
        
        setupAutoRefresh() {
          // Observar mudanças no texto
          this.$watch('rawText', (newText) => {
            if (this.autoRefresh && newText && newText.length > 10 && newText !== this.lastProcessedText) {
              // Cancelar timeout anterior
              if (this.refreshTimeout) {
                clearTimeout(this.refreshTimeout);
              }
              
              // Definir novo timeout para processar após 2 segundos de inatividade
              this.refreshTimeout = setTimeout(() => {
                if (!this.loading && newText.trim()) {
                  this.autoSubmit();
                }
              }, 2000);
            }
          });
        },
        
        toggleAutoRefresh() {
          this.autoRefresh = !this.autoRefresh;
          localStorage.setItem('autoRefresh', this.autoRefresh);
          
          if (this.autoRefresh) {
            this.setupAutoRefresh();
            this.showNotification('Auto-refresh ativado - resultados serão atualizados automaticamente', 'info');
          } else {
            if (this.refreshTimeout) {
              clearTimeout(this.refreshTimeout);
            }
            this.showNotification('Auto-refresh desativado', 'info');
          }
        },
        
        toggleDarkMode() {
          this.darkMode = !this.darkMode;
          localStorage.setItem('darkMode', this.darkMode);
          if (this.darkMode) {
            document.documentElement.classList.add('dark');
          } else {
            document.documentElement.classList.remove('dark');
          }
        },
        
        onFileChange(e){ 
          this.file = e.target.files[0] || null;
          if (this.file) {
            this.showNotification(`Arquivo selecionado: ${this.file.name}`, 'success');
          }
        },
        
        clearAll(){ 
          this.rawText = ""; 
          this.file = null; 
          this.result = null;
          const fileInput = document.querySelector('input[type="file"]');
          if (fileInput) {
            fileInput.value = '';
          }
          this.showNotification('Campos limpos com sucesso', 'success');
        },
        
        async autoSubmit() {
          // Versão silenciosa do submit para auto-refresh
          if (!this.rawText || this.rawText === this.lastProcessedText) {
            return;
          }
          
          this.loading = true;
          
          try {
            const response = await fetch('/dev/api/process', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ text: this.rawText })
            });
            
            if (!response.ok) {
              throw new Error('Erro no processamento');
            }
            
            const data = await response.json();
            this.result = this.convertToLocalFormat(data);
            this.lastProcessedText = this.rawText;
            
            // Salvar no histórico
            this.saveToHistory({
              text: this.rawText,
              result: this.result,
              timestamp: new Date().toISOString(),
              autoGenerated: true
            });
            
          } catch(err) {
            console.log('Auto-refresh error:', err.message);
          } finally {
            this.loading = false;
          }
        },
        
        async submit(){
          if (!this.rawText && !this.file) {
            this.showNotification('Por favor, insira um texto ou selecione um arquivo', 'error');
            return;
          }
          
          this.loading = true; 
          this.result = null;
          
          try{
            let textToProcess = this.rawText;
            
            // Se há arquivo, simular leitura (na AWS não temos processamento de arquivo real)
            if (this.file) {
              if (this.file.type === 'text/plain') {
                textToProcess = await this.readFileAsText(this.file);
              } else {
                this.showNotification('Apenas arquivos .txt são suportados na versão AWS', 'error');
                return;
              }
            }
            
            const response = await fetch('/dev/api/process', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ text: textToProcess })
            });
            
            if (!response.ok) {
              const error = await response.json();
              throw new Error(error.detail || error.error || 'Erro no processamento');
            }
            
            const data = await response.json();
            this.result = this.convertToLocalFormat(data);
            this.lastProcessedText = textToProcess;
            
            // Salvar no histórico
            this.saveToHistory({
              text: textToProcess,
              result: this.result,
              timestamp: new Date().toISOString(),
              autoGenerated: false
            });
            
            this.showNotification('Classificação realizada com sucesso!', 'success');
            
          } catch(err) {
            this.showNotification(`Erro: ${err.message}`, 'error');
          } finally {
            this.loading = false;
          }
        },
        
        readFileAsText(file) {
          return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = e => resolve(e.target.result);
            reader.onerror = reject;
            reader.readAsText(file);
          });
        },
        
        convertToLocalFormat(awsResult) {
          // Converter resultado da AWS para formato local
          const category = awsResult.classification === 'produtivo' ? 'Produtivo' : 'Improdutivo';
          const intent = this.mapCategoryToIntent(awsResult.category);
          
          return {
            category: category,
            category_score: awsResult.confidence,
            intent: intent,
            intent_score: awsResult.confidence * 0.9, // Simular score de intenção
            suggested_reply: this.generateSuggestedReply(awsResult),
            reply_source: 'Template AWS'
          };
        },
        
        mapCategoryToIntent(category) {
          const intentMap = {
            'reuniao': 'Agendamento',
            'aprovacao': 'Solicitação',
            'orcamento': 'Comercial',
            'status': 'Acompanhamento',
            'spam': 'Promocional',
            'geral': 'Informativo'
          };
          return intentMap[category] || 'Geral';
        },
        
        generateSuggestedReply(awsResult) {
          const replies = {
            'reuniao': 'Obrigado pelo convite. Confirmo minha presença na reunião. Aguardo mais detalhes sobre a agenda.',
            'aprovacao': 'Recebi sua solicitação e vou analisar. Retorno em breve com uma resposta.',
            'orcamento': 'Obrigado pelo interesse. Vou preparar uma proposta detalhada e envio em breve.',
            'status': 'Obrigado pela atualização. Vou acompanhar o andamento e qualquer dúvida estarei à disposição.',
            'spam': 'Não tenho interesse nesta oferta no momento. Obrigado.',
            'geral': 'Obrigado pelo contato. Recebi sua mensagem e vou analisar.'
          };
          return replies[awsResult.category] || 'Obrigado pelo contato. Recebi sua mensagem.';
        },
        
        saveToHistory(entry) {
          this.history.unshift(entry);
          if (this.history.length > 50) {
            this.history = this.history.slice(0, 50);
          }
          localStorage.setItem('emailHistory', JSON.stringify(this.history));
        },
        
        loadFromHistory(entry) {
          this.rawText = entry.text;
          this.result = entry.result;
          this.showNotification('Classificação carregada do histórico', 'info');
        },
        
        clearHistory() {
          this.history = [];
          localStorage.removeItem('emailHistory');
          this.showNotification('Histórico limpo com sucesso', 'success');
        },
        
        copyReply() {
          if (this.result?.suggested_reply) {
            navigator.clipboard.writeText(this.result.suggested_reply).then(() => {
              this.showNotification('Resposta copiada para a área de transferência', 'success');
            }).catch(() => {
              this.showNotification('Erro ao copiar resposta', 'error');
            });
          }
        },
        
        getConfidenceColor(score) {
          if (score >= 0.8) return 'text-green-600';
          if (score >= 0.6) return 'text-yellow-600';
          return 'text-red-600';
        },
        
        formatTimestamp(timestamp) {
          return new Date(timestamp).toLocaleString('pt-BR', {
            day: '2-digit',
            month: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
          });
        },
        
        showNotification(message, type = 'info') {
          this.notification.message = message;
          this.notification.type = type;
          this.notification.show = true;
          
          setTimeout(() => {
            this.notification.show = false;
          }, 4000);
        }
      }
    }
  </script>
</body>
</html>'''
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'text/html'},
                'body': html_content
            }
        
        # Process text endpoint - Enhanced to match local API
        if path == '/api/process' and method == 'POST':
            # Parse request body
            body = event.get('body', '{}')
            if isinstance(body, str):
                try:
                    data = json.loads(body)
                except json.JSONDecodeError:
                    return {
                        'statusCode': 400,
                        'headers': headers,
                        'body': json.dumps({'error': 'Invalid JSON in request body'})
                    }
            else:
                data = body
            
            text = data.get('text', '').strip()
            if not text:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'error': 'Text is required'})
                }
            
            # Enhanced rule-based classification matching local logic
            text_lower = text.lower()
            
            if any(word in text_lower for word in ['reunião', 'meeting', 'encontro', 'agenda', 'convite']):
                classification = "produtivo"
                category = "reuniao"
                confidence = 0.85
                message = "Email classificado como reunião/encontro"
            elif any(word in text_lower for word in ['aprovação', 'aprovar', 'autorização', 'autorizar', 'permissão']):
                classification = "produtivo"
                category = "aprovacao"
                confidence = 0.80
                message = "Email classificado como solicitação de aprovação"
            elif any(word in text_lower for word in ['orçamento', 'proposta', 'cotação', 'valor', 'preço', 'comercial']):
                classification = "produtivo"
                category = "orcamento"
                confidence = 0.75
                message = "Email classificado como orçamento/proposta"
            elif any(word in text_lower for word in ['status', 'andamento', 'progresso', 'atualização', 'relatório']):
                classification = "produtivo"
                category = "status"
                confidence = 0.70
                message = "Email classificado como atualização de status"
            elif any(word in text_lower for word in ['spam', 'promoção', 'oferta', 'desconto', 'grátis', 'ganhe']):
                classification = "improdutivo"
                category = "spam"
                confidence = 0.90
                message = "Email classificado como spam/promoção"
            else:
                classification = "produtivo"
                category = "geral"
                confidence = 0.60
                message = "Email classificado como produtivo (classificação geral)"
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'classification': classification,
                    'confidence': confidence,
                    'category': category,
                    'message': message
                })
            }
        
        # Default 404 response
        return {
            'statusCode': 404,
            'headers': headers,
            'body': json.dumps({'error': 'Not Found', 'path': path, 'method': method})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': 'Internal Server Error',
                'message': str(e),
                'service': 'autou-email-classifier'
            })
        }

# For serverless compatibility
app = lambda_handler