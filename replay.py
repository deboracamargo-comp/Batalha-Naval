import json


def exibir_replay():
    """Reproduz, jogada a jogada, o histórico da última partida salva."""
    try:
        with open("data/replay.json", "r") as arquivo:
            historico = json.load(arquivo)
    except FileNotFoundError:
        print("Nenhuma partida foi jogada ainda.")
        input("Pressione Enter para voltar ao menu...")
        return

    print("Reproduzindo replay da última partida...")
    for indice, jogada in enumerate(historico):
        print(
            f"Jogada {indice + 1}/{len(historico)} - "
            f"{jogada['jogador']} - {jogada['coordenada']} - "
            f"{jogada['resultado'].capitalize()}"
        )
        comando = input("[ENTER] Próxima jogada  [Q] Sair do replay: ")
        if comando.upper() == "Q":
            break

    print("Fim do replay.")
    input("Pressione Enter para voltar ao menu...")
