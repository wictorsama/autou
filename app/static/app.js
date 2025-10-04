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
    confirmDialog: {
      show: false,
      title: "",
      message: "",
      onConfirm: null,
      onReject: null,
      confirm() {
        if (this.onConfirm) this.onConfirm();
        this.hide();
      },
      reject() {
        if (this.onReject) this.onReject();
        this.hide();
      },
      hide() {
        this.show = false;
        this.title = "";
        this.message = "";
        this.onConfirm = null;
        this.onReject = null;
      }
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
      
      // Configurar atalhos de teclado
      this.setupKeyboardShortcuts();
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
      // Verificar se há conteúdo no textarea e nas variáveis
      const textArea = document.querySelector('textarea');
      const textAreaValue = textArea ? textArea.value : '';
      
      const hasContent = this.rawText || this.file || this.result || textAreaValue;
      
      if (hasContent) {
        this.showConfirm(
          'Limpar todos os campos',
          'Tem certeza que deseja limpar todos os campos? Esta ação não pode ser desfeita.',
          () => {
            // Limpar as variáveis do Alpine.js primeiro
            this.rawText = ""; 
            this.file = null; 
            this.result = null;
            
            // Forçar limpeza do textarea e disparar evento para Alpine.js detectar
            if (textArea) {
              textArea.value = '';
              // Disparar evento de input para que o Alpine.js detecte a mudança
              textArea.dispatchEvent(new Event('input', { bubbles: true }));
            }
            
            // Limpar também o input de arquivo
            const fileInput = document.querySelector('input[type="file"]');
            if (fileInput) {
              fileInput.value = '';
              // Disparar evento de change para o input de arquivo
              fileInput.dispatchEvent(new Event('change', { bubbles: true }));
            }
            
            // Forçar atualização do Alpine.js
            this.$nextTick(() => {
              // Garantir que a UI foi atualizada completamente
              this.$el.dispatchEvent(new CustomEvent('alpine:updated'));
            });
            
            this.showNotification('Campos limpos com sucesso', 'success');
          }
        );
      } else {
        this.showNotification('Não há conteúdo para limpar', 'info');
      }
    },
    
    async autoSubmit() {
      // Versão silenciosa do submit para auto-refresh
      if (!this.rawText || this.rawText === this.lastProcessedText) {
        return;
      }
      
      this.loading = true;
      
      try {
        const form = new FormData();
        form.append('text', this.rawText);
        
        const res = await fetch('/api/process', { method:'POST', body: form });
        if(!res.ok){ 
          const e = await res.json(); 
          throw new Error(e.detail || 'Erro no processamento'); 
        }
        
        this.result = await res.json();
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
        const form = new FormData();
        if(this.file){ form.append('file', this.file); }
        if(this.rawText && !this.file){ form.append('text', this.rawText); }
        
        const res = await fetch('/api/process', { method:'POST', body: form });
        if(!res.ok){ 
          const e = await res.json(); 
          throw new Error(e.detail || 'Erro no processamento'); 
        }
        
        this.result = await res.json();
        
        // Salvar no histórico
        this.saveToHistory({
          text: this.rawText || this.file?.name || '',
          result: this.result,
          timestamp: new Date().toISOString()
        });
        
        this.showNotification('Email classificado com sucesso!', 'success');
        
        // Limpar campos após processamento bem-sucedido
        setTimeout(() => {
          this.rawText = "";
          this.file = null;
          // Limpar também o input de arquivo
          const fileInput = document.querySelector('input[type="file"]');
          if (fileInput) {
            fileInput.value = '';
          }
          console.log('Campos limpos automaticamente');
        }, 500);
        
      }catch(err){
        this.showNotification(err.message, 'error');
      }finally{
        this.loading = false;
      }
    },
    
    async copyReply(){
      if(this.result?.suggested_reply){
        try {
          await navigator.clipboard.writeText(this.result.suggested_reply);
          this.showNotification('Resposta copiada para a área de transferência!', 'success');
        } catch (err) {
          this.showNotification('Erro ao copiar resposta', 'error');
        }
      }
    },
    
    saveToHistory(entry) {
      this.history.unshift(entry);
      // Manter apenas os últimos 10 itens
      if (this.history.length > 10) {
        this.history = this.history.slice(0, 10);
      }
      localStorage.setItem('emailHistory', JSON.stringify(this.history));
    },
    
    clearHistory() {
      if (this.history.length === 0) {
        this.showNotification('Histórico já está vazio', 'info');
        return;
      }
      
      this.showConfirm(
        'Limpar histórico',
        'Tem certeza que deseja limpar todo o histórico? Esta ação não pode ser desfeita.',
        () => {
          this.history = [];
          localStorage.removeItem('emailHistory');
          this.showNotification('Histórico limpo com sucesso', 'success');
        }
      );
    },
    
    loadFromHistory(entry) {
      this.rawText = entry.text;
      this.result = entry.result;
      this.showNotification('Item carregado do histórico', 'info');
    },
    
    showNotification(message, type = 'info') {
      this.notification.message = message;
      this.notification.type = type;
      this.notification.show = true;
      
      // Auto-hide após 3 segundos
      setTimeout(() => {
        this.notification.show = false;
      }, 3000);
    },

    showConfirm(title, message, onConfirm, onReject = null) {
      this.confirmDialog.title = title;
      this.confirmDialog.message = message;
      this.confirmDialog.onConfirm = onConfirm;
      this.confirmDialog.onReject = onReject;
      this.confirmDialog.show = true;
    },
    
    getConfidenceColor(score) {
      if (score >= 0.8) return 'text-green-600';
      if (score >= 0.6) return 'text-yellow-600';
      return 'text-red-600';
    },
    
    formatTimestamp(timestamp) {
      return new Date(timestamp).toLocaleString('pt-BR');
    },

    setupKeyboardShortcuts() {
      document.addEventListener('keydown', (e) => {
        // Ctrl+Enter para classificar
        if (e.ctrlKey && e.key === 'Enter') {
          e.preventDefault();
          if (!this.loading && (this.rawText || this.file)) {
            this.submit();
          }
        }
        // Ctrl+L para limpar
        if (e.ctrlKey && e.key === 'l') {
          e.preventDefault();
          if (this.rawText || this.file || this.result) {
            this.clearAll();
          }
        }
        // Ctrl+C para copiar (quando há resposta sugerida)
        if (e.ctrlKey && e.key === 'c' && e.shiftKey) {
          e.preventDefault();
          if (this.result?.suggested_reply) {
            this.copyReply();
          }
        }
      });
    }
  }
}