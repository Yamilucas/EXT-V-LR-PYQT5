class ProdutoVinculado():
    def __init__(self):
        super().__init__()  
        self._empresa_id: str = ""
        self._categoria_id: str = ""
        self._produto_id: str = ""
        self._preco_produto: float = 0.0
        self._promocao_produto: bool = False

    def set_empresa_id(self, empresa_id: str):
        self._empresa_id = empresa_id

    def get_empresa_id(self) -> str:
        return self._empresa_id

    def set_categoria_id(self, categoria_id: str):
        self._categoria_id = categoria_id

    def get_categoria_id(self) -> str:
        return self._categoria_id

    def set_produto_id(self, produto_id: str):
        self._produto_id = produto_id

    def get_produto_id(self) -> str:
        return self._produto_id

    def set_preco(self, preco_produto: float):
        self._preco_produto = preco_produto

    def get_preco(self) -> float:
        return self._preco_produto

    def set_promocao(self, promocao_produto: bool):
        self._promocao_produto = promocao_produto

    def get_promocao(self) -> bool:
        return self._promocao_produto