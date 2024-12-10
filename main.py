import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from flock import Flock

WIDTH = 800
HEIGHT = 600
WINDOW_NAME = "Boids!"
BACKGRND_COLOR = (20, 20, 20)


def run(weigths_forces, args_flock, wind, max_time):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_NAME)

    flock = Flock(WIDTH, HEIGHT, *args_flock, weigths_forces, wind)

    max_time *= 1000 #on convertit le temps en milisecondes
    run_time = 0
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
        run_time += dt
        
        #on ne s'arrete pas si le temps maximum a la valeur par défaut(-1000)
        if run_time >= max_time and max_time != -1000:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

                #appuyer sur espace met la simulation en pause
                if event.key == pygame.K_SPACE:
                    pause = not pause

        if not pause:
            screen.fill(BACKGRND_COLOR)
            flock.update(dt)
            flock.draw(screen)
            pygame.display.update()

    pygame.quit()
    exit()


def error_and_exit(message):
    print(f"Erreur: {message}", file=sys.stderr)
    print(
        f"\nUsage: {sys.argv[0]} detection_radius alignment_weight cohesion_weight avoidance_weight num_boids seed\n"
        "\n"
        " detection_radius: rayon de detection\n"
        " alignment_weight: coefficient pour la force d'alignement\n"
        " cohesion_weight: coefficient pour la force de cohesion\n"
        " avoidance_weight: coefficient pour la force d'evitement\n"
        " num_boids: nombre de boids\n"
        " seed: graine pour generer la position et la vitesse initiales des boids\n"
        "\n"
        f"exemple: {sys.argv[0]} 70 3 0.03 50 100 0\n"
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

    detection_radius = int(sys.argv[1])
    alignment_weight = float(sys.argv[2])
    cohesion_weight = float(sys.argv[3])
    avoidance_weight = float(sys.argv[4])
    num_boids = int(sys.argv[5])
    seed = int(sys.argv[6])

    #tous les arguments suivants on pour valeures par defaut celles du sujet initial, sans les fonctionnalites supplementaires
    isCone = False if nb_args_given <= 7 else sys.argv[7] == "True"
    fov  = 3.14 if nb_args_given <= 8 else float(sys.argv[8])
    isTore = True if nb_args_given <= 9 else sys.argv[9] == "True"
    padding = 50 if nb_args_given <= 10 else int(sys.argv[10])
    bounce_weight = 1 if nb_args_given <= 11 else int(sys.argv[11])
    wind_weight = 0 if nb_args_given <= 12 else float(sys.argv[12])
    wind_orientation = 0 if nb_args_given <= 13 else float(sys.argv[13])
    max_rotation = 3.2 if nb_args_given <= 14 else float(sys.argv[14])
    max_time = -1 if nb_args_given <= 15 else float(sys.argv[15])

    weigths_forces = (alignment_weight, cohesion_weight, avoidance_weight, bounce_weight)
    args_flock = (detection_radius, num_boids, seed, isCone, fov, padding, isTore, max_rotation)
    wind = wind_weight, wind_orientation
    
    return weigths_forces, args_flock, wind, max_time

if __name__ == "__main__":
    args = read_argv()
    run(*args)
