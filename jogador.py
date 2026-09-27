from tabuleiro import Tabuleiro
from navios import criar_frota, dentro_do_tabuleiro
from utils import converter_coordenada


class Jogador:
    def __init__(self):
        self.tabuleiro = Tabuleiro()
        self.frota = criar_frota()
        self.tabuleiro.posicionar_navios(self.frota)

    def jogada_valida(self, coordenada, oponente):
        linha, coluna = converter_coordenada(coordenada)
        if not dentro_do_tabuleiro([(linha, coluna)]):
            return False
        else:
            valor = oponente.tabuleiro.grade[linha][coluna]
            if valor == "X" or valor == "O":
                return False
            else:
                return True

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

    def perdeu(self):
        resultados = []
        for navio in self.frota:
            resultados.append(navio.afundado())
        return all(resultados)


if __name__ == "__main__":
    j1 = Jogador()
    j2 = Jogador()

    print(j1.perdeu())  # False, ninguém foi atingido ainda

    # afunda o primeiro navio da frota do j1, na força bruta
    for posicao in j1.frota[0].coordenadas:
        j1.frota[0].registrar_tiro(posicao)

    print(j1.perdeu())
    # ainda False, só 1 de 8 navios afundou
