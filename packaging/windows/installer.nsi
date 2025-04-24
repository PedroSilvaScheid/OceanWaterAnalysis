; Script de instalação para o WaterAnalyser
; Gerado para o projeto de análise de água

!include "MUI2.nsh"
!include "FileFunc.nsh"

; Definições do app
!define APPNAME "WaterAnalyser"
!define APPVERSION "1.0.0"
!define COMPANYNAME "YourCompany"
!define DESCRIPTION "Ferramenta para análise de qualidade da água"

; Pasta de instalação padrão
InstallDir "$PROGRAMFILES\${APPNAME}"

; Nome do arquivo de saída do instalador
OutFile "..\..\..\dist\${APPNAME}_Setup_${APPVERSION}.exe"

; Solicitar privilégios de administrador
RequestExecutionLevel admin

; Interface moderna
!define MUI_ABORTWARNING
!define MUI_ICON "..\..\..\resources\WaterAnalises.ico"
!define MUI_UNICON "..\..\..\resources\WaterAnalises.ico"

; Páginas do instalador
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\..\LICENSE.txt" ; Crie este arquivo de licença
!insertmacro MUI_PAGE_DIRECTORY
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
    File /r "..\..\..\dist\WaterAnalyser\*.*"
    
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