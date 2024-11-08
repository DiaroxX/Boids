import math
import numpy as np
import pygame
from vector import Vector

class Boid:
    """
    A single simulated boid that can interact with its surroundings and act
    according to boids rules.
    """
    def __init__(self, pos, vel, ):
        self.position = pos
        self.velocity = vel
        self.acceleration = Vector()
        #vitesse max deplacee dans flock car commune a tous les boids
        self.size = 2
        self.heading = self.velocity.angle() + math.pi / 2
        self.color = (255, 255, 255)

    def bounce(self, width, height, isTore, padding, weight):
        if isTore:
            self.position.x %= width
            self.position.y %= height
        else:
            if self.position.x < padding:
                self.position.x = 2*padding - self.position.x
                self.velocity.x = abs(self.velocity.x)
                self.acceleration.x += weight
            elif self.position.x > width - padding:
                self.position.x = 2*(width - padding) - self.position.x
                self.velocity.x = -abs(self.velocity.x)
                self.acceleration.x -= weight

            if self.position.y < padding:
                self.position.y = 2*padding - self.position.y
                self.velocity.y = abs(self.velocity.y)
                self.acceleration.y += weight
            elif self.position.y > height - padding:
                self.position.y = 2*(height - padding) - self.position.y
                self.velocity.y = -abs(self.velocity.y)
                self.acceleration.y -= weight


    def interact(self, d, v, n, alignment_weight, cohesion_weight, avoidance_weight):
        """
        dans cette modélisation interact realise l'interaction entre 2 boids voisins
        et non pas celle d'un boid avec l'ensemble des ses voisins
        """
        d_mag = d.magnitude()

        #f evitement:
        self.acceleration -= avoidance_weight*d/(n*d_mag*d_mag)

        #f groupement
        self.acceleration += cohesion_weight*d/n

        #f alignement
        self.acceleration += alignment_weight*v/n
        

    def update(self, dt, max_speed, max_rotation):
        v_initiale = Vector(self.velocity.x, self.velocity.y)

        self.velocity += self.acceleration * dt
        self.velocity.cap_angle_diff(v_initiale, max_rotation)
        self.velocity.cap_magnitude(max_speed)
        
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
    


