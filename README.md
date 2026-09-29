# Batalha Naval - GPTech Games

Documentação do sistema de Batalha Naval desenvolvido em Python, com suporte a partidas contra inteligência artificial ou entre dois jogadores humanos, persistência de dados, estatísticas de desempenho e reprodução de histórico de jogadas (replay).

---

## Sumário

- [1. Sobre o Projeto](#1-sobre-o-projeto)
- [2. Autora e Créditos](#2-autora-e-créditos)
- [3. Estrutura de Arquivos](#3-estrutura-de-arquivos)
- [4. Módulos e Funções](#4-módulos-e-funções)
  - [4.1 main.py](#41-mainpy)
  - [4.2 utils.py](#42-utilspy)
  - [4.3 tabuleiro.py](#43-tabuleiropy)
  - [4.4 navios.py](#44-naviospy)
  - [4.5 jogador.py](#45-jogadorpy)
  - [4.6 computador.py](#46-computadorpy)
  - [4.7 partida.py](#47-partidapy)
  - [4.8 replay.py](#48-replaypy)
  - [4.9 estatisticas.py](#49-estatisticaspy)
  - [4.10 menu.py](#410-menupy)
- [5. Como Executar](#5-como-executar)

---

## 1. Sobre o Projeto

O projeto é uma implementação completa do jogo de tabuleiro Batalha Naval via linha de comando. Ele permite a alocação automática de frota em uma grade de $10 \times 10$, validação estrita de coordenadas, persistência do histórico em formato JSON, cálculo de métricas e exibição turno a turno da última partida disputada.

---

## 2. Autora e Créditos

- **Desenvolvedora:** Débora Cristina Barbosa Camargo
- **Professor Orientador:** Guido Pantuza
- **Disciplina:** Programação em Python
- **Empresa/Projeto:** GPTech Games

---

## 3. Estrutura de Arquivos

```text
.
├── data/
│   ├── estatisticas.json    # Registro acumulado das partidas finalizadas
│   └── replay.json          # Histórico detalhado de jogadas da última partida
├── computador.py            # Lógica das jogadas automáticas do computador
├── estatisticas.py          # Leitura e apresentação das métricas do jogador
├── jogador.py               # Classe Jogador e regras de turno/ataque
├── main.py                  # Ponto de entrada do programa
├── menu.py                  # Interfaces de menu principal e submenus
├── navios.py                # Classe Navio e geração/posicionamento de frotas
├── partida.py               # Controle do fluxo da partida e persistência
├── replay.py                # Reprodutor do histórico de jogadas
├── tabuleiro.py             # Classe Tabuleiro e renderização gráfica via terminal
└── utils.py                 # Funções auxiliares de conversão de coordenadas
```

---

## 4. Módulos e Funções

### 4.1 main.py

Ponto de entrada para inicialização do jogo.

* `if __name__ == "__main__":`  
  Invoca a função `exibir_menu()` do módulo `menu.py` para dar início ao programa.

---

### 4.2 utils.py

Contém rotinas utilitárias para manipulação e conversão de dados.

* `converter_coordenada(coordenada)`  
  Recebe uma string com uma coordenada no formato letra-número (ex.: `"A1"`, `"C5"`, `"J10"`) e a converte em uma tupla de inteiros `(linha, coluna)` indexados em zero, apropriados para manipulação de matrizes.

---

### 4.3 tabuleiro.py

Gerencia a estrutura e a renderização da grade do jogo.

* `Tabuleiro.__init__()`  
  Instancia um tabuleiro $10 \times 10$ inicializado com o caractere `"~"`, representando água.
* `Tabuleiro.posicionar_navios(navios)`  
  Aloca os navios da frota no tabuleiro, atribuindo a letra `"N"` a cada coordenada ocupada.
* `Tabuleiro._exibir(esconder_navios)`  
  Método privado que imprime a grade formatada no terminal com eixos horizontais (A-J) e verticais (1-10). Quando `esconder_navios` é verdadeiro, substitui as posições `"N"` por `"~"`.
* `Tabuleiro.exibir_proprio()`  
  Chama `_exibir(False)` para mostrar o tabuleiro completo com a frota visível.
* `Tabuleiro.exibir_adversario()`  
  Chama `_exibir(True)` para ocultar os navios do oponente durante a fase de ataque.

---

### 4.4 navios.py

Mapeia as embarcações e provê a lógica de sorteio e posicionamento.

* `Navio.__init__(coordenadas)`  
  Cria o objeto da embarcação, armazenando suas coordenadas e um vetor de booleanos (`atingidas`) inicializado como `False` para acompanhar os acertos.
* `Navio.registrar_tiro(posicao)`  
  Verifica se a posição disparada faz parte do navio. Se fizer, marca a posição como atingida e retorna `True`; caso contrário, retorna `False`.
* `Navio.afundado()`  
  Retorna `True` caso todas as posições da embarcação tenham sido atingidas.
* `gerar_coordenadas(linha_inicial, coluna_inicial, tamanho, horizontal)`  
  Gera uma sequência de coordenadas ordenadas a partir de uma posição inicial, respeitando a orientação (horizontal ou vertical).
* `dentro_do_tabuleiro(coordenadas)`  
  Verifica se todas as coordenadas pertencem aos limites do tabuleiro ($0 \le \text{linha} \le 9$ e $0 \le \text{coluna} \le 9$).
* `sem_sobreposicao(coordenadas_novo_navio, ocupadas)`  
  Valida se as coordenadas de um novo navio não colidem com posições de navios já alocados.
* `posicionar_navio(tamanho, ocupadas)`  
  Gera posições aleatórias continuamente até encontrar uma combinação válida e livre para um determinado tamanho de navio.
* `criar_frota()`  
  Instancia e retorna uma frota completa contendo 8 navios (2 navios de tamanho 4 e 6 navios de tamanho 2).

---

### 4.5 jogador.py

Abstrai as ações de um participante do jogo.

* `Jogador.__init__()`  
  Instancia o tabuleiro e a frota do jogador, posicionando as embarcações automaticamente.
* `Jogador.jogada_valida(coordenada, oponente)`  
  Valida se a coordenada informada pelo jogador é sintaticamente correta, está dentro dos limites do tabuleiro e ainda não foi atacada anteriormente.
* `Jogador.jogar(coordenada, oponente)`  
  Aplica o ataque no oponente. Retorna `"invalida"` para disparos incorretos, `"agua"` quando não atinge nada, `"acerto"` quando atinge um segmento e `"afundou"` caso a embarcação seja destruída.
* `Jogador.perdeu()`  
  Avalia se todas as embarcações da frota do jogador foram afundadas.

---

### 4.6 computador.py

Controla as ações automatizadas da inteligência artificial.

* `sortear_coordenada()`  
  Gera aleatoriamente uma coordenada formatada em string (ex.: `"E7"`).
* `jogada_computador(computador, oponente)`  
  Realiza sorteios sucessivos até obter uma coordenada que represente uma jogada válida contra o oponente.

---

### 4.7 partida.py

Gerencia o ciclo de vida completo de um jogo e a persistência de dados.

* `jogar_partida(contra_computador=False)`  
  Coordena os turnos entre os dois participantes, colhe as entradas do usuário ou do computador, atualiza os estados dos tabuleiros, contabiliza o tempo e registra o histórico da partida.
* `exibir_resultado(vencedor, total_jogadas, duracao)`  
  Formatada e exibe o painel de encerramento com informações de vencedor, total de rodadas e duração em formato $HH:MM:SS$.
* `exibir_opcoes_fim_jogo(contra_computador)`  
  Exibe o menu de opções pós-partida, permitindo rever o replay, iniciar um novo jogo ou retornar ao menu principal.
* `iniciar_partida(contra_computador=False)`  
  Função controladora que chama `jogar_partida`, grava o histórico em `data/replay.json` e atualiza o arquivo `data/estatisticas.json`.

---

### 4.8 replay.py

Módulo para reprodução passo a passo de partidas passadas.

* `exibir_replay()`  
  Carrega o arquivo `data/replay.json` e exibe sequencialmente cada jogada realizada na partida anterior, permitindo que o usuário avance manualmente ou encerre a visualização.

---

### 4.9 estatisticas.py

Módulo responsável pela consolidação e exibição de estatísticas.

* `exibir_estatisticas()`  
  Lê os registros do arquivo `data/replay.json`, calcula a quantidade de disparos, total de acertos e percentual de aproveitamento do jogador.

---

### 4.10 menu.py

Interface em modo texto para interação e navegação do usuário.

* `nova_partida()`  
  Apresenta o submenu para escolha do modo de jogo (Jogador vs Computador ou Dois Jogadores).
* `creditos()`  
  Exibe as informações sobre a desenvolvedora, orientador e instituição.
* `exibir_menu()`  
  Menu principal do jogo que direciona para a criação de partidas, estatísticas, replay, créditos ou encerramento.
* `exibir_opcoes_fim_jogo(contra_computador)`  
  Menu de navegação exibido ao final de cada partida.

---

## 5. Como Executar

1. Certifique-se de ter o **Python 3.8** ou superior instalado no seu sistema.
2. Navegue até o diretório do projeto via terminal:

```bash
python main.py
