import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from flock import Flock

WIDTH = 800
HEIGHT = 600
WINDOW_NAME = "Boids!"
BACKGRND_COLOR = (20, 20, 20)


def run(args):
    (
        detection_radius,
        num_boids,
        seed,
        cone,
        fov,
        padding,
        tore,
        alignment_weight,
        cohesion_weight,
        avoidance_weight
    ) = args

    args_flock = args[1:7]
    weigths_forces = args[7:]

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_NAME)

    flock = Flock(WIDTH, HEIGHT, *args_flock, weigths_forces)

    run = True
    pause = False
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
                if event.key == pygame.K_SPACE:
                    pause = not pause

        if not pause:
            screen.fill(BACKGRND_COLOR)
            flock.update(dt, detection_radius)
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
    nb_args_given = len(sys.argv)
    if nb_args_given < 7:
        error_and_exit("Nombre d'arguments incorrect")

    args_def = [
        100,    #detection_radius
        20,     #alignment_weight
        0.005,  #cohesion_weight
        1,      #avoidance_weight
        100,    #num_boids
        None,   #seed
        False,  #cone
        3.1415, #fov
        10,     #padding
        True    #tore
    ]

    
    
    return tuple(args_def)

if __name__ == "__main__":
    args = read_argv()
    run(args)
