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
    def __init__(self, num_boids, width, height):
        self.num_boids = num_boids
        self.boids = []
        self.width = width
        self.height = height
        # initialize random boids
        for _ in range(num_boids):
            pos_x = random.randint(0, self.width)
            pos_y = random.randint(0, self.height)
            pos = Vector(pos_x, pos_y)
            vel_x = random.gauss(0, 1)
            vel_y = random.gauss(0, 1)
            vel = Vector(vel_x, vel_y)
            self.boids.append(Boid(pos, vel))
        
        #on choisit un boid a colorier en rouge pour l'observation
        self.boids[0].color = (255, 0, 0)

    def get_neighbours(self, boid, detection_radius, cone=False, fov=math.pi/2):
        neighbours = set()
        for other in self.boids:

            if boid == self.boids[0] and boid != other:
                other.color = (255, 255, 255)

            d = boid.position.distance(other.position, self.width, self.height)
            if d.magnitude() <= detection_radius:
                ang_diff = abs(angle_diff(boid.velocity.angle(), d.angle()))
                if not cone or ang_diff <= fov/2:
                    neighbours.add(other)
                    if boid == self.boids[0] and boid != other:
                        other.color = (0, 0, 255)

        if boid in neighbours:
            neighbours.remove(boid)

        return neighbours

    def update(self, dt, detection_radius):
        FOV = math.pi/2
        tore = False
        padding = 50

        for boid in self.boids:
            neighbours = self.get_neighbours(boid, detection_radius, cone=True, fov=FOV)
            nb_neighbours = len(neighbours)
            for neighbour in neighbours:
                d = boid.position.distance(neighbour.position, self.width, self.height, tore)
                boid.interact(d, neighbour.velocity, nb_neighbours)

        #f vent
        orientation = math.pi/4
        wind_strengh = 0.001
        wind = Vector(math.cos(orientation), math.sin(orientation)) * wind_strengh
        boid.acceleration += wind

        #f evite bords (deplacé dans bounce)
        """
        rappel_strengh = 100
        if not tore:
            rappel_au_centre = Vector(1/2 - boid.position.x/(self.width-padding), 1/2 - boid.position.y/(self.height-padding))
            rappel_strengh_mag = rappel_au_centre.magnitude()
            boid.acceleration += rappel_au_centre * rappel_strengh * (rappel_strengh_mag*rappel_strengh_mag)
        """

        for boid in self.boids:
            boid.bounce(self.width, self.height, tore, padding)
                
        for boid in self.boids:
            boid.update(dt, max_velocity_ang_diff=math.pi/32)
        

    def draw(self, screen):
        ### NE PAS MODIFIER CETTE FONCTION ###
        for boid in self.boids:
            boid.draw(screen)
