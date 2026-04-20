# Sistema de Cadastro e Tarefas

Sistema de gerenciamento de usuários e tarefas via terminal, com persistência em banco de dados MySQL e senhas protegidas com bcrypt.

---

## Funcionalidades

- Cadastro de usuários com senha criptografada
- Login com verificação de hash
- Edição de perfil (nome, gmail, senha)
- Visualização de informações próprias
- Criação de tarefas
- Visualização de tarefas
- Edição de tarefas (nome, descrição, status)

---

## Tecnologias

- Python 3.9+
- MySQL
- pymysql
- bcrypt
- python-dotenv

---

## Estrutura do Projeto

```
projeto/
│
├── main.py                  # Ponto de entrada e menu principal
│
├── Services/
│   └── system.py            # Lógica de negócio (cadastro, login, tarefas)
│
├── Ui/
│   └── interface.py         # Interface com o usuário (inputs e prints)
│
├── DataBase.py              # Acesso ao banco de dados (queries SQL)
│
├── Logs/
│   └── SalvarLogs.py        # Registro de eventos do sistema
│
├── .env                     # Variáveis de ambiente (não versionado)
├── .gitignore
└── requirements.txt
```

---

## Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
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

Ou manualmente:

```bash
pip install pymysql bcrypt python-dotenv
```

### 4. Configure o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto:

```env
DB_HOST=localhost
DB_PORT=3307
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=Base_para_dados
```

### 5. Execute o projeto

```bash
python main.py
```

---

## Arquitetura

O projeto segue separação de responsabilidades em três camadas:

- **Interface** — coleta dados do usuário e exibe resultados, sem lógica de negócio
- **Sistema** — verifica regras (login, validações) e coordena as operações
- **DataBase** — executa as queries SQL e retorna os dados

O fluxo sempre segue: `Interface → Sistema → DataBase`

---

## Segurança

- Senhas armazenadas com hash bcrypt — a senha real nunca é salva no banco
- Queries SQL parametrizadas com `%s` — protegido contra SQL injection
- Credenciais do banco isoladas em variável de ambiente via `.env`

---

## requirements.txt

```
pymysql
bcrypt
python-dotenv
```
