class Categoria:
    def __init__(self):
        self._nome_categoria: str = "" 

    def set_nome_categoria(self, nome_categoria: str):
        self._nome_categoria = nome_categoria

    def get_nome_categoria(self) -> str:
        return self._nome_categoria