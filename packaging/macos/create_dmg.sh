#!/bin/bash
# Script para criar um arquivo DMG para macOS
# Deve ser executado após o PyInstaller ter criado o arquivo .app

set -e  # Encerra em caso de erro

# Variáveis
APP_NAME="WaterAnalyser"
DMG_NAME="${APP_NAME}_1.0.0"
APP_PATH="../../../dist/${APP_NAME}.app"
DMG_PATH="../../../dist/${DMG_NAME}.dmg"
VOLUME_NAME="${APP_NAME}"

# Verifica se o aplicativo foi criado
if [ ! -d "$APP_PATH" ]; then
    echo "Erro: O aplicativo não foi encontrado em $APP_PATH"
    echo "Certifique-se de executar o PyInstaller primeiro."
    exit 1
fi

# Instala create-dmg se necessário
if ! command -v create-dmg &> /dev/null; then
    echo "Instalando create-dmg..."
    brew install create-dmg || {
        echo "Erro ao instalar create-dmg. Verifique se o Homebrew está instalado."
        echo "Para instalar o Homebrew, visite: https://brew.sh/"
        exit 1
    }
fi

# Remove qualquer DMG antigo
if [ -f "$DMG_PATH" ]; then
    echo "Removendo DMG antigo..."
    rm "$DMG_PATH"
fi

# Cria o DMG
echo "Criando DMG para $APP_NAME..."
create-dmg \
    --volname "$VOLUME_NAME" \
    --volicon "$APP_PATH/Contents/Resources/WaterAnalises.ico" \
    --window-pos 200 120 \
    --window-size 600 400 \
    --icon-size 100 \
    --icon "$APP_NAME.app" 175 200 \
    --app-drop-link 425 200 \
    --no-internet-enable \
    "$DMG_PATH" \
    "$APP_PATH"

echo "DMG criado com sucesso: $DMG_PATH"