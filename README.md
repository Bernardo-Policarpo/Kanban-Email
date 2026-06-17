# Kanban Email

Sistema web interno desenvolvido em Flask para envio de e-mails para acionamento de cartões Kanban.

## Tecnologias

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript

## Estrutura

```text
.
├── app.py
├── templates/
├── static/
├── .env
└── requirements.txt
```

## Instalação

Clone o repositório:

```bash
git clone https://github.com/Bernardo-Policarpo/Kanban-Email.git
cd kanban-email
```

Crie um ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente:

### Windows

```bash
venv\Scripts\activate
```

### Linux

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure as variáveis de ambiente no arquivo `.env`.

Execute a aplicação:

```bash
python app.py
```

## Objetivo

Automatizar processos internos e reduzir tarefas manuais relacionadas ao envio de e-mails.
