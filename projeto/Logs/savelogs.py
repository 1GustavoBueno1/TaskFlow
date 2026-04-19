"""
Aqui e onde as logs são registradas em arquivos para localizar, encontrar erros
ou indicar qual metodo obteve sucesso a ser execudado.
"""
from pathlib import Path

LOG_FILE = Path(__file__).parent / "Log.txt"
class log:
    """
    Aqui e onde os registros sao criados para emitir uma mensagem

    """
    def _log(self, msg: str) -> None:
        raise NotImplementedError("ERRO")
    def success(self, msg: str) -> str:
        return self._log(f"Sucess: {msg}")
    def error(self, msg: str) -> str:
        return self._log(f"Erro: {msg}")
class SaveLog(log):
    """
    Aqui os registros sao salvos e guardados em um arquivo txt
    """
    def _log(self, msg: str) -> None:
        with open(LOG_FILE, 'a', encoding='utf-8') as arquivo:
            arquivo.write(msg)
            arquivo.write("\n")