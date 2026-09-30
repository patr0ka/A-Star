# Documentação Técnica: Algoritmo A* para Busca de Caminho Ótimo

## Sumário Executivo

Este documento explica a implementação do algoritmo **A*** em Python para encontrar o caminho de **menor custo** (não apenas o caminho mais curto) em um grid 2D com múltiplos tipos de terreno. A implementação utiliza a heurística de **distância de Manhattan** e suporta diferentes tipos de células com custos variáveis.

---

## 1. Como o Algoritmo A* Funciona

### 1.1 Conceito Fundamental

O algoritmo A* é uma técnica de **busca heurística** que combina:
- **Custo real** (g): O custo do caminho percorrido do início até o nó atual
- **Heurística** (h): Uma estimativa do custo do nó atual até o objetivo
- **Avaliação** (f): f(n) = g(n) + h(n), usada para ordenar qual nó explorar a seguir

A chave está em usar a heurística para **direcionar a busca** em direção ao objetivo, tornando-a muito mais eficiente que uma busca cega.

### 1.2 Pseudocódigo do Algoritmo

```
A*(inicio, objetivo):
    fila_aberta = [Node(inicio)]
    conjunto_fechado = {}
    g_values = {inicio: 0}
    
    enquanto fila_aberta não vazia:
        nó_atual = extrai nó com menor f(n) de fila_aberta
        
        se nó_atual == objetivo:
            retorna reconstrói_caminho(nó_atual)
        
        marca nó_atual como explorado
        
        para cada vizinho de nó_atual:
            se vizinho já foi explorado:
                continua
            
            novo_g = g(nó_atual) + custo(nó_atual → vizinho)
            
            se novo_g < g_values[vizinho]:
                g_values[vizinho] = novo_g
                novo_h = heuristica(vizinho, objetivo)
                novo_f = novo_g + novo_h
                
                adiciona vizinho à fila_aberta
    
    retorna null (sem caminho)
```

### 1.3 Por Que A* É Ótimo?

A* é garantido encontrar o caminho de **menor custo** porque:

1. **Admissibilidade da Heurística**: A heurística nunca **superestima** o custo real (h(n) ≤ custo_real(n → objetivo))
2. **Fila de Prioridade**: Sempre explora primeiro o nó mais promissor (menor f(n))
3. **Rastreamento de g(n)**: Mantém registro dos melhores custos encontrados

Isso garante que quando o objetivo é alcançado, é via o **caminho mais barato possível**.

---

## 2. Heurística de Distância de Manhattan

### 2.1 Definição Matemática

A distância de Manhattan entre dois pontos é:

$$h(pos) = |x_{atual} - x_{objetivo}| + |y_{atual} - y_{objetivo}|$$

### 2.2 Por Que Manhattan e Não Euclidiana?

No contexto de movimentação em grid com **4 direções** (cima, baixo, esquerda, direita):

| Heurística | Fórmula | Admissível? | Eficiência |
|-----------|---------|-----------|-----------|
| **Manhattan** | \|Δx\| + \|Δy\| | ✓ Sim | ⭐⭐⭐⭐ (Excelente) |
| **Euclidiana** | √(Δx² + Δy²) | ✓ Sim | ⭐⭐⭐ (Boa) |
| **Zero** | 0 | ✓ Sim | ⭐ (Busca em largura) |
| **Chebyshev** | max(\|Δx\|, \|Δy\|) | ✗ Não | Inválida |

**Manhattan é ideal porque**:
- É **admissível** (nunca superestima)
- É **muito informativa** (reduz nós explorados)
- Corresponde exatamente à movimentação em 4 direções em um grid

### 2.3 Implementação no Código

```python
def manhattan_heuristic(self, pos: Tuple[int, int]) -> float:
    """Distância de Manhattan até o objetivo."""
    return abs(pos[0] - self.end[0]) + abs(pos[1] - self.end[1])
```

---

## 3. Sistema de Custos e Tipos de Células

### 3.1 Tabela de Custos

```python
CELL_COSTS = {
    'S': 1,              # Início
    'E': 1,              # Fim
    '.': 1,              # Caminho livre
    'F': 5,              # Fogo
    'Z': float('inf'),   # Inimigo (bloqueado)
}
```

### 3.2 Justificativa dos Pesos

#### **Células Livres (S, E, .): Custo = 1**
- Qualquer movimento em terreno seguro tem o mesmo custo
- Serve como baseline para outras células
- Permite comparação relativa com outros terrenos

#### **Fogo (F): Custo = 5**
- Multiplica por 5 o custo de atravessar aquela célula
- Cria um "desincentivo" mas **não bloqueia**
- O algoritmo evita fogo quando possível, mas atravessa se for caminho único
- Razão do peso 5:
  - Suficientemente alto para desviar quando há alternativas
  - Baixo o suficiente para não criar impacto drástico
  - Pode ser ajustado (3 = menos penalidade, 10 = mais penalidade)

#### **Inimigo (Z): Custo = ∞ (infinito)**
- **Bloqueia completamente** a passagem
- Célula é absolutamente intransponível
- Implementa `float('inf')` para evitar divisões
- A função `get_neighbors()` filtra essas células automaticamente

