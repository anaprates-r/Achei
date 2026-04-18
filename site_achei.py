import subprocess
import os
import sys
import signal
from pathlib import Path

def site_achei():
    raiz = Path(__file__).parent.absolute()
    backend_path = raiz / "backend"
    frontend_path = raiz / "frontend"
    venv_path = raiz / ".venv"
    
    # Define binários conforme o SO
    if os.name == "nt":
        python_venv = venv_path / "Scripts" / "python.exe"
        pip_venv = venv_path / "Scripts" / "pip.exe"
        creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP # Para Windows
    else:
        python_venv = venv_path / "bin" / "python"
        pip_venv = venv_path / "bin" / "pip"
        creation_flags = 0

    # 1. Preparação do Ambiente
    if not venv_path.exists():
        print("Criando venv...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)

    print("Instalando dependências do backend...")
    subprocess.run([str(pip_venv), "install", "-r", str(raiz / "requirements.txt")], check=True)

    processos = []

    try:
        # 2. Rodar Backend
        print("Iniciando Backend...")
        proc_back = subprocess.Popen(
            [str(python_venv), "main.py"], 
            cwd=backend_path,
            # No Unix, cria grupo de processo para matar filhos depois
            start_new_session=(os.name != "nt") 
        )
        processos.append(proc_back)

        # 3. Rodar Frontend
        if frontend_path.exists():
            if not (frontend_path / "node_modules").exists():
                print("Instalando dependências do frontend...")
                subprocess.run(["npm", "install"], cwd=frontend_path, check=True, shell=(os.name == "nt"))
            
            print("Iniciando Frontend...")
            # shell=True é recomendável para comandos npm no Windows
            proc_front = subprocess.Popen(
                ["npm", "run", "dev"], 
                cwd=frontend_path, 
                shell=(os.name == "nt"),
                start_new_session=(os.name != "nt")
            )
            processos.append(proc_front)

        print("\n--- TUDO RODANDO ---")
        print("Pressione Ctrl+C para encerrar.")
        
        # Aguarda os processos
        for p in processos:
            p.wait()

    except KeyboardInterrupt:
        print("\nEncerrando servidores...")
    
    finally:
        for p in processos:
            try:
                if os.name == "nt":
                    # taskkill /T fecha toda a árvore de processos
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True)
                else:
                    # Mata o grupo de processos (PID negativo no kill faz isso)
                    os.killpg(os.getpgid(p.pid), signal.SIGTERM)
            except Exception:
                p.terminate()
        print("Ambiente limpo. Até logo!")

if __name__ == "__main__":
    site_achei()