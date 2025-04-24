#!/usr/bin/env python3
import os
import platform
import shutil
import subprocess
import sys

def clean_build_directories():
    """Remove diretórios de build anteriores."""
    directories = ['build', 'dist']
    for directory in directories:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            print(f"Removido diretório: {directory}")

def update_spec_hiddenimports(spec_path, new_hiddenimports):
    """Atualiza os hiddenimports no arquivo .spec antes do build."""
    if not os.path.exists(spec_path):
        print(f"Arquivo .spec não encontrado em {spec_path}")
        return
    
    with open(spec_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    updated_lines = []
    inside_analysis = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("a = Analysis("):
            inside_analysis = True

        if inside_analysis and stripped.startswith("hiddenimports="):
            # Substitui os hiddenimports por novos
            hiddenimports_line = f"    hiddenimports={new_hiddenimports},\n"
            updated_lines.append(hiddenimports_line)
            inside_analysis = False
        else:
            updated_lines.append(line)

    with open(spec_path, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)

    print("Arquivo .spec atualizado com novos hiddenimports.")

def run_pyinstaller(spec_file='pyinstaller_spec.spec'):
    """Executa o PyInstaller com o arquivo spec fornecido."""
    print("Executando PyInstaller...")
    subprocess.run(['pyinstaller', '--clean', spec_file], check=True)
    print("Build PyInstaller concluído com sucesso!")

def create_windows_installer():
    """Cria instalador para Windows usando o NSIS."""
    if platform.system() != 'Windows':
        print("Pulando criação do instalador Windows (não estamos no Windows)")
        return
    
    print("Criando instalador Windows...")
    try:
        makensis = r'"C:\Program Files (x86)\NSIS\makensis.exe"'
        subprocess.run(f'{makensis} packaging/windows/installer.nsi', shell=True, check=True)
        print("Instalador Windows criado com sucesso!")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Erro ao criar instalador Windows. Verifique se o NSIS está instalado.")

def create_macos_package():
    """Cria pacote DMG para macOS."""
    if platform.system() != 'Darwin':
        print("Pulando criação do pacote macOS (não estamos no macOS)")
        return
    
    print("Criando pacote macOS...")
    try:
        subprocess.run(['bash', 'packaging/macos/create_dmg.sh'], check=True)
        print("Pacote macOS criado com sucesso!")
    except subprocess.SubprocessError:
        print("Erro ao criar pacote macOS.")

def create_linux_package():
    """Cria pacote para Linux."""
    if platform.system() != 'Linux':
        print("Pulando criação do pacote Linux (não estamos no Linux)")
        return
    
    print("Criando pacote Linux...")
    try:
        subprocess.run(['bash', 'packaging/linux/create_package.sh'], check=True)
        print("Pacote Linux criado com sucesso!")
    except subprocess.SubprocessError:
        print("Erro ao criar pacote Linux.")

def create_platform_package():
    """Cria pacote específico para a plataforma atual."""
    system = platform.system()
    if system == 'Windows':
        create_windows_installer()
    elif system == 'Darwin':
        create_macos_package()
    elif system == 'Linux':
        create_linux_package()
    else:
        print(f"Sistema não suportado: {system}")

def main():
    # Verifica se PyInstaller está instalado
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller não encontrado. Instalando...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
    
    # Verifica se todas as dependências estão instaladas
    print("Verificando dependências...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
    
    # Cria diretórios de empacotamento se não existirem
    os.makedirs('packaging/windows', exist_ok=True)
    os.makedirs('packaging/macos', exist_ok=True)
    os.makedirs('packaging/linux', exist_ok=True)
    
    # Limpa diretórios de builds anteriores
    clean_build_directories()

    # Atualiza os hiddenimports no .spec antes do build
    update_spec_hiddenimports(
        'pyinstaller_spec.spec',
        "['scipy._lib.array_api_compat.numpy.fft']"
    )

    # Executa PyInstaller
    run_pyinstaller()

    # Cria pacote específico da plataforma
    create_platform_package()

    print("Processo de build concluído!")

if __name__ == "__main__":
    main()