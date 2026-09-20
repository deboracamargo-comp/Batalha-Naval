TAMANHO = 10


class Tabuleiro:
    def __init__(self):
        self.grade = []
        for i in range(TAMANHO):
            linha = []
            for j in range(TAMANHO):
                linha.append("~")
            self.grade.append(linha)

    def exibir(self):
        print(f"{'':2}", end=" ")
        for i in range(TAMANHO):
            letra = chr(65 + i)
            print(letra, end=" ")
        print()
        for i in range(TAMANHO):
            print(f"{i + 1:2}", end=" ")
            for j in range(TAMANHO):
                print(self.grade[i][j], end=" ")
            print()


if __name__ == "__main__":
    t = Tabuleiro()
    t.exibir()