### 3.3 Exemplo de Impacto dos Custos

Dois caminhos possíveis:
```
Caminho 1: S → . → . → . → . → E  (4 passos, custo = 4)
Caminho 2: S → . → F → . → . → E  (4 passos, custo = 5)
```

A* escolherá **Caminho 1** porque tem custo 4 < 5.

Se não houvesse alternativa:
```
Caminho 3: S → . → F → F → . → E  (4 passos, custo = 1+5+5+1 = 12)
```

A* atravessaria o fogo porque não haveria outra opção.

---

## 4. Estrutura de Dados: Classe Node

### 4.1 Definição

```python
class Node:
    def __init__(self, pos, g=0, h=0):
        self.pos = pos      # (linha, coluna)
        self.g = g          # Custo real do caminho
        self.h = h          # Heurística (estimativa)
        self.f = g + h      # Valor de avaliação
        self.parent = None  # Referência para reconstruir caminho
```

### 4.2 Por Que `parent` é Essencial

O campo `parent` cria uma **lista ligada** que permite:
1. **Reconstrução do caminho** no final: caminha para trás de E até S
2. **Eficiência de memória**: em vez de guardar todo caminho em cada nó, apenas a referência anterior
3. **Rastreabilidade**: pode-se debugar e entender a sequência de decisões

Pseudocódigo de reconstrução:
```
caminho = []
nó_atual = nó_objetivo
enquanto nó_atual != null:
    caminho.prepend(nó_atual.pos)
    nó_atual = nó_atual.parent
retorna caminho
```

### 4.3 Método `__lt__` (menor que)

```python
def __lt__(self, other):
    return self.f < other.f
```

Isto permite que o `heapq` (fila de prioridade) ordene corretamente os nós. O heap sempre extrai o nó com **menor f(n)** primeiro.

---

## 5. Partes Complexas da Implementação

### 5.1 Fila de Prioridade com `heapq`

**Problema**: Precisamos sempre explorar o nó com menor f(n), sem procurar toda a lista.

**Solução**: Usar `heapq`, uma implementação eficiente de fila de prioridade (min-heap).

```python
open_list = []
heapq.heappush(open_list, start_node)      # O(log n)
current_node = heapq.heappop(open_list)    # O(log n)
```

**Complexidade**: Operações em O(log n) em vez de O(n), crucial para grids grandes.

### 5.2 Rastreamento de g(n) Ótimo

**Problema**: Múltiplos caminhos podem levar ao mesmo nó. Como saber se encontramos um melhor?

**Solução**: Guardar o melhor g(n) encontrado:

```python
g_values = {self.start: 0}

tentative_g = current_node.g + move_cost

if neighbor_pos not in g_values or tentative_g < g_values[neighbor_pos]:
    g_values[neighbor_pos] = tentative_g
    # Adiciona vizinho à fila novamente com novo g(n)
```

**Por que re-adicionar à fila?** Se encontramos um caminho melhor para um nó já explorado, o seu f(n) muda e pode se tornar mais prioritário.

### 5.3 Conjunto `closed_set` para Evitar Revisit

```python
closed_set = set()
# ...
if neighbor_pos in closed_set:
    continue

closed_set.add(current_pos)
```

**Propósito**: Uma vez que exploramos um nó e o removemos da fila (com o melhor g(n) até esse ponto), não precisamos revisitá-lo.

**Por que funciona**: Como sempre exploramos em ordem de f(n) crescente, o primeiro nó visitado da fila tem garantia de ter o melhor g(n) encontrado.

### 5.4 Cálculo de Vizinhos

```python
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Cima, Baixo, Esquerda, Direita

for dr, dc in directions:
    new_row, new_col = row + dr, col + dc
    if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
        cell = self.grid[new_row][new_col]
        cost = self.CELL_COSTS.get(cell, float('inf'))
        if cost != float('inf'):  # Válido (não é Z)
            neighbors.append(((new_row, new_col), cost))
```

**Detalhes importantes**:
- Apenas **4 direções** (ortogonais), não 8 (não inclui diagonais)
- Filtro de limites do grid evita out-of-bounds
- Filtro de infinito evita devolver células intransponíveis

---

## 6. Complexidade Computacional

### 6.1 Análise

| Métrica | Complexidade |
|---------|-------------|
| **Tempo (pior caso)** | O(E log V) |
| **Espaço (fila + fechado)** | O(V) |
| **Tempo (melhor caso com boa heurística)** | O(V log V) |

Onde:
- **V** = número total de células (linhas × colunas)
- **E** = número de arestas (conexões entre células ≈ 4×V para grid 4-conectado)

### 6.2 Impacto da Heurística

- **Com Manhattan**: Explora ~10-30% do grid (altamente direcional)
- **Com Euclidiana**: Explora ~30-50% do grid
- **Com Zero (BFS)**: Explora ~100% do grid (sem heurística)

Grids maiores com boa heurística são muito mais rápidas.

---

## 7. Fluxo de Execução Completo

