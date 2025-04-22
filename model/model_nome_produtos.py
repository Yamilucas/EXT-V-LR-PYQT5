class Produto:  
    def __init__(self):
        self._nome_produto: str = ""
        self._imagem_produto: str = ""
        self._categoria_id: str = "" 

    def set_nome_produto(self, nome_produto: str):
        self._nome_produto = nome_produto

    def get_nome_produto(self) -> str:
        return self._nome_produto

    def set_imagem_produto(self, imagem_produto: str):
        self._imagem_produto = imagem_produto

    def get_imagem_produto(self) -> str:
        return self._imagem_produto

    def set_categoria_id(self, categoria_id: str):
        self._categoria_id = categoria_id  

    def get_categoria_id(self) -> str:
        return self._categoria_id