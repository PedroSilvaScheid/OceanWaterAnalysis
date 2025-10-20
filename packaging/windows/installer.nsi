; Script de instalação para o WaterAnalyser
; Gerado para o projeto de análise de água

!include "MUI2.nsh"
!include "FileFunc.nsh"
!include "nsDialogs.nsh"
!include "LogicLib.nsh"

; Definições do app
!define APPNAME "WaterAnalyser"
!define APPVERSION "1.0.0"
!define COMPANYNAME "YourCompany"
!define DESCRIPTION "Ferramenta para análise de qualidade da água"

; Define o nome do aplicativo globalmente (usado em todas as páginas do instalador)
Name "${APPNAME}"

; Pasta de instalação padrão
InstallDir "$PROGRAMFILES\${APPNAME}"

; Nome do arquivo de saída do instalador
OutFile "..\..\..\dist\${APPNAME}_Setup_${APPVERSION}.exe"

; Solicitar privilégios de administrador
RequestExecutionLevel admin


; Interface moderna
!define MUI_ABORTWARNING
!define MUI_ICON "..\..\resources\WaterAnalises.ico"
!define MUI_UNICON "..\..\resources\WaterAnalises.ico"

; Personalizar textos para não exibir placeholders como "NOME"
!define MUI_WELCOMEPAGE_TITLE "Welcome to the WaterAnalyser Setup"
!define MUI_WELCOMEPAGE_TEXT "This installer will install WaterAnalyser on your computer."

; Páginas do instalador
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\..\LICENSE.txt" ; Crie este arquivo de licença
!insertmacro MUI_PAGE_DIRECTORY

; Custom page: ask user for encryption key (optional)
Var ENCKEY
Page custom AskEncryptionKeyCreate AskEncryptionKeyLeave

Function AskEncryptionKeyCreate
    ; Create a simple input box
    nsDialogs::Create 1018
    Pop $0
    ${If} $0 == error
        Abort
    ${EndIf}

    ; Label
    ${NSD_CreateLabel} 0 0 100% 12u "If you have an encryption key for the training dataset, enter it below. Leave blank to skip."
    Pop $0

    ; Input - criar campo de texto vazio
    ${NSD_CreateText} 0 18u 100% 12u ""
    Pop $ENCKEY

    nsDialogs::Show
FunctionEnd

Function AskEncryptionKeyLeave
    ; Read the text content into $ENCKEY
    ${NSD_GetText} $ENCKEY $ENCKEY
    ; If user entered a key, save it to registry (HKCU). We attempt HKLM first during install.
    StrLen $0 $ENCKEY
    ${If} $0 > 0
        ; Try to write to HKLM (requires admin), otherwise write to HKCU
        SetRegView 64
        WriteRegStr HKLM "Software\${APPNAME}" "CSV_ENC_KEY" "$ENCKEY"
        ${If} ${Errors}
            ; fallback to HKCU
            WriteRegStr HKCU "Software\${APPNAME}" "CSV_ENC_KEY" "$ENCKEY"
        ${EndIf}
    ${EndIf}
FunctionEnd

!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Páginas de desinstalação
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Idiomas
!insertmacro MUI_LANGUAGE "PortugueseBR"

; Seção principal de instalação
Section "Principal" SecMain
    SetOutPath "$INSTDIR"
    
    ; Copiar todos os arquivos da pasta dist/WaterAnalyser para a pasta de instalação
    File /r "..\..\dist\WaterAnalyser\*.*"
    
    ; Criar atalho no menu iniciar
    CreateDirectory "$SMPROGRAMS\${APPNAME}"
    CreateShortcut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\WaterAnalyser.exe" "" "$INSTDIR\WaterAnalyser.exe" 0
    CreateShortcut "$SMPROGRAMS\${APPNAME}\Desinstalar.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\Uninstall.exe" 0
    
    ; Criar atalho na área de trabalho
    CreateShortcut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\WaterAnalyser.exe" "" "$INSTDIR\WaterAnalyser.exe" 0
    
    ; Escrever informações de desinstalação no registro
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" "$\"$INSTDIR\Uninstall.exe$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "QuietUninstallString" "$\"$INSTDIR\Uninstall.exe$\" /S"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "InstallLocation" "$\"$INSTDIR$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayIcon" "$\"$INSTDIR\WaterAnalyser.exe$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "Publisher" "${COMPANYNAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayVersion" "${APPVERSION}"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoRepair" 1
    
    ; Calcular e salvar o tamanho da instalação
    ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
    IntFmt $0 "0x%08X" $0
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "EstimatedSize" "$0"
    
    ; Criar desinstalador
    WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

; Seção de desinstalação
Section "Uninstall"
    ; Remover ícones do menu iniciar
    Delete "$SMPROGRAMS\${APPNAME}\*.*"
    RMDir "$SMPROGRAMS\${APPNAME}"
    
    ; Remover atalho da área de trabalho
    Delete "$DESKTOP\${APPNAME}.lnk"
    
    ; Remover arquivos e pastas da instalação
    RMDir /r "$INSTDIR"
    
    ; Remover dados do registro
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
SectionEnd