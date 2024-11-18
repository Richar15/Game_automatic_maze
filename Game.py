import pygame  # Importar la biblioteca pygame para crear juegos
import sys  # Importar la biblioteca sys para manejar la salida del programa
import random  # Importar la biblioteca random para generar números aleatorios
from queue import Queue  # Importar la clase Queue de la biblioteca queue para manejar colas

# Inicializar Pygame
pygame.init()

# Inicializar pygame mixer
pygame.mixer.init()


#Rutas de Sonidos

# sonido/acabadocrtica.mp3
# sonido/amarilloplatano.mp3
# sonido/bueecobra.mp3
# sonido/sonidoRamdom.mp3
# sonido/broly.mp3
# sonido/vini v.mp3

# Cargar el sonido
pygame.mixer.music.load('sonido/sonidoRamdom.mp3')  # Cargar un archivo de sonido para reproducir en el juego

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600  # Definir el ancho y alto de la pantalla
CELL_SIZE = 40  # Definir el tamaño de cada celda del laberinto
GRID_WIDTH = WIDTH // CELL_SIZE  # Calcular el número de celdas en el ancho de la pantalla
GRID_HEIGHT = HEIGHT // CELL_SIZE  # Calcular el número de celdas en el alto de la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Crear la ventana del juego con las dimensiones especificadas
pygame.display.set_caption("Laberinto Autómata")  # Establecer el título de la ventana del juego

# Colores
WHITE = (255, 255, 255)  # Definir el color blanco
BLACK = (0, 0, 0)  # Definir el color negro
RED = (255, 0, 0)  # Definir el color rojo
GREEN = (0, 255, 0)  # Definir el color verde
BLUE = (10, 15, 255)  # Definir el color azul
YELLOW = (255, 255, 0)  # Definir el color amarillo
LIGHT_BLUE = (173, 216, 230)  # Definir el color azul claro
BUTTON_COLOR = (50, 150, 50)  # Definir el color del botón
BUTTON_HOVER_COLOR = (100, 200, 100)  # Definir el color del botón cuando el mouse está sobre él

class State:
    def __init__(self, position, path):
        self.position = position  # Posición del estado en el laberinto
        self.path = path  # Camino recorrido hasta este estado

class MazeAutomata:
    def __init__(self, grid, start, goal):
        self.grid = grid  # Matriz que representa el laberinto
        self.rows, self.cols = len(grid), len(grid[0])  # Número de filas y columnas del laberinto
        self.start = start  # Posición inicial en el laberinto
        self.goal = goal  # Posición objetivo en el laberinto
        self.states = self.create_states()  # Crear los estados del autómata
        self.transitions = self.define_transitions()  # Definir las transiciones entre estados

    def create_states(self):
        states = {}
        for y in range(self.rows):
            for x in range(self.cols):
                if self.grid[y][x] == 0:  # Si la celda es transitable
                    states[(x, y)] = State((x, y), [])  # Crear un estado para la celda
        return states

    def define_transitions(self):
        transitions = {}
        for state in self.states.values():
            x, y = state.position
            possible_moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]  # Movimientos posibles (derecha, izquierda, abajo, arriba)
            for new_x, new_y in possible_moves:
                if 0 <= new_x < self.cols and 0 <= new_y < self.rows and self.grid[new_y][new_x] == 0:  # Si el movimiento es válido
                    new_state = self.states.get((new_x, new_y))
                    if new_state:
                        if state not in transitions:
                            transitions[state] = []
                        transitions[state].append(new_state)  # Agregar la transición al nuevo estado
        return transitions

    def find_shortest_path(self):
        queue = Queue()
        queue.put(self.states[self.start])  # Agregar el estado inicial a la cola
        visited = set()  # Conjunto de estados visitados

        while not queue.empty():
            current = queue.get()
            if current.position == self.goal:  # Si se alcanza el objetivo
                return current.path  # Devolver el camino recorrido

            if current in visited:
                continue
            visited.add(current)

            for next_state in self.transitions.get(current, []):
                new_path = current.path + [next_state.position]
                next_state.path = new_path
                queue.put(next_state)  # Agregar el siguiente estado a la cola

        return []  # Si no se encuentra un camino

