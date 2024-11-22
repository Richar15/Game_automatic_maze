# Laberinto Autómata - Múltiples Caminos

Este proyecto es un juego de laberinto automático que utiliza Pygame para la visualización y la interacción. El objetivo del juego es encontrar el camino más corto desde el inicio hasta la meta en un laberinto generado automáticamente.

## Requisitos

- Python 3.x
- Pygame

## Instalación

1. Clona este repositorio en tu máquina local:
```sh
    git clone https://github.com/Richar15/Game_automatic_maze.git
    cd tu_repositorio
    ```

2. Instala las dependencias necesarias:
    ```sh
    pip install pygame
    ```

## Ejecución

Para ejecutar el juego, simplemente ejecuta el archivo `game.py`:
```sh
python [game.py](http://_vscodecontentref_/0)

Controles
P: Pausar/Despausar el juego
Cerrar ventana: Salir del juego

## Estructura del Proyecto

Game.py: Contiene la lógica principal del juego y la visualización.

# Descripción de Clases y Funciones

#Clases

State: Representa un estado en el autómata del laberinto.
MazeAutomata: Genera los estados y transiciones del laberinto y encuentra el camino más corto.
Laberinto: Genera el laberinto y maneja la lógica del juego.

#Funciones
draw_maze(laberinto): Dibuja el laberinto en la pantalla.
draw_button(text, x, y, w, h, color, hover_color, action): Dibuja un botón en la pantalla.
restart_game(): Reinicia el juego.
pygame.mixer.init(): Inicializa ele sonido del juego
main(): Función principal que inicia el juego.