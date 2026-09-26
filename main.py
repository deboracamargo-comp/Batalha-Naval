from jogador import Jogador


j1 = Jogador()
j2 = Jogador()
atacante = j1
defensor = j2
historico = []

while not j1.perdeu() and not j2.perdeu():
    defensor.tabuleiro.exibir_adversario()
    coordenada = input("Digite a posição do ataque: ")
    resultado = atacante.jogar(coordenada, defensor)
    if resultado == "agua":
        print("Água! Nenhum navio atingido nessa posição!")
    elif resultado == "afundou":
        print("Navio afundado! Você destruiu um navio inimigo.")
    elif resultado == "acerto":
        print("Acerto! Você atingiu um navio inimigo!")
    else:
        print("Jogada inválida — tente novamente.")
    if resultado != "invalida":
        if atacante is j1:
            nome_do_atacante = "Jogador 1"
        else:
            nome_do_atacante = "Jogador 2"
        registro = {"jogador": nome_do_atacante, "coordenada": coordenada, "resultado": resultado}
        historico.append(registro)
        atacante, defensor = defensor, atacante
print("\tFim do jogo!")
