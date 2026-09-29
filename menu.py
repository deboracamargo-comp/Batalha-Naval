from partida import iniciar_partida
from replay import exibir_replay
from estatisticas import ver_estatisticas


def nova_partida():
    """Exibe o menu de modos de jogo e inicia a partida escolhida."""
    while True:
        print("Selecione o modo de jogo: ")
        print(" [1]Jogador vs Computador")
        print(" [2]Dois Jogadores")
        print(" [0]Voltar ao menu")
        try:
            modo_de_jogo = int(input("\n>>_"))
        except ValueError:
            print("Opção inválida! Tente novamente!")
            continue
        if modo_de_jogo == 1:
            iniciar_partida(contra_computador=True)
            break
        elif modo_de_jogo == 2:
            iniciar_partida()
            break
        elif modo_de_jogo == 0:
            break
        else:
            print("Opção inválida! Tente novamente!")


def creditos():
    """Exibe os créditos do jogo."""
    print("========================================")
    print("\tCRÉDITOS")
    print("========================================")
    print("Nome do desenvolvedor: Débora Camargo")
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
        try:
            opcao = int(input("Escolha uma opção:_ "))
        except ValueError:
            print("Opção inválida! Tente novamente!")
            continue

        if opcao == 1:
            nova_partida()
        elif opcao == 2:
            ver_estatisticas()
        elif opcao == 3:
            exibir_replay()
        elif opcao == 4:
            creditos()
        elif opcao == 5:
            print("Saindo do jogo...")
        else:
            print("Opção inválida! Tente novamente!")


def exibir_opcoes_fim_jogo(contra_computador):
    """
    Exibe as opções de pós-jogo: replay,
    nova partida ou menu principal.
    """
    while True:
        print("[1] Ver replay  [2] Nova partida  [3] Menu principal")
        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Opção inválida! Tente novamente!")
            continue
        if opcao == 1:
            exibir_replay()
        elif opcao == 2:
            iniciar_partida(contra_computador)
            break
        elif opcao == 3:
            break
        else:
            print("Opção inválida! Tente novamente!")
