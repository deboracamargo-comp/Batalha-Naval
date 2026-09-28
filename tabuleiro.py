TAMANHO = 10


class Tabuleiro:
    def __init__(self):
        self.grade = []
        for i in range(TAMANHO):
            linha = []
            for j in range(TAMANHO):
                linha.append("~")
            self.grade.append(linha)

    def posicionar_navios(self, navios):
        for navio in navios:
            for linha, coluna in navio.coordenadas:
                self.grade[linha][coluna] = "N"

    def _exibir(self, esconder_navios):
        print(f"{'':2}", end=" ")
        for i in range(TAMANHO):
            letra = chr(65 + i)
            print(letra, end=" ")
        print()
        for i in range(TAMANHO):
            print(f"{i + 1:2}", end=" ")
            for j in range(TAMANHO):
                valor = self.grade[i][j]
                if esconder_navios and valor == "N":
                    valor = "~"
                print(valor, end=" ")
            print()

    def exibir_proprio(self):
        self._exibir(False)

    def exibir_adversario(self):
        self._exibir(True)
