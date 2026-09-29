def converter_coordenada(coordenada):
    """Converte uma coordenada em formato de texto (ex: 'A1')
    para índices inteiros (linha, coluna)."""
    coordenada = coordenada.upper()
    letra = coordenada[0]
    coluna = ord(letra) - 65
    linha = int(coordenada[1:]) - 1
    return linha, coluna
