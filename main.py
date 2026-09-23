from tabuleiro import Tabuleiro
from navios import criar_frota


if __name__ == "__main__":
    frota = criar_frota()
    t = Tabuleiro()
    t.posicionar_navios(frota)
    print("--- Tabuleiro próprio ---")
    t.exibir_proprio()
    print("--- Tabuleiro do adversário ---")
    t.exibir_adversario()
