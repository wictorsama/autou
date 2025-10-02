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