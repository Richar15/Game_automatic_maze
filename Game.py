import pygame
import sys
import random
from queue import Queue

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 40
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Laberinto Autómata - Múltiples Caminos")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (10, 15, 255)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (173, 216, 230)
BUTTON_COLOR = (50, 150, 50)
BUTTON_HOVER_COLOR = (100, 200, 100)

class State:
    def __init__(self, position, path):
        self.position = position
        self.path = path

class MazeAutomata:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.rows, self.cols = len(grid), len(grid[0])
        self.start = start
        self.goal = goal
        self.states = self.create_states()
        self.transitions = self.define_transitions()

    def create_states(self):
        states = {}
        for y in range(self.rows):
            for x in range(self.cols):
                if self.grid[y][x] == 0:
                    states[(x, y)] = State((x, y), [])
        return states

    def define_transitions(self):
        transitions = {}
        for state in self.states.values():
            x, y = state.position
            possible_moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            for new_x, new_y in possible_moves:
                if 0 <= new_x < self.cols and 0 <= new_y < self.rows and self.grid[new_y][new_x] == 0:
                    new_state = self.states.get((new_x, new_y))
                    if new_state:
                        if state not in transitions:
                            transitions[state] = []
                        transitions[state].append(new_state)
        return transitions

    def find_shortest_path(self):
        queue = Queue()
        queue.put(self.states[self.start])
        visited = set()

        while not queue.empty():
            current = queue.get()
            if current.position == self.goal:
                return current.path

            if current in visited:
                continue
            visited.add(current)

            for next_state in self.transitions.get(current, []):
                new_path = current.path + [next_state.position]
                next_state.path = new_path
                queue.put(next_state)

        return []  # Si no se encuentra un camino

class Laberinto:
    def __init__(self):
        self.grid = [[1 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.start = (1, 1)
        self.goal = (GRID_WIDTH - 2, GRID_HEIGHT - 2)
        self.player = list(self.start)
        self.generate_maze()
        self.maze_automata = MazeAutomata(self.grid, self.start, self.goal)
        self.shortest_path = self.maze_automata.find_shortest_path()

    def generate_maze(self):
        stack = [self.start]
        self.grid[self.start[1]][self.start[0]] = 0

        while stack:
            current = stack[-1]
            neighbors = self.get_unvisited_neighbors(current)

            if neighbors:
                next_cell = random.choice(neighbors)
                self.connect_cells(current, next_cell)
                stack.append(next_cell)
            else:
                stack.pop()

        self.grid[self.goal[1]][self.goal[0]] = 0

        # Agregar pasajes adicionales
        for _ in range(GRID_WIDTH * GRID_HEIGHT // 10):
            x, y = random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2)
            self.grid[y][x] = 0

    def get_unvisited_neighbors(self, cell):
        x, y = cell
        neighbors = []
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and self.grid[ny][nx] == 1:
                neighbors.append((nx, ny))
        return neighbors

    def connect_cells(self, cell1, cell2):
        x1, y1 = cell1
        x2, y2 = cell2
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
        self.grid[y2][x2] = 0
        self.grid[my][mx] = 0

    def move_player(self):
        if self.shortest_path:
            self.player = list(self.shortest_path.pop(0))

    def is_goal_reached(self):
        return tuple(self.player) == self.goal

def draw_maze(laberinto):
    screen.fill(WHITE)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = BLACK if laberinto.grid[y][x] == 1 else WHITE
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    """ # Dibujar el camino más corto
    for x, y in laberinto.shortest_path:
        pygame.draw.rect(screen, YELLOW, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)) """

    # Dibujar jugador
    pygame.draw.circle(screen, RED, (laberinto.player[0] * CELL_SIZE + CELL_SIZE // 2,
                                     laberinto.player[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

    # Dibujar meta
    pygame.draw.rect(screen, GREEN, (laberinto.goal[0] * CELL_SIZE, laberinto.goal[1] * CELL_SIZE,
                                     CELL_SIZE, CELL_SIZE))

def draw_button(text, x, y, w, h, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))
    
    small_font = pygame.font.Font(None, 50)
    text_surf = small_font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=((x + (w // 2)), (y + (h // 2))))
    screen.blit(text_surf, text_rect)

def restart_game():
    main()

def main():
    laberinto = Laberinto()
    clock = pygame.time.Clock()
    paused = False  # Estado de pausa
    game_over = False  # Estado del juego
    move_delay = 80  # Aumenta este valor para ralentizar el movimiento de la bola
    move_counter = 0  # Contador de fotogramas

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Alternar pausa con la tecla P
                    paused = not paused

        if not paused and not game_over:
            move_counter += 1
            if move_counter >= move_delay:
                laberinto.move_player()
                move_counter = 0

        draw_maze(laberinto)

        if paused:
            font = pygame.font.Font(None, 74)
            text = font.render("Pausado", True, BLUE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        pygame.display.flip()

        if laberinto.is_goal_reached() and not paused:
            game_over = True
            while game_over:
                font = pygame.font.Font(None, 74)
                text = font.render("¡Camino más corto encontrado!", True, BLUE)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
                draw_button("Nueva Partida", WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 75, BUTTON_COLOR, BUTTON_HOVER_COLOR, restart_game)
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                clock.tick(15)

if __name__ == "__main__":
    main()

