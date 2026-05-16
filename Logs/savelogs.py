"""
Aqui é onde os logs são registrados em arquivos para localizar erros
ou indicar qual método foi executado com sucesso.
"""
from pathlib import Path

ARQUIVO_LOG = Path(__file__).parent / "Log.txt"


class Log:
    """
    Classe base para emitir mensagens de log.
    """
    def _registrar(self, mensagem: str) -> None:
        raise NotImplementedError("Erro: método não implementado")

    def sucesso(self, mensagem: str) -> None:
        self._registrar(f"Sucesso: {mensagem}")

    def erro(self, mensagem: str) -> None:
        self._registrar(f"Erro: {mensagem}")


class SalvarLog(Log):
    """
    Salva os registros em um arquivo .txt.
    """
    def _registrar(self, mensagem: str) -> None:
        with open(ARQUIVO_LOG, 'a', encoding='utf-8') as arquivo:
            arquivo.write(mensagem)
            arquivo.write("\n")
