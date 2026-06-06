"""
Configuração compartilhada dos testes.

O módulo `app.config` levanta RuntimeError na importação caso a variável
SECRET_KEY não esteja definida. Como os testes não devem depender de um
arquivo .env real, garantimos um valor aqui ANTES de qualquer import de
`app.*`. O pytest carrega este conftest.py antes dos módulos de teste,
então essa variável já estará disponível na hora da importação.
"""
import os

os.environ.setdefault("SECRET_KEY", "chave-de-teste")
