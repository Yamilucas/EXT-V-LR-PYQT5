class Empresa:
    def __init__(self):
        self._nome_empresa: str = ""
        self._logo_empresa: str = ""  

    def set_nome_empresa(self, nome_empresa: str):
        self._nome_empresa = nome_empresa

    def get_nome_empresa(self) -> str:
        return self._nome_empresa

    def set_logo(self, logo_base64: str):
        self._logo_empresa = logo_base64

    def get_logo(self) -> str:
        return self._logo_empresa