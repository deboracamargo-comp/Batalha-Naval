import random


class Navio:
    def __init__(self, coordenadas):
        self.coordenadas = coordenadas
        self.atingidas = []
        for i in range(len(coordenadas)):
            self.atingidas.append(False)

    def registrar_tiro(self, posicao):
        if posicao in self.coordenadas:
            indice = self.coordenadas.index(posicao)
            self.atingidas[indice] = True
            return True
        return False

    def afundado(self):
        return all(self.atingidas)


def gerar_coordenadas(linha_inicial, coluna_inicial, tamanho, horizontal):
    coordenadasNavio = []
    if horizontal:
        for i in range(tamanho):
            nova_coluna = coluna_inicial + i
            coordenadasNavio.append((linha_inicial, nova_coluna))
    else:
        for i in range(tamanho):
            nova_linha = linha_inicial + i
            coordenadasNavio.append((nova_linha, coluna_inicial))
    return coordenadasNavio

def dentro_do_tabuleiro(coordenadas):
    valido = True
    for linha, coluna in coordenadas:
        if linha < 0 or linha > 9 or coluna < 0 or coluna > 9:
            valido = False
    return valido
        
def sem_sobreposicao(coordenadas_novo_navio, ocupadas):
    valido = True
    for posicao in coordenadas_novo_navio:
        if posicao in ocupadas:
            valido = False
    return valido

def posicionar_navio(tamanho, ocupadas):
    posicionado = False
    coordenadas = []
    while not posicionado:
        linha = random.randint(0, 9)
        coluna = random.randint(0, 9)
        horizontal = random.choice([True, False])
        candidatas = gerar_coordenadas(linha, coluna, tamanho, horizontal)
        if dentro_do_tabuleiro(candidatas) and sem_sobreposicao(candidatas, ocupadas):
            posicionado = True
            coordenadas = candidatas
    return coordenadas

def criar_frota():
    navios = []
    ocupadas = []
    for _ in range(2):
        coords = posicionar_navio(4, ocupadas)
        ocupadas.extend(coords)
        navio = Navio(coords)
        navios.append(navio)
    for _ in range(6):
        coords = posicionar_navio(2, ocupadas)
        ocupadas.extend(coords)
        navio = Navio(coords)
        navios.append(navio)
    return navios


if __name__ == "__main__":
    frota = criar_frota()
    print(len(frota))  # deve dar 8
    for navio in frota:
        print(navio.coordenadas)
