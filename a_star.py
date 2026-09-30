"""
Implementação do algoritmo A* para encontrar o caminho de menor custo em um grid 2D
com suporte a diferentes tipos de células com custos variáveis.
Com visualização em cores e animação em tempo real.
"""

import heapq
import time
import random
import os
import sys
from typing import List, Tuple, Set, Optional


# Cores ANSI para terminal
class Colors:
    """Definição de cores e estilos ANSI para terminal."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Cores de Fundo
    BG_START = '\033[42m'      # Verde para início
    BG_END = '\033[44m'         # Azul para fim
    BG_FREE = '\033[47m'        # Branco para livre
    BG_FIRE = '\033[101m'       # Vermelho claro para fogo
    BG_ENEMY = '\033[40m'       # Preto para inimigo
    BG_WALL = '\033[90m'        # Cinza escuro para parede
    BG_PATH = '\033[43m'        # Amarelo para caminho
    BG_EXPLORING = '\033[46m'   # Ciano para explorando
    BG_CLOSED = '\033[100m'     # Cinza escuro para explorado
    
    # Cores de Texto
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    @staticmethod
    def clear_screen():
        """Limpa a tela do terminal."""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    @staticmethod
    def hide_cursor():
        """Esconde o cursor do terminal."""
        print('\033[?25l', end='', flush=True)
    
    @staticmethod
    def show_cursor():
        """Mostra o cursor do terminal."""
        print('\033[?25h', end='', flush=True)


class Node:
    """
    Representa um nó no grid para o algoritmo A*.
    """
    def __init__(self, pos: Tuple[int, int], g: float = 0, h: float = 0):
        """
        Args:
            pos: Tupla (linha, coluna) da posição no grid
            g: Custo do caminho do início até este nó
            h: Heurística (estimativa do custo até o objetivo)
        """
        self.pos = pos
        self.g = g  # Custo real do caminho
        self.h = h  # Heurística estimada
        self.f = g + h  # f(n) = g(n) + h(n), usado para ordenar na fila de prioridade
        self.parent = None

    def __lt__(self, other):
        """Comparação para heap - nós com menor f(n) têm maior prioridade."""
        return self.f < other.f

    def __eq__(self, other):
        return self.pos == other.pos

    def __hash__(self):
        return hash(self.pos)


class AStarPathfinder:
    """
    Implementa o algoritmo A* para busca de caminho em um grid 2D com custos variáveis.
    """
    
    # Definição dos custos para cada tipo de célula
    CELL_COSTS = {
        'S': 1,      # Início - custo normal
        'E': 1,      # Fim - custo normal
        '.': 1,      # Caminho livre - custo normal
        'F': 5,      # Fogo - custo alto (evitar mas possível)
        'Z': float('inf'),  # Inimigo - bloqueado, intransponível
    }
    
    def __init__(self, grid: List[List[str]], verbose: bool = False):
        """
        Args:
            grid: Lista de listas representando o mapa
            verbose: Se True, mostra o processo de busca passo a passo
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0
        self.verbose = verbose
        self.start = None
        self.end = None
        self.steps = []  # Armazena os passos da busca para visualização
        
        self._find_start_and_end()
    
    def _find_start_and_end(self):
        """Localiza as posições de início (S) e fim (E) no grid."""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == 'S':
                    self.start = (i, j)
                elif self.grid[i][j] == 'E':
                    self.end = (i, j)
    
    def manhattan_heuristic(self, pos: Tuple[int, int]) -> float:
        """
        Calcula a heurística de distância de Manhattan.
        
        A distância de Manhattan é |x1-x2| + |y1-y2|.
        Ela nunca superestima o custo real (é admissível),
        garantindo que A* encontre o caminho ótimo.
        
        Args:
            pos: Posição atual (linha, coluna)
            
        Returns:
            Distância de Manhattan até o objetivo
        """
        if self.end is None:
            return 0
        return abs(pos[0] - self.end[0]) + abs(pos[1] - self.end[1])
    
    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[Tuple[int, int], float]]:
        """
        Retorna os vizinhos válidos de uma posição.
        
        Vizinhos são as 4 células adjacentes (cima, baixo, esquerda, direita).
        Uma célula é válida se está dentro dos limites e não é uma parede ('Z').
        
        Args:
            pos: Posição atual (linha, coluna)
            
        Returns:
            Lista de tuplas (nova_posição, custo_movimento)
        """
        row, col = pos
        neighbors = []
        
        # 4 direções: cima, baixo, esquerda, direita
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Verifica se está dentro dos limites do grid
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                cell = self.grid[new_row][new_col]
                cost = self.CELL_COSTS.get(cell, float('inf'))
                
                # Válido se não é bloqueado (Z)
                if cost != float('inf'):
                    neighbors.append(((new_row, new_col), cost))
        
        return neighbors
    
    def find_path(self, animate: bool = False, speed: float = 0.1) -> Optional[List[Tuple[int, int]]]:
        """
        Executa o algoritmo A* para encontrar o caminho de menor custo.
        
        Args:
            animate: Se True, mostra animação em tempo real
            speed: Delay em segundos entre iterações (para animação)
        
        Returns:
            Lista de posições representando o caminho, ou None se não houver
        """
        if self.start is None or self.end is None:
            print("Erro: início ou fim não encontrado no grid!")
            return None
        
        # Fila aberta: nós a explorar (heap de prioridade)
        open_list = []
        
        # Nó inicial
        start_node = Node(self.start, g=0, h=self.manhattan_heuristic(self.start))
        heapq.heappush(open_list, start_node)
        
        # Conjunto de nós já explorados
        closed_set = set()
        
        # Dicionário para rastrear o melhor g(n) encontrado para cada posição
        g_values = {self.start: 0}
        
        # Para visualização
        exploring_now = set()
        
        iteration = 0
        
        if animate:
            Colors.hide_cursor()
        
        while open_list:
            iteration += 1
            
            # Extrai nó com menor f(n)
            current_node = heapq.heappop(open_list)
            current_pos = current_node.pos
            exploring_now.add(current_pos)
            
            if self.verbose:
                print(f"Iteração {iteration}: Explorando {current_pos} | "
                      f"g={current_node.g:.0f}, h={current_node.h:.0f}, f={current_node.f:.0f}")
                self.steps.append(current_pos)
            
            # Animação em tempo real
            if animate:
                self._animate_step(current_pos, closed_set, exploring_now, iteration, current_node.g, current_node.h)
                time.sleep(speed)
            
            # Se chegou ao objetivo
            if current_pos == self.end:
                if animate:
                    Colors.show_cursor()
                print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Caminho encontrado em {iteration} iterações!{Colors.RESET}")
                return self._reconstruct_path(current_node)
            
            # Marca como explorado
            closed_set.add(current_pos)
            exploring_now.discard(current_pos)
            
            # Expande vizinhos
            for neighbor_pos, move_cost in self.get_neighbors(current_pos):
                # Pula se já foi explorado
                if neighbor_pos in closed_set:
                    continue
                
                # Calcula novo g(n)
                tentative_g = current_node.g + move_cost
                
                # Se encontrou um caminho melhor para este vizinho
                if neighbor_pos not in g_values or tentative_g < g_values[neighbor_pos]:
                    g_values[neighbor_pos] = tentative_g
                    
                    # Cria nó vizinho com custos atualizados
                    h = self.manhattan_heuristic(neighbor_pos)
                    neighbor_node = Node(neighbor_pos, g=tentative_g, h=h)
                    neighbor_node.parent = current_node
                    
                    heapq.heappush(open_list, neighbor_node)
        
        if animate:
            Colors.show_cursor()
        print(f"\n{Colors.RED}{Colors.BOLD}✗ Nenhum caminho encontrado após {iteration} iterações!{Colors.RESET}")
        return None
    
    def _animate_step(self, current_pos: Tuple[int, int], closed_set: Set[Tuple[int, int]], 
                      exploring: Set[Tuple[int, int]], iteration: int, g: float, h: float):
        """
        Mostra animação de uma iteração do A*.
        """
        Colors.clear_screen()
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}")
        print(f"BUSCA A* EM PROGRESSO - Iteração {iteration}")
        print(f"{'='*70}{Colors.RESET}\n")
        
        self._print_colored_grid(self.grid, exploring, closed_set)
        
        print(f"\n{Colors.BOLD}Status da Busca:{Colors.RESET}")
        print(f"  {Colors.BG_EXPLORING}{Colors.BLACK}◆{Colors.RESET} Explorando agora: {len(exploring)} nó(s)")
        print(f"  {Colors.BG_CLOSED}{Colors.BLACK}●{Colors.RESET} Já explorados: {len(closed_set)} nó(s)")
        print(f"  Posição atual: {Colors.BOLD}{current_pos}{Colors.RESET}")
        print(f"  Custo acumulado (g): {Colors.YELLOW}{g:.0f}{Colors.RESET}")
        print(f"  Heurística (h): {Colors.YELLOW}{h:.0f}{Colors.RESET}")
        print(f"  Avaliação (f=g+h): {Colors.YELLOW}{g+h:.0f}{Colors.RESET}")
        
        # Calcula progressão em direção ao objetivo
        if self.end:
            dist = abs(current_pos[0] - self.end[0]) + abs(current_pos[1] - self.end[1])
            print(f"  Distância até fim (Manhattan): {Colors.YELLOW}{dist}{Colors.RESET}")
    
    def _reconstruct_path(self, node: Node) -> List[Tuple[int, int]]:
        """
        Reconstrói o caminho seguindo os ponteiros parent até o início.
        """
        path = []
        current = node
        
        while current is not None:
            path.append(current.pos)
            current = current.parent
        
        path.reverse()
        return path
    
    def print_grid(self):
        """Imprime o grid original com cores."""
        print("\n" + "="*70)
        print(f"{Colors.BOLD}GRID ORIGINAL:{Colors.RESET}")
        print("="*70)
        self._print_colored_grid(self.grid)
    
    def _print_colored_grid(self, grid: List[List[str]], 
                           exploring: Set[Tuple[int, int]] = None,
                           closed_set: Set[Tuple[int, int]] = None):
        """
        Imprime um grid com cores baseado no tipo de célula.
        """
        if exploring is None:
            exploring = set()
        if closed_set is None:
            closed_set = set()
        
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                pos = (i, j)
                
                # Determina cor baseado no tipo de célula e estado
                if pos in exploring:
                    bg_color = Colors.BG_EXPLORING
                    symbol = '◆'
                elif pos in closed_set:
                    bg_color = Colors.BG_CLOSED
                    symbol = '●'
                else:
                    if cell == 'S':
                        bg_color = Colors.BG_START
                        symbol = 'S'
                    elif cell == 'E':
                        bg_color = Colors.BG_END
                        symbol = 'E'
                    elif cell == '.':
                        bg_color = Colors.BG_FREE
                        symbol = '·'
                    elif cell == '#':
                        bg_color = Colors.BG_WALL
                        symbol = '█'
                    elif cell == 'F':
                        bg_color = Colors.BG_FIRE
                        symbol = 'F'
                    elif cell == 'Z':
                        bg_color = Colors.BG_ENEMY
                        symbol = 'Z'
                    else:
                        bg_color = Colors.BG_FREE
                        symbol = '?'
                
                print(f"{bg_color}{Colors.BLACK}{symbol}{Colors.RESET}", end=' ')
            print()
    
    def print_grid_with_path(self, path: List[Tuple[int, int]]):
        """
        Imprime o grid com o caminho marcado com cores vibrantes.
        """
        result = [row[:] for row in self.grid]
        
        print("\n" + "="*70)
        print(f"{Colors.BOLD}GRID FINAL COM CAMINHO:{Colors.RESET}")
        print("="*70)
        
        # Marca o caminho
        for i, pos in enumerate(path):
            row, col = pos
            if result[row][col] not in ['S', 'E']:
                result[row][col] = '*'
        
        # Imprime com cores
        for i, row in enumerate(result):
            for j, cell in enumerate(row):
                pos = (i, j)
                
                if cell == 'S':
                    bg_color = Colors.BG_START
                    symbol = 'S'
                    text_color = Colors.BLACK
                elif cell == 'E':
                    bg_color = Colors.BG_END
                    symbol = 'E'
                    text_color = Colors.WHITE
                elif cell == '*':
                    bg_color = Colors.BG_PATH
                    symbol = '★'
                    text_color = Colors.BLACK
                elif cell == '.':
                    bg_color = Colors.BG_FREE
                    symbol = '·'
                    text_color = Colors.BLACK
                elif cell == '#':
                    bg_color = Colors.BG_WALL
                    symbol = '█'
                    text_color = Colors.BLACK
                elif cell == 'F':
                    bg_color = Colors.BG_FIRE
                    symbol = 'F'
                    text_color = Colors.BLACK
                elif cell == 'Z':
                    bg_color = Colors.BG_ENEMY
                    symbol = 'Z'
                    text_color = Colors.WHITE
                else:
                    bg_color = Colors.BG_FREE
                    symbol = '?'
                    text_color = Colors.BLACK
                
                print(f"{bg_color}{text_color}{symbol}{Colors.RESET}", end=' ')
            print()
        
        # Legenda colorida
        print(f"\n{Colors.BOLD}LEGENDA:{Colors.RESET}")
        print(f"{Colors.BG_START}{Colors.BLACK}S{Colors.RESET} = Início    ", end="")
        print(f"{Colors.BG_END}{Colors.WHITE}E{Colors.RESET} = Fim    ", end="")
        print(f"{Colors.BG_PATH}{Colors.BLACK}★{Colors.RESET} = Caminho    ", end="")
        print(f"{Colors.BG_FREE}{Colors.BLACK}·{Colors.RESET} = Livre")
        
        print(f"{Colors.BG_FIRE}{Colors.BLACK}F{Colors.RESET} = Fogo    ", end="")
        print(f"{Colors.BG_ENEMY}{Colors.WHITE}Z{Colors.RESET} = Inimigo    ", end="")
        print(f"{Colors.BG_WALL}{Colors.BLACK}█{Colors.RESET} = Parede    ", end="")
        print(f"{Colors.BG_EXPLORING}{Colors.BLACK}◆{Colors.RESET} = Explorando")


