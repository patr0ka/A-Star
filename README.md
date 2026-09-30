<div align="center">

# 🌟 Algoritmo A* (A-Star) - Pathfinding Interativo

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Concluído-success)](#)
[![Disciplina](https://img.shields.io/badge/IA%20I-UNICENTRO-orange)](#)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Standard%20Lib-brightgreen)](#)
[![Licença](https://img.shields.io/badge/License-MIT-lightgrey)](#)

> **Implementação robusta e visual do algoritmo de busca heurística A* (A-Star) em Python, projetado para encontrar o caminho de menor custo em grids 2D com múltiplos tipos de terrenos e animação em tempo real no terminal.**

---

</div>

## 📌 Sumário

- [Visão Geral](#-visão-geral)
- [Funcionalidades Principais](#-funcionalidades-principais)
- [Fundamentação Teórica](#-fundamentação-teórica)
  - [Como Funciona o A*](#como-funciona-o-a)
  - [Heurística de Manhattan](#heurística-de-manhattan)
- [Tabela de Custos e Terrenos](#-tabela-de-custos-e-terrenos)
- [Como Executar](#-como-executar)
  - [Pré-requisitos](#pré-requisitos)
  - [Executando o Programa](#executando-o-programa)
- [Modos de Operação](#-modos-de-operação)
- [Uso Programático](#-uso-programático)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Documentação Técnica](#-documentação-técnica)
- [Autor](#-autor)

---

## 🧭 Visão Geral

O **A*** é um dos algoritmos de busca de caminho mais populares e eficientes da Ciência da Computação e Inteligência Artificial. Diferente de algoritmos de busca cega (como BFS ou DFS) ou busca por custo uniforme (Dijkstra), o A* combina o custo real acumulado com uma **heurística orientada a objetivos**, garantindo encontrar o caminho ótimo com máxima eficiência.

Este projeto foi desenvolvido com foco educacional e prático, apresentando:
- Interface interativa via terminal CLI.
- Visualização gráfica colorida via códigos **ANSI**.
- Modo animado em tempo real com taxa de atualização configurável.
- Diversos geradores de mapas procedurais e labirintos.

---

## ✨ Funcionalidades Principais

- 🎯 **Busca Ótima Garantida**: Encontra sempre o caminho de **menor custo total** (não apenas menor quantidade de células).
- ⚡ **Fila de Prioridade Eficiente**: Utiliza min-heap (`heapq`) com complexidade $O(\log n)$ para extração de nós.
- 🎨 **Visualização em Cores ANSI**: Destaque para nós abertos, nós fechados, caminho percorrido, obstáculos e perigos.
- 🎬 **3 Modos de Execução**:
  - **Silencioso**: Execução instantânea com estatísticas finais completas.
  - **Verbose**: Passo a passo detalhado no terminal.
  - **Animado**: Reprodução em tempo real diretamente na tela.
- 🧩 **6 Tipos de Grids Pré-configurados**:
  - Grid Simples (Exemplo inicial)
  - Grid Complexo (Cenário estratégico)
  - Grid Aleatório (Configurável)
  - Grid em Labirinto (Paredes e corredores)
  - Grid Esparso (Terreno aberto)
  - Grid Denso (Desafio de navegação difícil)
- 📦 **Zero Dependências Externas**: Executa diretamente com a biblioteca padrão do Python (`heapq`, `time`, `random`, `os`, `sys`).

---

## 🧠 Fundamentação Teórica

### Como Funciona o A*

O A* avalia os nós na fronteira de busca utilizando a função de avaliação:

$$f(n) = g(n) + h(n)$$

Onde:
- **$g(n)$**: Custo real acumulado para viajar do ponto inicial até o nó atual $n$.
- **$h(n)$**: Estimativa heurística do custo restante do nó $n$ até o objetivo.
- **$f(n)$**: Custo total estimado do caminho passando pelo nó $n$.

### Heurística de Manhattan

Por ser uma malha ortogonal (movimentação em 4 direções: Cima, Baixo, Esquerda, Direita), a heurística adotada é a **Distância de Manhattan**:

$$h(n) = |x_n - x_{\text{alvo}}| + |y_n - y_{\text{alvo}}|$$

> **Propriedades da Heurística**:
> - **Admissível**: Nunca superestima o custo real até o destino ($h(n) \le h^*(n)$), assegurando otimalidade.
> - **Consistente**: Respeita a desigualdade triangular ($h(n) \le c(n, a, n') + h(n')$).

---

## 🗺️ Tabela de Custos e Terrenos

| Símbolo | Cor / Estilo | Terreno | Custo | Transponível? | Descrição |
|:-------:|:------------:|:--------|:-----:|:-------------:|:----------|
| `S` | 🟢 Verde | **Início (Start)** | `1` | Sim | Ponto de partida do agente |
| `E` | 🔵 Azul | **Objetivo (End)** | `1` | Sim | Ponto de destino da busca |
| `.` | ⚪ Branco | **Caminho Livre** | `1` | Sim | Terreno plano padrão |
| `F` | 🔴 Vermelho | **Fogo (Hazard)** | `5` | Sim | Área perigosa (custo elevado) |
| `Z` | ⚫ Preto | **Inimigo (Threat)** | `∞` | Não | Bloqueio dinâmico |
| `#` | 🔘 Cinza | **Parede (Obstacle)** | `∞` | Não | Obstáculo intransponível |
| `★` | 🟡 Amarelo | **Caminho Final** | — | — | Caminho ótimo traçado |
| `◆` | 🔵 Ciano | **Explorando** | — | — | Nó sendo avaliado atualmente |
| `●` | ⚪ Cinza Escuro | **Explorado** | — | — | Nó já pertencente ao closed set |

---

## 🚀 Como Executar

### Pré-requisitos

- **Python 3.8+** instalado.
- Terminal com suporte a cores ANSI (Windows Terminal, VS Code, PowerShell, bash, zsh, etc.).

### Executando o Programa

1. Clone o repositório:
```bash
git clone https://github.com/patr0ka/A-Star.git
cd A-Star
```

2. Execute o script principal:
```bash
python a_star.py
```
*(No Linux ou macOS, utilize `python3 a_star.py`)*

3. Siga o menu interativo no terminal:
```text
============================================================
              ALGORITMO DE BUSCA A* (A-STAR)                
============================================================

Escolha o tipo de grid:
  1. Grid Simples (Exemplo inicial)
  2. Grid Complexo (Mais obstáculos)
  3. Grid Aleatório (Configurável)
  4. Grid em Labirinto (Paredes estruturadas)
  5. Grid Esparso (Terreno aberto)
  6. Grid Denso (Muitos obstáculos)

Opções de Visualização:
  1. Modo Silencioso (Execução direta com relatório)
  2. Modo Verbose (Exibe cada iteração no terminal)
  3. Modo Animado (Animação fluida em tempo real)
```

---

## 💻 Uso Programático

Você pode importar as classes e geradores diretamente em seu próprio código Python:

```python
from a_star import AStarPathfinder, create_random_grid

# 1. Cria um grid customizado (linhas, colunas, chances de obstáculos)
grid = create_random_grid(
    rows=12,
    cols=20,
    obstacle_chance=0.15,
    fire_chance=0.08,
    enemy_chance=0.05
)

# 2. Inicializa o pathfinder
pathfinder = AStarPathfinder(grid, verbose=False)

# 3. Executa a busca
path = pathfinder.find_path(animate=False)

# 4. Imprime o mapa com o traçado resultante
if path:
    pathfinder.print_grid_with_path(path)
    print(f"Caminho encontrado com sucesso! Total de passos: {len(path)}")
else:
    print("Nenhum caminho possível até o objetivo.")
```

---

## 📂 Estrutura do Repositório

```text
A-Star/
│
├── a_star.py               # Implementação do algoritmo, nós, geradores e interface CLI
├── A_STAR_DOCUMENTACAO.md  # Relatório técnico com aprofundamento matemático e de complexidade
├── README.md               # Guia do projeto e documentação visual
└── .gitignore              # Regras de exclusão do Git para ambiente limpo
```

---

## 📖 Documentação Técnica

Para uma análise formal completa contendo:
- Complexidade de tempo $O(E \log V)$ e espaço $O(V)$
- Provas matemáticas de admissibilidade
- Comparações detalhadas com Dijkstra e BFS
- Rastreamento passo a passo de nós

Consulte o arquivo [`A_STAR_DOCUMENTACAO.md`](./A_STAR_DOCUMENTACAO.md).

---

## 👤 Autor

Desenvolvido por **Patrick** ([@patr0ka](https://github.com/patr0ka))  
*Universidade Estadual do Centro-Oeste (UNICENTRO)*  
*Curso de Ciência da Computação - Inteligência Artificial I*

---

<div align="center">
  <sub>Feito com dedicação para a disciplina de IA I 🚀</sub>
</div>
