@echo off
echo ================================================
echo Instalador do SPED Auto - Softcom Tecnologia
echo ================================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale o Python 3.x primeiro.
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] Criando ambiente virtual...
python -m venv venv
if errorlevel 1 (
    echo ERRO: Falha ao criar ambiente virtual
    pause
    exit /b 1
)

echo [2/3] Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo [3/3] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERRO: Falha ao instalar dependencias
    pause
    exit /b 1
)

echo.
echo ================================================
echo Instalacao concluida com sucesso!
echo ================================================
echo.
echo Para executar o programa:
echo   1. Execute: executar.bat
echo   OU
echo   1. Ative o venv: venv\Scripts\activate.bat
echo   2. Execute: python auto.py
echo.
pause
