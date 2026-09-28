import json


def exibir_replay():
    with open("data/replay.json", "r") as arquivo:
        historico = json.load(arquivo)
        print("Reproduzindo replay da última partida...")
        for indice, jogada in enumerate(historico):
            print(
                f"Jogada {indice + 1}/{len(historico)} - "
                f"{jogada['jogador'].capitalize()} - "
                f"{jogada['coordenada'].capitalize()} - "
                f"{jogada['resultado'].capitalize()}"
                )
