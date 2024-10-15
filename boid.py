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
    def __init__(self, pos, vel):
        self.position = pos
        self.velocity = vel
        self.acceleration = Vector()
        self.max_speed = 0.3
        self.size = 2
        self.heading = self.velocity.angle() + math.pi / 2
        self.color = (255, 255, 255)

    def bounce(self, width, height):
        #corrigé je pense
        if self.position.x > width:
            self.position.x //= width
        if self.position.x < 0:
            self.position.x //= width
        if self.position.y > height:
            self.position.y //= height
        if self.position.y < 0:
            self.position.y //height

    def interact(self, d, n):
        # random behaviour
        #self.acceleration += Vector(random.gauss(0, 0.4), random.gauss(0, 0.4))

        #f evitement:
        d_mag = d.magnitude()
        self.acceleration += d/(n*d_mag*d_mag)

        #f groupement
        self.acceleration -= d/n

        

    def update(self, dt):
        self.velocity += self.acceleration * dt
        self.velocity.cap_magnitude(self.max_speed)
        #print(self.max_speed, self.velocity.magnitude())
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
    


