import ctypes
import os
import sys
import time
import pygame
from jogador import Jogador
from computador import jogada_computador
from partida import salvar_partida, formatar_duracao
from estatisticas import calcular_estatisticas
from replay import carregar_replay
from tabuleiro import TAMANHO
from utils import converter_coordenada

LARGURA, ALTURA = 900, 600
CELULA = 32
TAB_ESQ = (70, 150)
TAB_DIR = (500, 150)
TAB_CENTRO = ((LARGURA - CELULA * TAMANHO) // 2, 130)

FUNDO = (20, 30, 50)
TEXTO = (240, 240, 240)
AGUA = (40, 90, 160)
NAVIO = (130, 130, 130)
ACERTO = (200, 50, 50)
ERRO = (230, 230, 230)
BORDA = (15, 20, 35)
BOTAO = (60, 80, 120)
BOTAO_HOVER = (90, 120, 170)

CORES_CELULA = {"~": AGUA, "N": NAVIO, "X": ACERTO, "O": ERRO}

MENSAGENS_JOGADOR = {
    "agua": "Água! Nenhum navio atingido nessa posição!",
    "acerto": "Acerto! Você atingiu um navio inimigo!",
    "afundou": "Navio afundado! Você destruiu um navio inimigo.",
}
MENSAGENS_COMPUTADOR = {
    "agua": "nenhum dos seus navios foi atingido.",
    "acerto": "ele atingiu um dos seus navios!",
    "afundou": "ele afundou um dos seus navios!",
}

_fontes = {}


def fonte(tamanho):
    """Retorna a fonte padrão no tamanho pedido, criando-a só uma vez."""
    if tamanho not in _fontes:
        _fontes[tamanho] = pygame.font.Font(None, tamanho)
    return _fontes[tamanho]


def desenhar_texto(tela, texto, x, y, tamanho=28, centralizado=False):
    """Escreve um texto na tela. Se centralizado, (x, y) é o centro."""
    imagem = fonte(tamanho).render(texto, True, TEXTO)
    if centralizado:
        rect = imagem.get_rect(center=(x, y))
    else:
        rect = imagem.get_rect(topleft=(x, y))
    tela.blit(imagem, rect)


def desenhar_tabuleiro(tela, grade, x, y, esconder_navios, titulo):
    """Desenha um tabuleiro 10x10 com letras, números e título."""
    largura_tab = CELULA * TAMANHO
    desenhar_texto(tela, titulo, x + largura_tab // 2, y - 45, 26, True)
    for i in range(TAMANHO):
        letra = chr(65 + i)
        desenhar_texto(tela, letra, x + i * CELULA + CELULA // 2,
                       y - 14, 22, True)
        desenhar_texto(tela, str(i + 1), x - 16, y + i * CELULA + CELULA // 2,
                       22, True)
    for linha in range(TAMANHO):
        for coluna in range(TAMANHO):
            valor = grade[linha][coluna]
            if esconder_navios and valor == "N":
                valor = "~"
            rect = pygame.Rect(x + coluna * CELULA, y + linha * CELULA,
                               CELULA, CELULA)
            pygame.draw.rect(tela, CORES_CELULA[valor], rect)
            pygame.draw.rect(tela, BORDA, rect, 1)


def celula_clicada(pos_mouse, x, y):
    """Retorna (linha, coluna) da célula clicada, ou None se estiver
    fora do tabuleiro."""
    mx, my = pos_mouse
    coluna = (mx - x) // CELULA
    linha = (my - y) // CELULA
    if 0 <= linha < TAMANHO and 0 <= coluna < TAMANHO:
        return linha, coluna
    return None


def para_coordenada(linha, coluna):
    """Converte índices (linha, coluna) para o formato de texto (ex.: 'A1')."""
    return f"{chr(65 + coluna)}{linha + 1}"


def maximizar_janela():
    """Maximiza a janela do jogo (apenas no Windows; nos outros sistemas
    a janela abre no tamanho normal e pode ser maximizada manualmente)."""
    janela = pygame.display.get_wm_info().get("window")
    if sys.platform == "win32" and janela:
        ctypes.windll.user32.ShowWindow(janela, 3)  # 3 = SW_MAXIMIZE


def grade_vazia():
    """Cria uma grade 10x10 só com água."""
    return [["~"] * TAMANHO for _ in range(TAMANHO)]


class JogoGUI:
    def __init__(self):
        # Suaviza a ampliação da tela quando a janela é maximizada.
        os.environ["SDL_RENDER_SCALE_QUALITY"] = "linear"
        pygame.init()
        # SCALED: o jogo é desenhado em 900x600 e ampliado para o tamanho
        # da janela, mantendo a proporção e ajustando as posições do mouse.
        self.tela = pygame.display.set_mode((LARGURA, ALTURA),
                                            pygame.SCALED | pygame.RESIZABLE)
        pygame.display.set_caption("Batalha Naval - GPTech Games")
        maximizar_janela()
        self.relogio = pygame.time.Clock()
        self.rodando = True
        self.tela_atual = "menu"
        self.botoes = []

    # ---------- Laço principal ----------

    def executar(self):
        while self.rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False
                elif (evento.type == pygame.MOUSEBUTTONDOWN
                      and evento.button == 1):
                    self.tratar_clique(evento.pos)
            self.tela.fill(FUNDO)
            self.botoes = []
            self.desenhar()
            pygame.display.flip()
            self.relogio.tick(30)
        pygame.quit()

    def desenhar(self):
        """Chama a função de desenho da tela atual (ex.: desenhar_menu)."""
        getattr(self, "desenhar_" + self.tela_atual)()

    def tratar_clique(self, pos):
        for rect, acao in self.botoes:
            if rect.collidepoint(pos):
                acao()
                return
        if self.tela_atual == "partida" and not self.aguardando_troca:
            celula = celula_clicada(pos, *TAB_DIR)
            if celula is not None:
                self.atacar(*celula)

    def ir_para(self, tela):
        self.tela_atual = tela

    def botao(self, texto, x, y, acao, largura=260, altura=45):
        """Desenha um botão e registra a ação executada ao clicar nele."""
        rect = pygame.Rect(x, y, largura, altura)
        if rect.collidepoint(pygame.mouse.get_pos()):
            cor = BOTAO_HOVER
        else:
            cor = BOTAO
        pygame.draw.rect(self.tela, cor, rect, border_radius=6)
        desenhar_texto(self.tela, texto, rect.centerx, rect.centery, 26, True)
        self.botoes.append((rect, acao))

    def botao_centralizado(self, texto, y, acao):
        self.botao(texto, (LARGURA - 260) // 2, y, acao)

    # ---------- Menus ----------

    def desenhar_menu(self):
        desenhar_texto(self.tela, "BATALHA NAVAL - GPTECH GAMES",
                       LARGURA // 2, 100, 48, True)
        self.botao_centralizado("Nova partida", 190,
                                lambda: self.ir_para("modo"))
        self.botao_centralizado("Ver estatísticas", 250,
                                lambda: self.ir_para("estatisticas"))
        self.botao_centralizado("Assistir replay", 310,
                                lambda: self.abrir_replay("menu"))
        self.botao_centralizado("Créditos", 370,
                                lambda: self.ir_para("creditos"))
        self.botao_centralizado("Sair", 430, self.sair)

    def sair(self):
        self.rodando = False

    def desenhar_modo(self):
        desenhar_texto(self.tela, "Selecione o modo de jogo",
                       LARGURA // 2, 120, 40, True)
        self.botao_centralizado("Jogador vs Computador", 220,
                                lambda: self.iniciar_partida(True))
        self.botao_centralizado("Dois Jogadores", 280,
                                lambda: self.iniciar_partida(False))
        self.botao_centralizado("Voltar", 380, lambda: self.ir_para("menu"))

    def desenhar_estatisticas(self):
        desenhar_texto(self.tela, "ESTATÍSTICAS", LARGURA // 2, 100, 44, True)
        dados = calcular_estatisticas()
        if dados is None:
            desenhar_texto(self.tela, "Nenhuma partida foi jogada ainda.",
                           LARGURA // 2, 250, 30, True)
        else:
            linhas = [
                f"Partidas jogadas: {dados['partidas']}",
                f"Total de jogadas: {dados['jogadas']}",
                f"Acertos: {dados['acertos']}",
                f"Aproveitamento: {dados['aproveitamento']:.1f}%",
            ]
            for i, linha in enumerate(linhas):
                desenhar_texto(self.tela, linha, LARGURA // 2, 190 + i * 45,
                               32, True)
        self.botao_centralizado("Voltar", 450, lambda: self.ir_para("menu"))

    def desenhar_creditos(self):
        desenhar_texto(self.tela, "CRÉDITOS", LARGURA // 2, 100, 44, True)
        linhas = [
            "Nome do desenvolvedor: Débora Camargo",
            "Professor: Guido Pantuza",
            "Disciplina: Programação em Python",
            "Nome do Projeto: GPTech Games",
        ]
        for i, linha in enumerate(linhas):
            desenhar_texto(self.tela, linha, LARGURA // 2, 190 + i * 45,
                           32, True)
        self.botao_centralizado("Voltar", 450, lambda: self.ir_para("menu"))

    # ---------- Preparação da partida ----------

    def iniciar_partida(self, contra_computador):
        self.contra_computador = contra_computador
        self.j1 = Jogador()
        self.j2 = Jogador()
        self.historico = []
        self.mensagens = []
        self.aguardando_troca = False
        self.frota_atual = 1
        self.ir_para("frota")

    def sortear_novamente(self):
        if self.frota_atual == 1:
            self.j1 = Jogador()
        else:
            self.j2 = Jogador()

    def confirmar_frota(self):
        if self.frota_atual == 1 and not self.contra_computador:
            self.frota_atual = 2
        else:
            self.comecar_batalha()

    def comecar_batalha(self):
        if self.contra_computador:
            nome_j2 = "Computador"
        else:
            nome_j2 = "Jogador 2"
        self.nomes = {self.j1: "Jogador 1", self.j2: nome_j2}
        self.atacante = self.j1
        self.defensor = self.j2
        self.inicio = time.time()
        if self.contra_computador:
            self.ir_para("partida")
        else:
            self.ir_para("passar_vez")

    # ---------- Sair da partida antes do fim ----------

    def botao_sair_partida(self):
        """Botão no canto da tela para abandonar a partida em andamento."""
        self.botao("Sair da partida", 15, 15, self.pedir_saida,
                   largura=150, altura=35)

    def pedir_saida(self):
        self.tela_antes_sair = self.tela_atual
        self.ir_para("confirmar_saida")

    def desenhar_confirmar_saida(self):
        desenhar_texto(self.tela, "Deseja sair da partida?",
                       LARGURA // 2, 200, 44, True)
        desenhar_texto(self.tela, "A partida não será salva no replay "
                       "nem nas estatísticas.", LARGURA // 2, 260, 28, True)
        self.botao("Sim, sair", LARGURA // 2 - 280, 340,
                   lambda: self.ir_para("menu"))
        self.botao("Não, continuar", LARGURA // 2 + 20, 340,
                   lambda: self.ir_para(self.tela_antes_sair))

    def desenhar_frota(self):
        if self.frota_atual == 1:
            jogador = self.j1
        else:
            jogador = self.j2
        desenhar_texto(self.tela, f"CONFERÊNCIA DE FROTA - JOGADOR "
                       f"{self.frota_atual}", LARGURA // 2, 40, 40, True)
        desenhar_tabuleiro(self.tela, jogador.tabuleiro.grade, *TAB_CENTRO,
                           False, "Seus navios")
        self.botao("Sortear novamente", LARGURA // 2 - 280, 490,
                   self.sortear_novamente)
        self.botao("Pronto", LARGURA // 2 + 20, 490, self.confirmar_frota)
        self.botao_sair_partida()

    def desenhar_passar_vez(self):
        nome = self.nomes[self.atacante]
        desenhar_texto(self.tela, f"Vez do {nome}", LARGURA // 2, 220,
                       48, True)
        desenhar_texto(self.tela, "Passe o computador e clique em Continuar.",
                       LARGURA // 2, 280, 30, True)
        self.botao_centralizado("Continuar", 360,
                                lambda: self.ir_para("partida"))
        self.botao_sair_partida()

    # ---------- Partida ----------

    def desenhar_partida(self):
        nome_atacante = self.nomes[self.atacante]
        nome_defensor = self.nomes[self.defensor]
        desenhar_texto(self.tela, f"Vez do {nome_atacante}", LARGURA // 2, 30,
                       38, True)
        desenhar_tabuleiro(self.tela, self.atacante.tabuleiro.grade, *TAB_ESQ,
                           False, f"Sua frota ({nome_atacante})")
        desenhar_tabuleiro(self.tela, self.defensor.tabuleiro.grade, *TAB_DIR,
                           True, f"Ataque aqui ({nome_defensor})")
        for i, mensagem in enumerate(self.mensagens):
            desenhar_texto(self.tela, mensagem, LARGURA // 2, 500 + i * 28,
                           26, True)
        if self.aguardando_troca:
            self.botao_centralizado("Passar a vez", 545, self.passar_vez)
        self.botao_sair_partida()

    def registrar(self, jogador, coordenada, resultado):
        self.historico.append({
            "jogador": self.nomes[jogador],
            "coordenada": coordenada,
            "resultado": resultado,
        })

    def atacar(self, linha, coluna):
        coordenada = para_coordenada(linha, coluna)
        resultado = self.atacante.jogar(coordenada, self.defensor)
        if resultado == "invalida":
            self.mensagens = ["Posição já atacada - escolha outra."]
            return
        self.registrar(self.atacante, coordenada, resultado)
        self.mensagens = [f"{coordenada}: {MENSAGENS_JOGADOR[resultado]}"]
        if self.defensor.perdeu():
            self.encerrar_partida()
            return

        if self.contra_computador:
            coordenada = jogada_computador(self.j2, self.j1)
            resultado = self.j2.jogar(coordenada, self.j1)
            self.registrar(self.j2, coordenada, resultado)
            self.mensagens.append(f"O computador jogou {coordenada}: "
                                  f"{MENSAGENS_COMPUTADOR[resultado]}")
            if self.j1.perdeu():
                self.encerrar_partida()
        else:
            self.aguardando_troca = True

    def passar_vez(self):
        self.atacante, self.defensor = self.defensor, self.atacante
        self.aguardando_troca = False
        self.mensagens = []
        self.ir_para("passar_vez")

    def encerrar_partida(self):
        if self.j1.perdeu():
            self.vencedor = self.nomes[self.j2]
        else:
            self.vencedor = self.nomes[self.j1]
        self.duracao = time.time() - self.inicio
        salvar_partida(self.vencedor, len(self.historico), self.historico)
        self.ir_para("fim")

    def desenhar_fim(self):
        desenhar_texto(self.tela, "FIM DO JOGO", LARGURA // 2, 90, 50, True)
        linhas = [
            f"Vencedor: {self.vencedor}",
            f"Total de jogadas: {len(self.historico)}",
            f"Tempo de partida: {formatar_duracao(self.duracao)}",
        ]
        for i, linha in enumerate(linhas):
            desenhar_texto(self.tela, linha, LARGURA // 2, 170 + i * 45,
                           32, True)
        self.botao_centralizado("Ver replay", 340,
                                lambda: self.abrir_replay("fim"))
        self.botao_centralizado("Nova partida", 400,
                                lambda: self.iniciar_partida(
                                    self.contra_computador))
        self.botao_centralizado("Menu principal", 460,
                                lambda: self.ir_para("menu"))

    # ---------- Replay ----------

    def abrir_replay(self, origem):
        self.origem_replay = origem
        self.replay = carregar_replay()
        self.replay_indice = 1
        self.ir_para("replay")

    def mudar_jogada(self, passo):
        novo = self.replay_indice + passo
        if 1 <= novo <= len(self.replay):
            self.replay_indice = novo

    def sair_do_replay(self):
        self.ir_para(self.origem_replay)

    def desenhar_replay(self):
        if not self.replay:
            desenhar_texto(self.tela, "Nenhuma partida foi jogada ainda.",
                           LARGURA // 2, 250, 30, True)
            self.botao_centralizado("Voltar", 450, self.sair_do_replay)
            return

        # Reconstrói os tiros de cada jogador até a jogada atual.
        tiros_j1 = grade_vazia()
        tiros_j2 = grade_vazia()
        nome_j2 = "Adversário"
        for jogada in self.replay[:self.replay_indice]:
            linha, coluna = converter_coordenada(jogada["coordenada"])
            if jogada["resultado"] == "agua":
                marca = "O"
            else:
                marca = "X"
            if jogada["jogador"] == "Jogador 1":
                tiros_j1[linha][coluna] = marca
            else:
                tiros_j2[linha][coluna] = marca
                nome_j2 = jogada["jogador"]

        atual = self.replay[self.replay_indice - 1]
        desenhar_texto(self.tela,
                       f"Jogada {self.replay_indice}/{len(self.replay)} - "
                       f"{atual['jogador']} - {atual['coordenada']} - "
                       f"{atual['resultado'].capitalize()}",
                       LARGURA // 2, 40, 32, True)
        desenhar_tabuleiro(self.tela, tiros_j1, *TAB_ESQ, False,
                           "Tiros do Jogador 1")
        desenhar_tabuleiro(self.tela, tiros_j2, *TAB_DIR, False,
                           f"Tiros do {nome_j2}")
        self.botao("Anterior", 100, 520, lambda: self.mudar_jogada(-1),
                   largura=200)
        self.botao("Próxima", 350, 520, lambda: self.mudar_jogada(1),
                   largura=200)
        self.botao("Voltar", 600, 520, self.sair_do_replay, largura=200)


if __name__ == "__main__":
    # Garante que a pasta data/ seja encontrada mesmo abrindo o arquivo
    # a partir de outro diretório.
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    JogoGUI().executar()
