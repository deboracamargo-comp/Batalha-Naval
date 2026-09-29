from tabuleiro import Tabuleiro
from navios import criar_frota, dentro_do_tabuleiro
from utils import converter_coordenada


class Jogador:
    def __init__(self):
        self.tabuleiro = Tabuleiro()
        self.frota = criar_frota()
        self.tabuleiro.posicionar_navios(self.frota)

    def jogada_valida(self, coordenada, oponente):
        """
        Verifica se a coordenada está dentro
        do tabuleiro e não foi jogada antes.
        """
        try:
            linha, coluna = converter_coordenada(coordenada)
        except (ValueError, IndexError):
            return False
        if not dentro_do_tabuleiro([(linha, coluna)]):
            return False
        valor = oponente.tabuleiro.grade[linha][coluna]
        if valor in ["X", "O"]:
            return False
        return True

    def jogar(self, coordenada, oponente):
        """Realiza um disparo contra o oponente e atualiza o tabuleiro."""
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
        """Verifica se o jogador perdeu o jogo."""
        resultados = []
        for navio in self.frota:
            resultados.append(navio.afundado())
        return all(resultados)
