import math
import numpy as np
import random
import pygame
from vector import Vector

class Boid:
    """
    A single simulated boid that can interact with its surroundings and act
    according to boids rules.
    """
    def __init__(self, pos, vel, color=(255, 255, 255)):
        self.position = pos
        self.velocity = vel
        self.acceleration = Vector()
        self.max_speed = 0.3
        self.size = 2
        self.heading = self.velocity.angle() + math.pi / 2
        self.color = color

    def bounce(self, width, height):
        #corrigé je pense
        """
        if self.position.x > width:
            self.position.x //= width
        if self.position.x < 0:
            self.position.x //= width #utile seulement si le boid se déplace de plus d'un écran par frame
            self.position.x += width

        if self.position.y > height:
            self.position.y //= height
        if self.position.y < 0:
            self.position.y //= height #utile seulement si le boid se déplace de plus d'un écran par frame
            self.position.y += height
        """
        self.position.x %= width
        self.position.y %= height

    def interact(self, d, v, n, coeffs=(25, 0.015, 7)):
        # random behaviour
        #self.acceleration += Vector(random.gauss(0, 0.4), random.gauss(0, 0.4))

        c1, c2, c3 = coeffs

        #f evitement:
        d_mag = d.magnitude()
        self.acceleration -= c1*d/(n*d_mag*d_mag)

        #f groupement
        self.acceleration += c2*d/n

        #f alignement
        self.acceleration += c3*v/n

        #f vent
        orientation = math.pi*2.25
        wind_strengh = 0.001
        wind = Vector(math.cos(orientation), math.sin(orientation)) * wind_strengh
        self.acceleration += wind

        

    def update(self, dt):
        self.velocity += self.acceleration * dt
        self.velocity.cap_magnitude(self.max_speed)
        self.position += self.velocity * dt
        self.heading = self.velocity.angle() + math.pi / 2
        # reset acceleration
        self.acceleration = Vector()

    def rotation_2D(self, angle):
        ### NE PAS MODIFIER CETTE FONCTION ###
        return np.array(
            [
                [math.cos(angle), -math.sin(angle)],
                [math.sin(angle), math.cos(angle)],
            ]
        )
    
    def draw(self, screen):
        ### NE PAS MODIFIER CETTE FONCTION ###
        size = 10
        # 2D triangle facing down
        points = [
            (0,-size),
            (size//2,size//2),
            (-size//2,size//2)
        ]
        rotated_points = []
        rot = self.rotation_2D(self.heading)
        rotated_points = (rot@np.array(points).T).T
        rotated_points = [
            tuple([p[0]+self.position.x, p[1]+self.position.y]) for p in rotated_points
        ]
        pygame.draw.polygon(screen, self.color, rotated_points, width=2)

    def __repr__(self):
        ### NE PAS MODIFIER CETTE FONCTION ###
        return f"Boid ({self.position.x:.1f}, {self.position.y:.1f})"
    


