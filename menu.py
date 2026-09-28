from main import jogar_partida
from replay import exibir_replay
from estatisticas import exibir_estatisticas


def nova_partida():
    """Exibe o menu de modos de jogo e inicia a partida escolhida."""
    while True:
        print("Selecione o modo de jogo: ")
        print(" [1]Jogador vs Computador")
        print(" [2]Dois Jogadores")
        print(" [0]Voltar ao menu")
        modo_de_jogo = int(input("\n>>_"))
        if modo_de_jogo == 1:
            jogar_partida(contra_computador=True)
            break
        elif modo_de_jogo == 2:
            jogar_partida()
            break
        elif modo_de_jogo == 0:
            break
        else:
            print("Opção inválida! Tente novamente!")


def ver_estatisticas():
    """Exibe as estatísticas de desempenho a partir do histórico salvo."""
    exibir_estatisticas()


def ver_replay():
    """Reproduz, jogada a jogada, o histórico da última partida salva."""
    exibir_replay()


def creditos():
    """Exibe os créditos do jogo."""
    print("========================================")
    print("\tCRÉDITOS")
    print("========================================")
    print("Nome do desenvolvedor: Débora Cristina Barbosa Camargo")
    print("Professor: Guido Pantuza")
    print("Disciplina: Programação em Python")
    print("Nome do Projeto: GPTech Games")
    print("----------------------------------------")
    input("Pressione Enter para voltar para o menu...")


def exibir_menu():
    """Exibe o menu principal e direciona para a opção escolhida."""
    opcao = None
    while opcao != 5:
        print("========================================")
        print("\tBATALHA NAVAL - GPTECH GAMES")
        print("========================================")
        print("1. Nova partida")
        print("2. Ver estatísticas")
        print("3. Assistir replay da última partida")
        print("4. Créditos")
        print("5. Sair")
        print("----------------------------------------")
        opcao = int(input("Escolha uma opção:_ "))

        if opcao == 1:
            nova_partida()
        elif opcao == 2:
            ver_estatisticas()
        elif opcao == 3:
            ver_replay()
        elif opcao == 4:
            creditos()
        elif opcao == 5:
            print("Saindo do jogo...")
        else:
            print("Opção inválida! Tente novamente!")


if __name__ == "__main__":
    exibir_menu()
