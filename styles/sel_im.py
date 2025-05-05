def obter_estilo_borda():
    return """
        QLabel#area_imagem {
            border: 2px dashed #808080;
            background-color: #FFFFFF;
            border-radius: 15px;
            min-width: 240px;
            max-width: 240px;
            min-height: 240px;
            max-height: 240px;
            qproperty-alignment: 'AlignCenter';
        }
        
        QLabel#area_imagem {
            qproperty-scaledContents: false;
            padding: 0;
        }
    """

def obter_estilo_botao_circular():
    return """
        QPushButton#botao_mais {
            background-color: #000000;
            color: #FFFFFF;
            border: none;
            border-radius: 25px;
            min-width: 50px;
            max-width: 50px;
            min-height: 50px;
            max-height: 50px;
            font-size: 24px;
            font-weight: bold;
        }
        QPushButton#botao_mais:hover {
            background-color: #333333;
        }
        QPushButton#botao_mais:pressed {
            background-color: #666666;
        }
    """

def obter_estilo_logo_empresa():
    return """
        QLabel#logo_empresa {
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 8px;
            background-color: white;
            padding: 2px;
        }
        QLabel#logo_empresa:hover {
            border-color: #FFA500;
            background-color: rgba(255, 165, 0, 0.1);
        }
        QLabel#logo_empresa_selecionada {
            border: 3px solid #FFA500;
            background-color: rgba(255, 165, 0, 0.1);
        }
    """

def obter_estilo_preco():
    return """
        QLabel#preco_label {
            color: #FFA500;
            font: bold 16px;
            background-color: rgba(0, 0, 0, 0.7);
            border-radius: 5px;
            padding: 5px 10px;
        }
    """