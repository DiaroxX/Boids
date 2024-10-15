import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from flock import Flock

WIDTH = 800
HEIGHT = 600
WINDOW_NAME = "Boids!"
BACKGRND_COLOR = (20, 20, 20)
DETECTION_RADIUS = 100 #a mettre en arguments


def run(num_boids):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_NAME)

    flock = Flock(num_boids, WIDTH, HEIGHT)

    run = True
    clock = pygame.time.Clock()
    framerate = 60

    # a pygame program follows this loop
    # while run : 
    #   check for game loop end
    #   tick for all objects
    #   draw all objects
    #   pygame update display

    while run:
        dt = clock.tick_busy_loop(framerate)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        screen.fill(BACKGRND_COLOR)
        flock.update(dt, detection_radius=DETECTION_RADIUS)
        flock.draw(screen)
        pygame.display.update()

    pygame.quit()
    exit()


def error_and_exit(message):
    print(f"Erreur: {message}", file=sys.stderr)
    print(
        f"\nUsage: {sys.argv[0]} num_boids\n"
        "\n"
        " num_boids: nombre de boids\n"
        "\n"
        f"exemple: {sys.argv[0]} 100\n"
        , file=sys.stderr
    )
    sys.exit(1)


def to_float(str):
    try:
        res = float(str)
    except ValueError:
        res = None
    return res


def read_argv():
    if len(sys.argv) < 2:
        error_and_exit("Nombre d'arguments incorrect")
    num_boids = int(sys.argv[1])
    return num_boids

if __name__ == "__main__":
    num_boids = read_argv()
    run(num_boids)
