#!/bin/bash
# Script para criar pacotes Linux (deb, rpm)
# Deve ser executado após o PyInstaller ter criado os arquivos em dist/WaterAnalyser

set -e  # Encerra em caso de erro

# Variáveis
APP_NAME="wateranalyser"
APP_VERSION="1.0.0"
APP_DESCRIPTION="Ferramenta para análise de qualidade da água"
MAINTAINER="seu.email@example.com"
DIST_PATH="../../../dist/WaterAnalyser"
OUTPUT_DIR="../../../dist"
DESKTOP_FILE="${APP_NAME}.desktop"

# Verifica se o PyInstaller criou os arquivos corretamente
if [ ! -d "$DIST_PATH" ]; then
    echo "Erro: O diretório $DIST_PATH não foi encontrado."
    echo "Certifique-se de executar o PyInstaller primeiro."
    exit 1
fi

# Verifica se os pacotes necessários estão instalados
check_and_install() {
    if ! command -v $1 &> /dev/null; then
        echo "Instalando $1..."
        sudo apt-get update
        sudo apt-get install -y $1 || {
            echo "Erro ao instalar $1. Verifique se você está usando uma distribuição baseada em Debian."
            exit 1
        }
    fi
}

check_and_install "fpm"

# Crie um arquivo .desktop para o aplicativo
create_desktop_file() {
    cat > "${DESKTOP_FILE}" << EOF
[Desktop Entry]
Name=WaterAnalyser
Comment=${APP_DESCRIPTION}
Exec=/usr/local/bin/${APP_NAME}/${APP_NAME}
Icon=/usr/local/share/icons/${APP_NAME}.png
Terminal=false
Type=Application
Categories=Science;Education;
EOF
}

# Crie o ícone e o diretório temporário
create_temp_structure() {
    mkdir -p temp/usr/local/bin/${APP_NAME}
    mkdir -p temp/usr/local/share/icons
    mkdir -p temp/usr/local/share/applications
    
    # Copie os arquivos compilados
    cp -r "${DIST_PATH}"/* temp/usr/local/bin/${APP_NAME}/
    
    # Copie o ícone
    cp "../../../resources/WaterAnalises.ico" temp/usr/local/share/icons/${APP_NAME}.png
    
    # Copie o arquivo .desktop
    cp "${DESKTOP_FILE}" temp/usr/local/share/applications/
}

# Crie pacotes usando fpm
create_packages() {
    echo "Criando pacote DEB..."
    fpm -s dir -t deb -n ${APP_NAME} -v ${APP_VERSION} \
        --description "${APP_DESCRIPTION}" \
        --maintainer "${MAINTAINER}" \
        -C temp \
        --after-install "after_install.sh" \
        -p "${OUTPUT_DIR}/${APP_NAME}_${APP_VERSION}.deb" \
        .

    echo "Criando pacote RPM..."
    fpm -s dir -t rpm -n ${APP_NAME} -v ${APP_VERSION} \
        --description "${APP_DESCRIPTION}" \
        --maintainer "${MAINTAINER}" \
        -C temp \
        --after-install "after_install.sh" \
        -p "${OUTPUT_DIR}/${APP_NAME}_${APP_VERSION}.rpm" \
        .
}

# Script post-instalação
create_after_install() {
    cat > "after_install.sh" << EOF
#!/bin/bash
# Crie um link simbólico para facilitar a execução
ln -sf /usr/local/bin/${APP_NAME}/${APP_NAME} /usr/local/bin/${APP_NAME}
# Atualize o cache de ícones e aplicativos
update-desktop-database /usr/local/share/applications || true
gtk-update-icon-cache /usr/local/share/icons || true
EOF
    chmod +x "after_install.sh"
}

# Execute o processo de empacotamento
main() {
    echo "Preparando pacotes Linux para ${APP_NAME} v${APP_VERSION}..."
    
    # Crie um arquivo desktop
    create_desktop_file
    
    # Crie um script post-instalação
    create_after_install
    
    # Crie a estrutura temporária
    create_temp_structure
    
    # Crie os pacotes
    create_packages
    
    # Limpe os arquivos temporários
    rm -rf temp
    rm -f "${DESKTOP_FILE}"
    rm -f "after_install.sh"
    
    echo "Pacotes Linux criados com sucesso em ${OUTPUT_DIR}!"
}

main