def create_example_grid() -> List[List[str]]:
    """Cria um grid de exemplo com vários tipos de terreno."""
    return [
        ['S', '.', '#', '.', '.', 'F', '.'],
        ['.', '#', '.', '.', '#', 'F', '.'],
        ['.', '.', '.', 'F', '.', '.', '.'],
        ['#', '.', 'Z', '.', '.', '#', '.'],
        ['.', '.', '.', '.', '.', '.', 'E'],
    ]


def create_complex_grid() -> List[List[str]]:
    """Cria um grid mais complexo com múltiplos obstáculos."""
    return [
        ['S', '.', '.', '#', '.', '.', '.', '.', '.', '.'],
        ['.', '#', '.', '#', '.', '#', '#', '#', 'F', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', 'F', '.'],
        ['#', '.', 'Z', '.', '#', 'F', 'F', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '#', '.'],
        ['.', '#', '#', '.', '.', 'F', '.', '.', '#', '.'],
        ['.', '.', '.', '.', 'Z', '.', '.', '.', '.', 'E'],
    ]


def create_random_grid(rows: int = 10, cols: int = 15, 
                       obstacle_chance: float = 0.15,
                       fire_chance: float = 0.08,
                       enemy_chance: float = 0.05) -> List[List[str]]:
    """
    Gera um grid totalmente aleatório com distribuição controlada.
    """
    grid = [['.' for _ in range(cols)] for _ in range(rows)]
    
    # Define posições aleatórias para início e fim
    start_row, start_col = random.randint(0, rows - 1), random.randint(0, cols - 1)
    grid[start_row][start_col] = 'S'
    
    # Fim deve estar longe do início
    while True:
        end_row, end_col = random.randint(0, rows - 1), random.randint(0, cols - 1)
        if (end_row, end_col) != (start_row, start_col):
            grid[end_row][end_col] = 'E'
            break
    
    # Preenche com obstáculos, fogo e inimigos
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] not in ['S', 'E']:
                rand = random.random()
                
                if rand < enemy_chance:
                    grid[i][j] = 'Z'
                elif rand < enemy_chance + fire_chance:
                    grid[i][j] = 'F'
                elif rand < enemy_chance + fire_chance + obstacle_chance:
                    grid[i][j] = '#'
    
    return grid