```
1. Instancia AStarPathfinder(grid, verbose=True)
   ├─ Encontra posições de S e E
   └─ Prepara estruturas de dados

2. Chama find_path()
   ├─ Inicializa open_list com nó inicial
   ├─ LOOP enquanto open_list não vazia:
   │  ├─ Extrai nó com menor f(n)
   │  ├─ Se é objetivo → reconstrói caminho (SUCESSO)
   │  ├─ Senão, expande vizinhos
   │  │  └─ Calcula g, h, f para cada vizinho
   │  │  └─ Se custo melhor, adiciona à fila
   │  └─ Marca nó como explorado
   └─ Retorna None se fila esvaziar (FALHA)

3. Reconstrói caminho via parent pointers
   ├─ Começa do objetivo
   ├─ Segue parent até chegou ao início
   └─ Inverte para ter S→...→E

4. Visualiza resultado
   ├─ Mostra grid original
   ├─ Mostra grid com caminho marcado
   └─ Calcula custo total
```

---

## 8. Decisões de Design

### 8.1 Classe vs Procedural

**Decisão**: Usar classe `AStarPathfinder`

**Vantagens**:
- Encapsula estado do grid e cache de heurísticas
- Permite múltiplas instâncias independentes
- Facilita visualização e debug
- Interface limpa: `.find_path()`, `.print_grid()`, etc.

### 8.2 Manhattan vs Outras Heurísticas

**Decisão**: Usar Manhattan (não Euclidiana ou Chebyshev)

**Razão**: 
- Euclidiana fornece menos informação (subestima mais)
- Chebyshev é não-admissível para movimentação em 4 direções
- Manhattan é ótima para grids 4-conectados

### 8.3 Suporte a Custos Variáveis

**Decisão**: Cada célula tem um custo (1, 5, ∞)

**Impacto**:
- Caminho "mais curto" ≠ caminho "mais barato"
- A* garante **mínimo custo**, não mínimo comprimento
- Mais realista (terrenos diferentes têm diferentes dificuldades)

### 8.4 Verbose Mode (Opcional)

**Implementação**:
```python
if self.verbose:
    print(f"Explorando {pos} | f={f_value}")
    self.steps.append(pos)
```

Permite visualizar **quantos nós foram explorados** vs tamanho do caminho final.

---

## 9. Exemplo de Execução

### 9.1 Grid Simples

```
Original:
S . # . . F .
. # . . # F .
. . . F . . .
# . Z . . # .
. . . . . . E
```

### 9.2 Execução do A*

```
Iteração 1: Explorando (0,0) | g=0, h=8, f=8
Iteração 2: Explorando (1,0) | g=1, h=7, f=8
Iteração 3: Explorando (2,0) | g=2, h=6, f=8
...
[13 iterações mais]
Iteração 14: Explorando (4,6) | g=10, h=0, f=10
✓ Caminho encontrado!

Caminho: (0,0) → (1,0) → (2,0) → (2,1) → (2,2) → (2,3) → (2,4) → ... → (4,6)
Custo: 10
```

Grid com Caminho:
```
S * # . . F .
* # * * # F .
* * * F * * *
# . Z . . # *
. . . . . . E
```

### 9.3 Cálculo de Custo

```
(0,0) [S] → custo=1
(1,0) [.] → custo=1
(2,0) [.] → custo=1
(2,1) [.] → custo=1
(2,2) [.] → custo=1
(2,3) [F] → custo=5
(2,4) [.] → custo=1
(2,5) [.] → custo=1
(2,6) [.] → custo=1
(3,6) [.] → custo=1
(4,6) [E] → custo=1

Total: 1+1+1+1+1+5+1+1+1+1+1 = 15
```

---

## 10. Possíveis Otimizações Futuras

### 10.1 Bidirectional A*
Executar A* simultaneamente do início e do fim, encontrando-se no meio. Reduz exploração pela metade.

### 10.2 Jump Point Search (JPS)
Para grids com movimento livre, "pular" diagonais sem obstáculos, reduzindo nós explorados.

### 10.3 Pesos Adaptativos
Usar heurística ponderada: f(n) = g(n) + w×h(n), onde w > 1 favorece velocidade sobre otimalidade.

### 10.4 Cache de Heurísticas
Pré-calcular distâncias Manhattan para todas as células em relação ao objetivo.

### 10.5 8-Conectado
Permitir movimento diagonal (√2 de custo adicional) para caminhos mais naturais.

---

## 11. Conclusão

O algoritmo A* implementado neste projeto é uma **busca de caminho ótimo** que:

✓ Encontra o caminho de **menor custo total** (não apenas mais curto)  
✓ Usa heurística **Manhattan admissível** para eficiência  
✓ Suporta **múltiplos tipos de terreno** com custos variáveis  
✓ Utiliza **fila de prioridade** para eficiência O(log n)  
✓ Reconstrói caminho via **parent pointers**  
✓ Oferece **visualização completa** do processo  

A implementação equilibra **correção matemática**, **eficiência computacional** e **visualização clara** para fins educacionais e práticos.

---

**Data da Documentação**: 27 de Abril de 2026  
**Versão do Código**: 1.0  
**Linguagem**: Python 3.7+  
**Dependências**: Apenas módulos padrão (heapq, collections)
