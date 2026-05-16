import re


_EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@gmail\.com$')


class Validadores:
    def validar_email(self, email: str) -> str | bool:
        if _EMAIL_REGEX.fullmatch(email):
            return email
        return False

    def validar_senha(self) -> None:
        ...

    def validar_nome(self) -> None:
        ...
