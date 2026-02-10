# SPED Auto - Sistema de Automação

## 📋 Descrição

Sistema de automação para o SPED da Softcom Tecnologia que facilita processos repetitivos através de automação de cliques para corrigir CESTs.

## 🚀 Rodar código fonte localmente

### Pré-requisitos

- Python 3.x instalado ([Download aqui](https://www.python.org/downloads/))
  - ⚠️ Durante a instalação, marque a opção "Add Python to PATH"

### Instalação Rápida

1. Copie toda a pasta do projeto para o novo computador
2. Execute o arquivo `instalar.bat` (duplo clique)
3. Aguarde a instalação das dependências
4. Pronto! O sistema está instalado

## ▶️ Como Usar

### Executar o Programa

Duplo clique no arquivo `executar.bat`

**OU** manualmente:

```batch
venv\Scripts\activate.bat
python auto.py
```

### Atalhos de Teclado

Após iniciar o programa:

- **F3** - Auto-login (preenche senha automaticamente)
- **F4** - Corrigir CEST (inicia/para o loop automático)
- **F2** - Listar janelas abertas (debug)
- **F1** - Mostrar IDs dos controles (debug)

## 📦 Dependências

As dependências estão listadas no arquivo `requirements.txt`:

- pywinauto - Automação de interface Windows
- keyboard - Captura de teclas de atalho

## 🔧 Reinstalação

Se precisar reinstalar as dependências:

```batch
venv\Scripts\activate.bat
pip install -r requirements.txt
```

## 📂 Estrutura do Projeto

```
SPED/
├── auto.py              # Script principal
├── SPED.exe.config     # Configuração do SPED
├── requirements.txt     # Dependências Python
├── instalar.bat        # Script de instalação
├── executar.bat        # Script de execução
├── venv/               # Ambiente virtual (gerado)
├── json/               # Arquivos JSON
│   └── nfe_cest.json
└── Log/                # Arquivos de log
    ├── log.txt
    └── updatelog.txt
```

## ⚠️ Solução de Problemas

### Python não encontrado

- Reinstale o Python marcando "Add Python to PATH"
- Ou adicione manualmente o Python ao PATH do sistema

### Erro ao instalar dependências

- Certifique-se de ter conexão com a internet
- Execute o PowerShell como Administrador e rode:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
