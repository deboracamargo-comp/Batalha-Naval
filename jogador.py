from tabuleiro import Tabuleiro
from navios import criar_frota, dentro_do_tabuleiro
from utils import converter_coordenada


class Jogador:
    def __init__(self):
        self.tabuleiro = Tabuleiro()
        self.frota = criar_frota()
        self.tabuleiro.posicionar_navios(self.frota)

    def jogar(self, coordenada, oponente):
        if not self.jogada_valida(coordenada, oponente):
            return "invalida"
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

    def jogada_valida(self, coordenada, oponente):
        linha, coluna = converter_coordenada(coordenada)
        if not dentro_do_tabuleiro([(linha, coluna)]):
            return False
        else:
            if oponente.tabuleiro.grade[linha][coluna] == "~":
                return True
            else:
                return False


if __name__ == "__main__":
    j1 = Jogador()
    j2 = Jogador()

    print(j2.frota[0].coordenadas)
    resultado = j1.jogar("A3", j2)
    print("Resultado do tiro:", resultado)
    j2.tabuleiro.exibir_proprio()
    print(j2.frota[0].coordenadas)
    resultado = j1.jogar("A3", j2)
    print("Resultado do tiro:", resultado)
    j2.tabuleiro.exibir_proprio()