class Laberinto:
    def __init__(self):
        self.grid = [[1 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]  # Crear una matriz llena de paredes
        self.start = (1, 1)  # Posición inicial del jugador
        self.goal = (GRID_WIDTH - 2, GRID_HEIGHT - 2)  # Posición objetivo
        self.player = list(self.start)  # Posición actual del jugador
        self.generate_maze()  # Generar el laberinto
        self.maze_automata = MazeAutomata(self.grid, self.start, self.goal)  # Crear el autómata del laberinto
        self.shortest_path = self.maze_automata.find_shortest_path()  # Encontrar el camino más corto

    def generate_maze(self):
        stack = [self.start]
        self.grid[self.start[1]][self.start[0]] = 0  # Hacer transitable la celda inicial

        while stack:
            current = stack[-1]
            neighbors = self.get_unvisited_neighbors(current)

            if neighbors:
                next_cell = random.choice(neighbors)
                self.connect_cells(current, next_cell)
                stack.append(next_cell)
            else:
                stack.pop()

        self.grid[self.goal[1]][self.goal[0]] = 0  # Hacer transitable la celda objetivo

        # Agregar pasajes adicionales
        for _ in range(GRID_WIDTH * GRID_HEIGHT // 10):
            x, y = random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2)
            self.grid[y][x] = 0  # Hacer transitable una celda aleatoria

    def get_unvisited_neighbors(self, cell):
        x, y = cell
        neighbors = []
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:  # Movimientos posibles (dos celdas a la derecha, izquierda, abajo, arriba)
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and self.grid[ny][nx] == 1:  # Si el vecino no ha sido visitado
                neighbors.append((nx, ny))
        return neighbors

    def connect_cells(self, cell1, cell2):
        x1, y1 = cell1
        x2, y2 = cell2
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2  # Calcular la celda intermedia
        self.grid[y2][x2] = 0  # Hacer transitable la celda destino
        self.grid[my][mx] = 0  # Hacer transitable la celda intermedia

    def move_player(self):
        if self.shortest_path:
            self.player = list(self.shortest_path.pop(0))  # Mover el jugador al siguiente paso del camino más corto

    def is_goal_reached(self):
        return tuple(self.player) == self.goal  # Verificar si el jugador ha alcanzado el objetivo

def draw_maze(laberinto):
    screen.fill(WHITE)  # Rellenar la pantalla con color blanco
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = BLACK if laberinto.grid[y][x] == 1 else WHITE  # Dibujar paredes en negro y celdas transitables en blanco
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Dibujar el camino más corto
    """ for x, y in laberinto.shortest_path:
        pygame.draw.rect(screen, YELLOW, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))  """

    # Dibujar jugador
    pygame.draw.circle(screen, RED, (laberinto.player[0] * CELL_SIZE + CELL_SIZE // 2,
                                     laberinto.player[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

    # Dibujar meta
    pygame.draw.rect(screen, GREEN, (laberinto.goal[0] * CELL_SIZE, laberinto.goal[1] * CELL_SIZE,
                                     CELL_SIZE, CELL_SIZE))

def draw_button(text, x, y, w, h, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()  # Obtener la posición del mouse
    click = pygame.mouse.get_pressed()  # Obtener el estado de los botones del mouse
    
    if x + w > mouse[0] > x and y + h > mouse[1] > y:  # Verificar si el mouse está sobre el botón
        pygame.draw.rect(screen, hover_color, (x, y, w, h))  # Dibujar el botón con el color de hover
        if click[0] == 1 and action is not None:  # Verificar si se ha hecho clic en el botón
            action()  # Ejecutar la acción asociada al botón
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))  # Dibujar el botón con el color normal
    
    small_font = pygame.font.Font(None, 50)  # Crear una fuente para el texto del botón
    text_surf = small_font.render(text, True, WHITE)  # Renderizar el texto del botón
    text_rect = text_surf.get_rect(center=((x + (w // 2)), (y + (h // 2))))  # Calcular la posición del texto en el botón
    screen.blit(text_surf, text_rect)  # Dibujar el texto en el botón

def restart_game():
    pygame.mixer.music.play(-1)  # Reproducir el sonido en bucle al reiniciar el juego
    main()  # Llamar a la función principal para reiniciar el juego

def main():
    laberinto = Laberinto()  # Crear una instancia de la clase Laberinto
    clock = pygame.time.Clock()  # Crear un reloj para controlar la velocidad del juego
    paused = False  # Estado de pausa
    game_over = False  # Estado del juego
    move_delay = 200  # Aumenta este valor para ralentizar el movimiento de la bola
    move_counter = 0  # Contador de fotogramas

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Verificar si se ha cerrado la ventana
                pygame.quit()  # Cerrar Pygame
                sys.exit()  # Salir del programa
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Alternar pausa con la tecla P
                    paused = not paused
                    if paused:
                        pygame.mixer.music.pause()  # Pausar el sonido
                    else:
                        pygame.mixer.music.unpause()  # Reanudar el sonido

        if not paused and not game_over:
            move_counter += 1
            if move_counter >= move_delay:
                laberinto.move_player()  # Mover el jugador
                move_counter = 0

        draw_maze(laberinto)  # Dibujar el laberinto

        if paused:
            font = pygame.font.Font(None, 74)  # Crear una fuente para el texto de pausa
            text = font.render("Pausado", True, BLUE)  # Renderizar el texto de pausa
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))  # Dibujar el texto de pausa

        pygame.display.flip()  # Actualizar la pantalla

        if laberinto.is_goal_reached() and not paused:
            pygame.mixer.music.stop()  # Detener el sonido cuando se alcanza la meta
            game_over = True
            while game_over:
                font = pygame.font.Font(None, 74)  # Crear una fuente para el texto de fin del juego
                text = font.render("¡Camino más corto encontrado!", True, BLUE)  # Renderizar el texto de fin del juego
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))  # Dibujar el texto de fin del juego
                draw_button("Nueva Partida", WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 75, BUTTON_COLOR, BUTTON_HOVER_COLOR, restart_game)  # Dibujar el botón de nueva partida
                pygame.display.flip()  # Actualizar la pantalla

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # Verificar si se ha cerrado la ventana
                        pygame.quit()  # Cerrar Pygame
                        sys.exit()  # Salir del programa

                clock.tick(15)  # Controlar la velocidad del bucle de fin del juego

if __name__ == "__main__":
    pygame.mixer.music.play(-1)  # Reproducir el sonido en bucle al iniciar el juego
    main()  # Llamar a la función principal para iniciar el juego