import random


def sortear_coordenada():
    """Sorteia uma coordenada aleatória no formato letra+número (ex.: C5)."""
    linha = random.randint(0, 9)
    coluna = random.randint(0, 9)
    letra = chr(65 + coluna)
    return f"{letra}{linha + 1}"


def jogada_computador(computador, oponente):
    """Sorteia uma jogada válida para o computador."""
    while True:
        coordenada = sortear_coordenada()
        if computador.jogada_valida(coordenada, oponente):
            break
    return coordenada
