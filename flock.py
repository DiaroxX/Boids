import random 
from boid import Boid
from vector import Vector

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

    def get_neighbours(self, boid, detection_radius):
        neighbours = set()
        for other in self.boids:
            d = boid.position - other.position
            if d.magnitude() <= detection_radius:
                neighbours.add(other)

        neighbours.remove(boid)
        return neighbours

    def update(self, dt, detection_radius):
        for boid in self.boids:
            neighbours = self.get_neighbours(boid, detection_radius)
            nb_neighbours = len(neighbours)
            for neighbour in neighbours:
                d = boid.position - neighbour.position
                boid.interact(d, nb_neighbours)


        for boid in self.boids:
            boid.bounce(self.width, self.height)
                
        for boid in self.boids:
            boid.update(dt)
        

    def draw(self, screen):
        ### NE PAS MODIFIER CETTE FONCTION ###
        for boid in self.boids:
            boid.draw(screen)
