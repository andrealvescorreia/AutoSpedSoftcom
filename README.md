# SPED Auto - Sistema de Automação

## 📋 Descrição

Sistema de automação para o SPED da Softcom Tecnologia que facilita processos repetitivos através de automação de cliques para corrigir CESTs.

## Rodar localmente

### Crie venv

`python -m venv venv`

### Ativar venv

`venv\Scripts\activate`

### Instalar dependencias

`pip install -r requirements.txt`

### Alterar dependencias

`pip freeze > requirements.txt`

## Gerar arquivo executavel

`pyinstaller --onefile --windowed --name "SPED-Auto" auto.py`
