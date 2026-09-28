import json


def exibir_estatisticas():
    with open("data/replay.json", "r") as arquivo:
        historico = json.load(arquivo)

    total_jogadas = len(historico)
    acertos = 0
    for jogada in historico:
        if jogada["resultado"] == "acerto" or jogada["resultado"] == "afundou":
            acertos += 1

    aproveitamento = (acertos / total_jogadas) * 100

    print("========================================")
    print("ESTATÍSTICAS")
    print("========================================")
    print(f"Total de jogadas: {total_jogadas}")
    print(f"Acertos: {acertos}")
    print(f"Aproveitamento: {aproveitamento:.1f}%")
