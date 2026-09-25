from tabuleiro import Tabuleiro
from navios import criar_frota
from utils import converter_coordenada


class Jogador:
    def __init__(self):
        self.tabuleiro = Tabuleiro()
        self.frota = criar_frota()
        self.tabuleiro.posicionar_navios(self.frota)

    def jogar(self, coordenada, oponente):
        linha, coluna = converter_coordenada(coordenada)
        navio_atingido = None
        for navio in oponente.frota:
            if navio.registrar_tiro((linha, coluna)):
                oponente.tabuleiro.grade[linha][coluna] = "X"
                navio_atingido = navio
                break
        if navio_atingido is None:
            oponente.tabuleiro.grade[linha][coluna] = "O"
            return "agua"
        else:
            if navio_atingido.afundado():
                return "afundou"
            else:
                return "acerto"


if __name__ == "__main__":
    j1 = Jogador()
    j2 = Jogador()

    print(j2.frota[0].coordenadas)
    resultado = j1.jogar("D2", j2)
    print("Resultado do tiro:", resultado)
    j2.tabuleiro.exibir_proprio()