def create_maze_like_grid(rows: int = 12, cols: int = 20) -> List[List[str]]:
    """Gera um grid em estilo labirinto com corredores e obstáculos."""
    grid = [['#' for _ in range(cols)] for _ in range(rows)]
    
    # Cria corredores usando um padrão simples
    for i in range(rows):
        for j in range(cols):
            if i % 2 == 0 or j % 2 == 0:
                grid[i][j] = '.'
    
    # Adiciona alguns inimigos e fogo aleatoriamente nos corredores
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '.':
                rand = random.random()
                if rand < 0.05:
                    grid[i][j] = 'Z'
                elif rand < 0.12:
                    grid[i][j] = 'F'
    
    # Define início e fim
    start_row, start_col = 1, 1
    end_row, end_col = rows - 2, cols - 2
    
    grid[start_row][start_col] = 'S'
    grid[end_row][end_col] = 'E'
    
    return grid


def create_sparse_grid(rows: int = 15, cols: int = 15) -> List[List[str]]:
    """Gera um grid com poucos obstáculos (terreno aberto)."""
    return create_random_grid(rows, cols, obstacle_chance=0.05, 
                             fire_chance=0.03, enemy_chance=0.02)


def create_dense_grid(rows: int = 10, cols: int = 10) -> List[List[str]]:
    """Gera um grid denso com muitos obstáculos (desafio difícil)."""
    return create_random_grid(rows, cols, obstacle_chance=0.25, 
                             fire_chance=0.12, enemy_chance=0.08)


