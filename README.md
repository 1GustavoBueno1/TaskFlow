# TaskFlow

Aplicação web de gerenciamento de **usuários** e **tarefas**, construída em **Flask** com persistência em **MySQL**. Conta com autenticação por sessão, senhas protegidas com **bcrypt**, proteção **CSRF**, **rate limiting** e validação de email.

---

## Funcionalidades

- Cadastro de usuários com senha criptografada (bcrypt)
- Login com verificação de hash e sessão
- Edição de perfil (nome, gmail, senha) com confirmação de senha
- Visualização do próprio perfil
- Criação de tarefas
- Listagem das tarefas do usuário logado
- Edição de tarefas (nome, descrição, status)
- Deleção de tarefas (com confirmação de senha)
- Logout

---

## Tecnologias

- **Python 3.10+**
- **Flask 3** — framework web
- **MySQL 8.0** (driver **PyMySQL**)
- **Flask-WTF** — proteção CSRF
- **Flask-Limiter** — limite de requisições (rate limiting)
- **bcrypt** — hash de senhas
- **python-dotenv** — variáveis de ambiente
- **waitress** — servidor WSGI para produção
- **pytest** — testes
- **Docker / docker-compose** — banco MySQL em container

> O `requirements.txt` traz todas as dependências com versões fixadas.

---

## Estrutura do Projeto

```
TaskFlow/
│
├── main.py                     # Entrada de desenvolvimento (app.run)
├── wsgi.py                     # Entrada de produção (waitress)
├── Procfile                    # web: python wsgi.py
├── requirements.txt
├── pytest.ini
│
├── app/
│   ├── __init__.py             # create_app() — application factory
│   ├── config.py               # Config + conexão com o banco (get_connection)
│   ├── extensions.py           # Instâncias de CSRF e Limiter
│   │
│   ├── models/                 # Acesso ao banco (queries SQL)
│   │   ├── user.py             # UserRepository
│   │   └── task.py             # TaskRepository
│   │
│   ├── routes/                 # Blueprints (camada web)
│   │   ├── auth_route.py       # /auth   — cadastro e login
│   │   ├── task_route.py       # /tarefa — CRUD de tarefas
│   │   └── user_route.py       # /perfil — perfil e logout
│   │
│   ├── services/               # Regras de negócio
│   │   ├── auth_service.py     # Autenticacao
│   │   ├── task_service.py     # Tarefas
│   │   └── user_service.py     # Usuario
│   │
│   ├── static/                 # CSS e JS
│   └── templates/              # Páginas Jinja2
│
├── Logs/
│   └── savelogs.py             # Registro de eventos (logs)
│
└── Docker-compose/
    ├── docker-compose.yml      # MySQL 8.0
    └── .env-exemple            # Modelo de variáveis do banco
```

---

## Arquitetura

O projeto segue separação em camadas, no fluxo `Rotas → Serviços → Modelos`:

- **Rotas (`routes/`)** — blueprints do Flask; recebem a requisição, leem o formulário/sessão e devolvem a resposta (render/redirect). Sem regra de negócio.
- **Serviços (`services/`)** — validações e regras (autenticação, verificação de senha, validação de email, montagem das operações).
- **Modelos (`models/`)** — repositórios que executam as queries SQL e retornam os dados.

A criação da aplicação usa o padrão **application factory** (`create_app()`), e as tabelas `Users` e `Tasks` são criadas automaticamente na inicialização.

### Rotas principais

| Método      | Rota                                  | Descrição                       |
|-------------|---------------------------------------|---------------------------------|
| GET         | `/`                                   | Página inicial                  |
| GET/POST    | `/auth/cadastro`                      | Cadastro de usuário             |
| GET/POST    | `/auth/login`                         | Login                           |
| GET         | `/tarefa/listar`                      | Lista tarefas do usuário        |
| GET/POST    | `/tarefa/criar`                       | Cria tarefa                     |
| GET/POST    | `/tarefa/editar/<id>/<coluna>`        | Edita campo da tarefa           |
| GET/POST    | `/tarefa/editar/deletar/<id>`         | Deleta tarefa                   |
| GET         | `/perfil/visualizar`                  | Visualiza perfil                |
| GET/POST    | `/perfil/editar/<coluna>`             | Edita campo do perfil           |
| GET/POST    | `/perfil/sair`                        | Logout                          |

---

## Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/TaskFlow.git
cd TaskFlow
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Suba o banco MySQL (Docker)

Dentro de `Docker-compose/`, crie um `.env` a partir do `.env-exemple`:

```env
MYSQL_ROOT_PASSWORD=sua_senha_root
MYSQL_DATABASE=Base_para_dados
MYSQL_USER=seu_usuario
MYSQL_PASSWORD=sua_senha
```

E suba o container (MySQL exposto na porta `3307`):

```bash
cd Docker-compose
docker-compose up -d
```

### 5. Configure o `.env` da aplicação

Crie um `.env` na raiz do projeto:

```env
SECRET_KEY=uma_chave_secreta_bem_aleatoria
DB_HOST=localhost
DB_PORT=3307
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=Base_para_dados

# Opcionais
FLASK_DEBUG=False
SESSION_COOKIE_SECURE=False   # use True em produção (HTTPS)
HOST=0.0.0.0
PORT=8000
```

> **`SECRET_KEY` é obrigatória** — a aplicação não inicia sem ela.

### 6. Execute o projeto

**Desenvolvimento:**

```bash
python main.py
```

**Produção (waitress):**

```bash
python wsgi.py
```

---

## Testes

```bash
pytest
```

---

## Segurança

- **Senhas com hash bcrypt** — a senha real nunca é armazenada no banco.
- **SQL parametrizado** (`%s`) — proteção contra SQL injection.
- **Allowlist de colunas** — updates dinâmicos só aceitam colunas previstas (`frozenset`), evitando injeção pelo nome da coluna.
- **Proteção CSRF** em todos os formulários (Flask-WTF).
- **Rate limiting** (Flask-Limiter) — 200/hora por padrão, login 5/min e cadastro 10/min.
- **Cookies de sessão endurecidos** — `HttpOnly`, `SameSite=Lax` e `Secure` configurável.
- **Validação de email** por regex (apenas `@gmail.com`).
- **Credenciais isoladas** em variáveis de ambiente via `.env`.
