import json


def calcular_estatisticas():
    """
    Calcula as estatísticas acumuladas de todas as partidas.
    Retorna None se nenhuma partida foi jogada ainda.
    """
    try:
        with open("data/estatisticas.json", "r") as arquivo:
            estatisticas = json.load(arquivo)
    except FileNotFoundError:
        return None

    total_jogadas = 0
    total_acertos = 0
    for partida in estatisticas:
        total_jogadas += partida["total_jogadas"]
        total_acertos += partida["acertos"]

    if total_jogadas > 0:
        aproveitamento = (total_acertos / total_jogadas) * 100
    else:
        aproveitamento = 0

    return {
        "partidas": len(estatisticas),
        "jogadas": total_jogadas,
        "acertos": total_acertos,
        "aproveitamento": aproveitamento,
    }


def ver_estatisticas():
    """Exibe as estatísticas acumuladas de todas as partidas jogadas."""
    dados = calcular_estatisticas()
    if dados is None:
        print("Nenhuma partida foi jogada ainda.")
        input("Pressione Enter para voltar ao menu...")
        return

    print("========================================")
    print("ESTATÍSTICAS")
    print("========================================")
    print(f"Partidas jogadas: {dados['partidas']}")
    print(f"Total de jogadas: {dados['jogadas']}")
    print(f"Acertos: {dados['acertos']}")
    print(f"Aproveitamento: {dados['aproveitamento']:.1f}%")
    input("Pressione Enter para voltar ao menu...")