def main():
    """Função principal para testar o algoritmo A*."""
    
    Colors.clear_screen()
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'█'*70}")
    print(f"█{' '*68}█")
    print(f"█{'  ALGORITMO A* - BUSCA DE CAMINHO ÓTIMO'.center(68)}█")
    print(f"█{' '*68}█")
    print(f"{'█'*70}{Colors.RESET}\n")
    
    # Menu de seleção
    print(f"{Colors.BOLD}Escolha um tipo de grid:{Colors.RESET}\n")
    print("  1. Grid Simples")
    print("  2. Grid Complexo")
    print("  3. Grid Aleatório")
    print("  4. Grid em Labirinto")
    print("  5. Grid Esparso (Aberto)")
    print("  6. Grid Denso (Difícil)")
    
    choice = input(f"\n{Colors.YELLOW}Digite 1-6 (padrão: 1):{Colors.RESET} ").strip() or "1"
    
    print(f"\n{Colors.CYAN}Gerando grid...{Colors.RESET}")
    
    if choice == "2":
        grid = create_complex_grid()
        print("✓ Grid Complexo carregado")
    elif choice == "3":
        grid = create_random_grid(12, 18)
        print("✓ Grid Aleatório gerado")
    elif choice == "4":
        grid = create_maze_like_grid(12, 20)
        print("✓ Grid em Labirinto gerado")
    elif choice == "5":
        grid = create_sparse_grid(15, 15)
        print("✓ Grid Esparso gerado")
    elif choice == "6":
        grid = create_dense_grid(10, 10)
        print("✓ Grid Denso gerado")
    else:
        grid = create_example_grid()
        print("✓ Grid Simples carregado")
    
    # Opções de visualização
    print(f"\n{Colors.BOLD}Opções de Visualização:{Colors.RESET}\n")
    print("  1. Modo Silencioso (rápido)")
    print("  2. Modo Verbose (mostra iterações no terminal)")
    print("  3. Modo Animado (animação em tempo real)")
    
    vis_choice = input(f"\n{Colors.YELLOW}Digite 1-3 (padrão: 3):{Colors.RESET} ").strip() or "3"
    
    verbose = vis_choice in ["2"]
    animate = vis_choice in ["3"]
    
    # Define velocidade da animação
    speed = 0.05
    if animate:
        speed_input = input(f"\n{Colors.YELLOW}Velocidade da animação (0.01-1.0, padrão: 0.05):{Colors.RESET} ").strip()
        try:
            speed = float(speed_input) if speed_input else 0.05
            speed = max(0.01, min(1.0, speed))
        except ValueError:
            speed = 0.05
    
    # Cria o pathfinder e executa o algoritmo
    pathfinder = AStarPathfinder(grid, verbose=verbose)
    
    # Mostra grid original
    pathfinder.print_grid()
    
    if not animate:
        input(f"\n{Colors.YELLOW}Pressione ENTER para iniciar a busca...{Colors.RESET}")
    else:
        print(f"\n{Colors.YELLOW}Iniciando busca animada em 2 segundos...{Colors.RESET}")
        time.sleep(2)
    
    # Executa A*
    if not animate:
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}")
        print(f"EXECUTANDO A*...")
        print(f"{'='*70}{Colors.RESET}")
    
    path = pathfinder.find_path(animate=animate, speed=speed)
    
    # Mostra resultado
    if path:
        print(f"\n{Colors.GREEN}{Colors.BOLD}{'='*70}")
        print(f"RESULTADO DA BUSCA")
        print(f"{'='*70}{Colors.RESET}\n")
        
        print(f"{Colors.BOLD}Caminho encontrado com {len(path)} passos:{Colors.RESET}")
        
        # Mostra caminho em formato legível
        path_str = " → ".join([f"({pos[0]},{pos[1]})" for pos in path])
        if len(path_str) > 80:
            parts = path_str.split(" → ")
            for i in range(0, len(parts), 4):
                print("  " + " → ".join(parts[i:i+4]))
        else:
            print(f"  {path_str}")
        
        # Calcula custo total
        total_cost = 0
        cost_breakdown = []
        for i in range(len(path)):
            current = path[i]
            cell = grid[current[0]][current[1]]
            cost = AStarPathfinder.CELL_COSTS.get(cell, 1)
            total_cost += cost
            cost_breakdown.append((cell, cost))
        
        print(f"\n{Colors.BOLD}Análise de Custo:{Colors.RESET}")
        print(f"  {Colors.YELLOW}Custo total do caminho: {total_cost}{Colors.RESET}")
        print(f"  Número de passos: {len(path)}")
        print(f"  Custo médio por passo: {total_cost / len(path):.2f}")
        
        # Mostra breakdown de custos
        print(f"\n{Colors.BOLD}Breakdown de Células:{Colors.RESET}")
        cell_stats = {}
        for cell, cost in cost_breakdown:
            if cell not in cell_stats:
                cell_stats[cell] = {'count': 0, 'total_cost': 0}
            cell_stats[cell]['count'] += 1
            cell_stats[cell]['total_cost'] += cost
        
        for cell in ['S', 'E', '.', 'F']:
            if cell in cell_stats:
                stats = cell_stats[cell]
                symbol = '●' if cell == '.' else cell
                print(f"  {symbol} ({cell}): {stats['count']}x = {stats['total_cost']} custo total")
        
        # Mostra grid com caminho
        pathfinder.print_grid_with_path(path)
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}{'='*70}")
        print(f"NENHUM CAMINHO FOI ENCONTRADO!")
        print(f"{'='*70}{Colors.RESET}\n")
        print("O objetivo é inalcançável. Verifique se há inimigos (Z) bloqueando o caminho.")
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'█'*70}{Colors.RESET}\n")


if __name__ == "__main__":
    main()
