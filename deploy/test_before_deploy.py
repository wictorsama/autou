#!/usr/bin/env python3
"""
Script de teste para validar aplicação antes do deploy AWS
Testa todas as funcionalidades críticas
"""

import os
import sys
import json
import time
import requests
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

# Adicionar diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

class DeploymentTester:
    """Testa funcionalidades antes do deploy"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = []
        self.server_process = None
    
    def log_result(self, test_name: str, success: bool, message: str = "", duration: float = 0):
        """Registra resultado do teste"""
        status = "✅ PASS" if success else "❌ FAIL"
        duration_str = f" ({duration:.2f}s)" if duration > 0 else ""
        
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'duration': duration
        }
        
        self.results.append(result)
        print(f"{status} {test_name}{duration_str}")
        if message:
            print(f"    {message}")
    
    def start_server(self) -> bool:
        """Inicia servidor local para testes"""
        print("🚀 Iniciando servidor local...")
        
        try:
            # Verificar se já está rodando
            response = requests.get(f"{self.base_url}/health", timeout=2)
            if response.status_code == 200:
                print("✅ Servidor já está rodando")
                return True
        except:
            pass
        
        # Iniciar servidor
        try:
            self.server_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", 
                "app.main:app", 
                "--host", "0.0.0.0", 
                "--port", "8000"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Aguardar servidor iniciar
            for i in range(30):  # 30 segundos timeout
                try:
                    response = requests.get(f"{self.base_url}/health", timeout=2)
                    if response.status_code == 200:
                        print("✅ Servidor iniciado com sucesso")
                        return True
                except:
                    time.sleep(1)
            
            print("❌ Timeout ao iniciar servidor")
            return False
            
        except Exception as e:
            print(f"❌ Erro ao iniciar servidor: {e}")
            return False
    
    def stop_server(self):
        """Para servidor local"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
            print("🛑 Servidor parado")
    
    def test_health_endpoint(self) -> bool:
        """Testa endpoint de health"""
        start_time = time.time()
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                status = data.get('status')
                if status in ['healthy', 'ok']:  # Aceitar ambos os valores
                    self.log_result("Health Check", True, f"Status: {status}", duration)
                    return True
                else:
                    self.log_result("Health Check", False, f"Status inválido: {status}", duration)
                    return False
            else:
                self.log_result("Health Check", False, f"Status code: {response.status_code}", duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            self.log_result("Health Check", False, f"Erro: {str(e)}", duration)
            return False
    
    def test_static_files(self) -> bool:
        """Testa servir arquivos estáticos"""
        start_time = time.time()
        
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            duration = time.time() - start_time
            
            if response.status_code == 200 and "AutoU" in response.text:
                self.log_result("Static Files", True, "Index.html carregado", duration)
                return True
            else:
                self.log_result("Static Files", False, f"Status: {response.status_code}", duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            self.log_result("Static Files", False, f"Erro: {str(e)}", duration)
            return False
    
    def test_email_classification(self) -> bool:
        """Testa classificação de email"""
        start_time = time.time()
        
        test_text = "Reunião importante amanhã. Olá, precisamos nos reunir amanhã às 14h para discutir o projeto. Por favor, confirme sua presença."
        
        try:
            # Usar FormData como a aplicação espera
            form_data = {'text': test_text}
            response = requests.post(
                f"{self.base_url}/api/process",
                data=form_data,
                timeout=30
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'category' in data and 'intent' in data:
                    category = data['category']
                    intent = data['intent']
                    self.log_result(
                        "Email Classification", 
                        True, 
                        f"Categoria: {category}, Intenção: {intent}", 
                        duration
                    )
                    return True
                else:
                    self.log_result("Email Classification", False, "Resposta inválida", duration)
                    return False
            else:
                self.log_result("Email Classification", False, f"Status: {response.status_code}", duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            self.log_result("Email Classification", False, f"Erro: {str(e)}", duration)
            return False
    
    def test_suggestion_generation(self) -> bool:
        """Testa geração de sugestões (incluído no processo)"""
        start_time = time.time()
        
        test_text = "Preciso do status do chamado #12345. Quando será resolvido?"
        
        try:
            # A sugestão é gerada junto com a classificação no /api/process
            form_data = {'text': test_text}
            response = requests.post(
                f"{self.base_url}/api/process",
                data=form_data,
                timeout=30
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'suggested_reply' in data and data['suggested_reply']:
                    reply_length = len(data['suggested_reply'])
                    reply_source = data.get('reply_source', 'unknown')
                    self.log_result(
                        "Suggestion Generation", 
                        True, 
                        f"Resposta gerada ({reply_length} chars, fonte: {reply_source})", 
                        duration
                    )
                    return True
                else:
                    self.log_result("Suggestion Generation", False, "Nenhuma sugestão gerada", duration)
                    return False
            else:
                self.log_result("Suggestion Generation", False, f"Status: {response.status_code}", duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            self.log_result("Suggestion Generation", False, f"Erro: {str(e)}", duration)
            return False
    
    def test_memory_usage(self) -> bool:
        """Testa uso de memória através do health endpoint"""
        start_time = time.time()
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                memory_info = data.get('memory', {})
                memory_mb = memory_info.get('rss', 0)
                
                # Verificar se está dentro de limites aceitáveis (< 2GB)
                if memory_mb < 2048:
                    self.log_result(
                        "Memory Usage", 
                        True, 
                        f"RSS: {memory_mb:.1f}MB", 
                        duration
                    )
                    return True
                else:
                    self.log_result(
                        "Memory Usage", 
                        False, 
                        f"Uso alto: {memory_mb:.1f}MB", 
                        duration
                    )
                    return False
            else:
                self.log_result("Memory Usage", False, f"Status: {response.status_code}", duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            self.log_result("Memory Usage", False, f"Erro: {str(e)}", duration)
            return False
    
    def test_file_upload(self) -> bool:
        """Testa upload de arquivo"""
        start_time = time.time()
        
        # Criar arquivo de teste
        test_content = "Subject: Teste\nFrom: test@test.com\n\nEste é um email de teste para classificação."
        
        try:
            files = {'file': ('test.txt', test_content, 'text/plain')}
            response = requests.post(
                f"{self.base_url}/api/process",
                files=files,
                timeout=20
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'category' in data and 'intent' in data:
                    category = data['category']
                    intent = data['intent']
                    self.log_result(
                        "File Upload", 
                        True, 
                        f"Arquivo processado: {category} - {intent}", 
                        duration
                    )
                    return True
                else:
                    self.log_result("File Upload", False, "Resposta inválida", duration)
                    return False
            else:
                self.log_result("File Upload", False, f"Status: {response.status_code}", duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            self.log_result("File Upload", False, f"Erro: {str(e)}", duration)
            return False
    
    def run_all_tests(self) -> bool:
        """Executa todos os testes"""
        print("🧪 AutoU Email Classifier - Testes de Deploy")
        print("=" * 50)
        
        # Iniciar servidor se necessário
        if not self.start_server():
            return False
        
        try:
            # Lista de testes
            tests = [
                self.test_health_endpoint,
                self.test_static_files,
                self.test_memory_usage,
                self.test_email_classification,
                self.test_suggestion_generation,
                self.test_file_upload
            ]
            
            # Executar testes
            passed = 0
            total = len(tests)
            
            for test in tests:
                if test():
                    passed += 1
                time.sleep(1)  # Pausa entre testes
            
            # Relatório final
            print("\n" + "=" * 50)
            print(f"📊 Resultados: {passed}/{total} testes passaram")
            
            if passed == total:
                print("🎉 Todos os testes passaram! Pronto para deploy.")
                return True
            else:
                print(f"⚠️ {total - passed} testes falharam. Verifique os problemas antes do deploy.")
                return False
                
        finally:
            # Parar servidor se foi iniciado por este script
            if self.server_process:
                self.stop_server()
    
    def generate_report(self) -> str:
        """Gera relatório detalhado"""
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_tests': len(self.results),
            'passed': sum(1 for r in self.results if r['success']),
            'failed': sum(1 for r in self.results if not r['success']),
            'results': self.results
        }
        
        return json.dumps(report, indent=2)

def main():
    """Função principal"""
    # Verificar se estamos no diretório correto
    if not os.path.exists('app/main.py'):
        print("❌ Execute este script no diretório raiz do projeto")
        sys.exit(1)
    
    # Executar testes
    tester = DeploymentTester()
    success = tester.run_all_tests()
    
    # Salvar relatório
    report = tester.generate_report()
    with open('deploy/test_report.json', 'w') as f:
        f.write(report)
    
    print(f"\n📄 Relatório salvo em: deploy/test_report.json")
    
    # Exit code
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()