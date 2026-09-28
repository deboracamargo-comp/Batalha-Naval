def converter_coordenada(coordenada):
    coordenada = coordenada.upper()
    letra = coordenada[0]
    coluna = ord(letra) - 65
    linha = int(coordenada[1:]) - 1
    return linha, coluna


if __name__ == "__main__":
    print(converter_coordenada("A1"))
    print(converter_coordenada("C5"))
    print(converter_coordenada("J10"))
