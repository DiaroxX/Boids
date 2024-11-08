import random 
from boid import Boid
from vector import Vector, angle_diff
import math

class Flock:
    """
    Initial paper available at https://dl.acm.org/doi/pdf/10.1145/37402.37406
    A bit more details here https://www.red3d.com/cwr/boids/
    A flock of boids holding the general parameters and for loops to run the
    simulation.
    """
    def __init__(self, width, height, detection_radius, num_boids, seed, isCone, fov, padding, isTore, max_rotation, weights_forces, wind):
        random.seed(seed)

        self.max_speed = 0.3 #venant de boid  car commun a tous les boids

        self.detection_radius = detection_radius
        self.num_boids = num_boids
        self.boids = []
        self.width = width
        self.height = height
        self.weights_forces = weights_forces
        self.isCone = isCone
        self.fov = fov
        self.padding = padding
        self.isTore = isTore
        self.max_rotation = max_rotation
        self.wind = wind

        # initialize random boids
        for _ in range(num_boids):

            pos_x = random.randint(0, self.width)
            pos_y = random.randint(0, self.height)
            pos = Vector(pos_x, pos_y)

            vel_x = random.gauss(0, 1)
            vel_y = random.gauss(0, 1)
            vel = Vector(vel_x, vel_y)

            #on borne la vitesse ce qu'in n'etait pas le cas initialement
            vel.cap_magnitude(0.3)

            self.boids.append(Boid(pos, vel))
            

    def get_neighbours(self, boid):
        neighbours = set()
        for other in self.boids:

            d = boid.position.distance(other.position, self.width, self.height, self.isTore)
            if d.magnitude() <= self.detection_radius:

                #on verifie si le "other" est dans le cone de vision
                ang_diff = abs(angle_diff(boid.velocity.angle(), d.angle()))
                if not self.isCone or ang_diff <= self.fov/2:
                    neighbours.add(other)

        #un boid ne doit pas etre voisin de lui meme
        if boid in neighbours:
            neighbours.remove(boid)

        return neighbours

    def update(self, dt):
        *weights_interactions_forces, bounce_weight = self.weights_forces

        neighbours = set()

        for boid in self.boids:
            #on réinitialise la couleur de chaque boid (voir prochains commentaires)
            boid.color = (255, 255, 255)

            neighbours = self.get_neighbours(boid)
            nb_neighbours = len(neighbours)
            for neighbour in neighbours:
                d = boid.position.distance(neighbour.position, self.width, self.height, self.isTore)
                boid.interact(d, neighbour.velocity, nb_neighbours, *weights_interactions_forces)

        #on colorie le dernier boid en rouge pour l'observation
        self.boids[self.num_boids-1].color = (255, 0, 0)

        #les boids avec lesquel IL interagit sont en bleu, pas ceux qui interagissent avec lui
        for boid in neighbours:
            boid.color = (0, 255, 0)

        #f vent
        wind_weight, wind_angle = self.wind
        boid.acceleration += Vector(math.cos(wind_angle), math.sin(wind_angle)) * wind_weight

        for boid in self.boids:
            boid.bounce(self.width, self.height, self.isTore, self.padding, bounce_weight)
                
        for boid in self.boids:
            boid.update(dt, self.max_speed, self.max_rotation)
        

    def draw(self, screen):
        ### NE PAS MODIFIER CETTE FONCTION ###
        for boid in self.boids:
            boid.draw(screen)
