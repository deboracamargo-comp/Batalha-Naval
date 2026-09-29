import json
import time
from replay import exibir_replay
from jogador import Jogador
from computador import jogada_computador


def jogar_partida(contra_computador=False):
    """
    Executa uma partida completa entre dois jogadores até
    haver um vencedor.
    """
    j1 = Jogador()
    j2 = Jogador()
    nome_j1 = "Jogador 1"
    if contra_computador:
        nome_j2 = "Computador"
    else:
        nome_j2 = "Jogador 2"
    atacante = j1
    defensor = j2
    historico = []
    inicio = time.time()

    while not j1.perdeu() and not j2.perdeu():
        turno_do_computador = contra_computador and atacante is j2
        defensor.tabuleiro.exibir_adversario()
        if turno_do_computador:
            coordenada = jogada_computador(atacante, defensor)
            print(f"O computador jogou: {coordenada}")
        else:
            coordenada = input("Digite a posição do ataque: ")
        resultado = atacante.jogar(coordenada, defensor)
        if not turno_do_computador:
            if resultado == "agua":
                print("Água! Nenhum navio atingido nessa posição!")
            elif resultado == "afundou":
                print("Navio afundado! Você destruiu um navio inimigo.")
            elif resultado == "acerto":
                print("Acerto! Você atingiu um navio inimigo!")
            else:
                print("Jogada inválida — tente novamente.")
        else:
            if resultado == "agua":
                print("Nenhum dos seus navios foi atingido nessa posição!")
            elif resultado == "afundou":
                print("O computador afundou um dos seus navios!")
            else:
                print("O computador atingiu um dos seus navios!")
        if resultado != "invalida":
            if atacante is j1:
                nome_do_atacante = nome_j1
            else:
                nome_do_atacante = nome_j2
            registro = {
                "jogador": nome_do_atacante,
                "coordenada": coordenada,
                "resultado": resultado,
            }
            historico.append(registro)
            atacante, defensor = defensor, atacante

    fim = time.time()
    duracao = fim - inicio
    if j1.perdeu():
        vencedor = nome_j2
    else:
        vencedor = nome_j1
    total_jogadas = len(historico)
    return vencedor, total_jogadas, duracao, historico


def exibir_resultado(vencedor, total_jogadas, duracao):
    """Exibe o resumo de fim de jogo: vencedor, total de jogadas e tempo."""
    segundos_totais = int(duracao)
    horas = segundos_totais // 3600
    minutos = segundos_totais // 60 - horas * 60
    segundos = segundos_totais % 60
    print("========================================")
    print("FIM DO JOGO")
    print("========================================")
    print(f"Vencedor: {vencedor}")
    print(f"Total de jogadas: {total_jogadas}")
    print(f"Tempo de partida: {horas:02}:{minutos:02}:{segundos:02}")


def exibir_opcoes_fim_jogo(contra_computador):
    """Exibe as opções de pós-jogo: replay, nova partida ou menu principal."""
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


def iniciar_partida(contra_computador=False):
    """
    Joga uma partida, salva o histórico e as estatísticas,
    e exibe o resultado final.
    """
    vencedor, total_jogadas, duracao, historico = jogar_partida(
        contra_computador
    )
    with open("data/replay.json", "w") as arquivo:
        json.dump(historico, arquivo)

    acertos = 0
    for jogada in historico:
        if jogada["resultado"] == "acerto" or jogada["resultado"] == "afundou":
            acertos += 1

    try:
        with open("data/estatisticas.json", "r") as arquivo:
            estatisticas = json.load(arquivo)
    except FileNotFoundError:
        estatisticas = []

    estatisticas.append({
        "vencedor": vencedor,
        "total_jogadas": total_jogadas,
        "acertos": acertos,
    })
    with open("data/estatisticas.json", "w") as arquivo:
        json.dump(estatisticas, arquivo)

    exibir_resultado(vencedor, total_jogadas, duracao)
    exibir_opcoes_fim_jogo(contra_computador)
