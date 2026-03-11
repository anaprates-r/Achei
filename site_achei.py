import subprocess
import os
import sys
import shutil
from pathlib import Path

def preparar_e_rodar():
    diretorio_raiz = Path.cwd()
    
    # 1. Definir o caminho conforme o SO
    if os.name == 'nt':
        python_venv = diretorio_raiz / "venv" / "Scripts" / "python.exe"
        comando_npm = "npm.cmd"
    else:
        python_venv = diretorio_raiz / "venv" / "bin" / "python"
        comando_npm = "npm"

    # --- BLOCO TRY-EXCEPT PARA A VENV ---
    try:
        print("🔍 Verificando integridade do ambiente virtual...")
        # Tenta rodar um comando simples usando o python da venv
        subprocess.run([str(python_venv), "--version"], check=True, capture_output=True)
        print("✅ Ambiente virtual encontrado e funcional.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ Venv não encontrada ou corrompida. Criando uma nova...")
        
        # Se a pasta existir mas estiver quebrada, removemos para evitar conflitos
        pasta_venv = diretorio_raiz / "venv"
        if pasta_venv.exists():
            shutil.rmtree(pasta_venv) # Apaga a pasta inteira
            
        # Cria a nova venv
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✨ Nova venv criada com sucesso.")

    # --- INSTALAÇÃO DE DEPENDÊNCIAS ---
    print("📦 Atualizando pacotes (Backend)...")
    try:
        subprocess.run([str(python_venv), "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([str(python_venv), "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        
        print("📦 Instalando dependências (Frontend)...")
        frontend_path = diretorio_raiz / "frontend"
        subprocess.run([comando_npm, "install"], cwd=str(frontend_path), shell=(os.name == 'nt'), check=True)
    except Exception as e:
        print(f"❌ Erro na instalação: {e}")
        return

    # --- EXECUÇÃO SIMULTÂNEA ---
    print("\n🚀 Iniciando servidores...")
    backend_path = diretorio_raiz / "backend"
    frontend_path = diretorio_raiz / "frontend"

    # Lança o Backend
    p_back = subprocess.Popen([str(python_venv), "main.py"], cwd=str(backend_path))
    
    # Lança o Frontend
    p_front = subprocess.Popen([comando_npm, "run", "dev"], cwd=str(frontend_path), shell=(os.name == 'nt'))

    try:
        p_back.wait()
        p_front.wait()
    except KeyboardInterrupt:
        print("\n🛑 Encerrando processos...")
        p_back.terminate()
        p_front.terminate()

if __name__ == "__main__":
    preparar_e_rodar()