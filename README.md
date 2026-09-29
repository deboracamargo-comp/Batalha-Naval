# 🚢 Batalha Naval — GPTech Games

> Trabalho 1 da disciplina **Programação em Python**
> Professor: Guido Pantuza — CEFET-MG, Campus Divinópolis
> Desenvolvedora: **Débora Cristina Barbosa Camargo**

Implementação do jogo Batalha Naval em modo texto, em Python, a partir do
Documento de Requisitos do projeto fictício "Sistema de Batalha Naval —
GPTech Games". O projeto foi construído em Programação Orientada a
Objetos, modularizado por responsabilidade e com persistência de dados em
JSON.

🔗 **Repositório:** https://github.com/deboracamargo-comp/Batalha-Naval
🎥 **Vídeo de demonstração:** [link do vídeo]

---

## 📋 Sumário

- [Como executar](#-como-executar)
- [Como jogar](#-como-jogar)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Decisões de projeto](#-decisões-de-projeto)
- [Funcionalidades](#-funcionalidades-implementadas)
- [Requisitos não funcionais](#-requisitos-não-funcionais)
- [Diário de desenvolvimento](#-diário-de-desenvolvimento)

---

## ▶️ Como executar

Requer **Python 3.10** ou superior. A versão de terminal não precisa de
nenhuma dependência externa — só a biblioteca padrão.

```bash
git clone [link do repositório]
cd BatalhaNaval
python main.py
```

O jogo abre direto no menu principal.

### Interface gráfica (PyGame)

Também há uma versão com janela, que usa a mesma lógica do jogo de terminal.
Ela precisa do PyGame (no Python 3.14+, use o `pygame-ce`, que tem a mesma API):

```bash
pip install -r requirements.txt
python gui.py
```

Na interface gráfica, o ataque é feito clicando numa célula do tabuleiro
adversário (à direita). No modo Dois Jogadores, uma tela de "passe o
computador" aparece entre os turnos para que um jogador não veja os navios
do outro.

## 🎮 Como jogar

Ao iniciar uma nova partida, o programa pergunta o modo de jogo:

| Opção | Modo                 | Descrição                                      |
|:-----:|----------------------|-------------------------------------------------|
| 1     | Jogador vs Computador | Você joga contra um oponente controlado pelo computador, que joga de forma autônoma. |
| 2     | Dois Jogadores        | Dois jogadores humanos se alternam no mesmo terminal. |

Antes da partida começar, cada jogador vê seu próprio tabuleiro para
conferir o posicionamento da frota (sorteada automaticamente). A cada
turno, o atacante digita uma coordenada no formato **letra + número**
(ex.: `C5`, colunas de A a J, linhas de 1 a 10) para atirar no tabuleiro
adversário.

Ao final da partida, é possível:

- ver o replay, jogada a jogada, da partida que acabou de terminar;
- iniciar uma nova partida no mesmo modo;
- voltar ao menu principal.

## 🗂️ Estrutura do projeto
BatalhaNaval/
├── main.py # Ponto de entrada: abre o menu principal
├── menu.py # Menu principal e seleção de modo de jogo
├── partida.py # Fluxo de uma partida: turnos, fim de jogo,
│ # persistência de replay e estatísticas
├── tabuleiro.py # Classe Tabuleiro: grade 10x10 e exibição
├── navios.py # Classe Navio e posicionamento automático da frota
├── jogador.py # Classe Jogador: tabuleiro e frota próprios,
│ # processamento de tiros e validação de jogadas
├── computador.py # Lógica do modo Jogador x Computador
├── utils.py # Conversão de coordenadas (ex.: "C5" → índices)
├── estatisticas.py # Exibição das estatísticas acumuladas
├── replay.py # Reprodução passo a passo do histórico salvo
├── data/ # Arquivos gerados em tempo de execução
│ ├── replay.json # histórico da última partida
│ └── estatisticas.json # estatísticas acumuladas entre partidas
└── docs/ # Documentação complementar

Cada módulo tem uma responsabilidade única (RNF04): `tabuleiro.py` e
`navios.py` conhecem apenas seu próprio domínio, `jogador.py` os combina
para representar um jogador completo, e `partida.py` orquestra o fluxo do
jogo sem se preocupar com os detalhes internos de cada peça.

## 🧠 Decisões de projeto

- **Paradigma.** O jogo foi implementado em Programação Orientada a
  Objetos, com `Tabuleiro`, `Navio` e `Jogador` como núcleo do domínio.

- **Composição da frota.** Cada jogador recebe 2 navios grandes (4
  posições) e 6 navios pequenos (2 posições) — 20 das 100 posições do
  tabuleiro. O enunciado não fixa a quantidade de navios por tipo; esse
  número foi escolhido para equilibrar duração e dificuldade da partida.

- **Posicionamento automático.** Cada navio é posicionado por sorteio de
  posição inicial e orientação (horizontal ou vertical). A cada
  tentativa, verifica-se se todas as posições calculadas cabem dentro do
  tabuleiro e não colidem com navios já posicionados; caso contrário, uma
  nova tentativa é sorteada, até encontrar uma posição válida.

- **`main.py` como porta de entrada única.** Toda a lógica de partida foi
  isolada em `partida.py`, e `main.py` apenas inicia o menu. Isso evita
  uma dependência circular entre `menu.py` (que precisa iniciar uma
  partida) e a lógica de jogo, e deixa o ponto de entrada do programa
  fácil de entender de relance.

- **Persistência em JSON.** O histórico de jogadas de cada partida é
  salvo em `data/replay.json`, sobrescrito a cada partida (guarda sempre
  a *última*). As estatísticas ficam em `data/estatisticas.json`, como
  uma lista que cresce a cada partida jogada — permitindo calcular o
  aproveitamento acumulado, não apenas o da última partida.

- **Modo Jogador x Computador.** O computador sorteia coordenadas e só
  efetiva a jogada quando ela é válida, reaproveitando exatamente a
  mesma validação usada para jogadas humanas — garantindo que as duas
  formas de jogar sigam as mesmas regras.

- **Validação de entradas.** Conversões de coordenada e leitura de opções
  numéricas de menu são protegidas com `try`/`except`, para que uma
  entrada mal formatada gere uma mensagem de erro, e não o encerramento
  do programa.

## ✅ Funcionalidades implementadas

| Requisito | Descrição                                              | Status |
|:---------:|----------------------------------------------------------|:------:|
| RF01      | Menu principal com as opções do sistema                  | ✅ |
| RF02      | Tabuleiro 10x10 por jogador                               | ✅ |
| RF03      | Navios pequeno (2) e grande (4 posições)                  | ✅ |
| RF04      | Posicionamento automático sem sobreposição                | ✅ |
| RF05      | Validação de jogadas (limites e repetição)                 | ✅ |
| RF06      | Mensagens de água, acerto e navio afundado                  | ✅ |
| RF07      | Fim de partida com vencedor, jogadas e tempo                 | ✅ |
| RF08      | Nova partida a qualquer momento pelo menu                     | ✅ |
| RF09      | Modos Jogador x Computador e Dois Jogadores                    | ✅ |
| RF10      | Posicionamento e conferência dos navios                         | ✅ |
| RF11      | Histórico de jogadas da partida                                  | ✅ |
| RF12      | Estatísticas de desempenho acumuladas                              | ✅ |
| RF13      | Replay passo a passo da última partida                              | ✅ |

## ⚙️ Requisitos não funcionais

- Implementação em **Python 3.10+**
- Código aderente ao **PEP 8** (verificado com Flake8)
- Sistema **organizado em módulos coesos**, um por responsabilidade
- **Tratamento de erros** nas entradas do usuário
- Execução validada em ambiente Windows/Linux via terminal

## 📓 Diário de desenvolvimento

O desenvolvimento seguiu incrementalmente, módulo a módulo, começando pelo
tabuleiro e pela conversão de coordenadas, passando pela classe de navios e
seu posicionamento automático, depois pela classe de jogador e a lógica de
turnos, até chegar ao menu, ao modo contra o computador e à persistência de
replay e estatísticas. As principais dificuldades encontradas foram:

- Um bug clássico de Python vindo de C: `[[...] * 10] * 10` cria referências
  repetidas para a mesma lista interna, em vez de linhas independentes —
  resolvido construindo a grade com um laço aninhado.
- Uma validação de jogada que rejeitava indevidamente posições com navio
  ainda não atingido (tratava apenas `"~"` como válido, não `"N"`) —
  corrigida para tratar como inválidas apenas posições já marcadas com
  `"X"` ou `"O"`.
- Uma dependência circular entre o menu e a lógica de partida, resolvida
  isolando o fluxo de partida em um módulo próprio (`partida.py`).
