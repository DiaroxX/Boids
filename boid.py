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

    def bounce(self, width, height, tore, padding=0):
        if tore:
            self.position.x %= width
            self.position.y %= height
        else:
            if self.position.x < padding:
                self.position.x = 2*padding - self.position.x
                self.velocity.x = abs(self.velocity.x)
                self.acceleration.x += 100
            elif self.position.x > width - padding:
                self.position.x = 2*(width - padding) - self.position.x
                self.velocity.x = -abs(self.velocity.x)
                self.acceleration.x -= 100

            if self.position.y < padding:
                self.position.y = 2*padding - self.position.y
                self.velocity.y = abs(self.velocity.y)
                self.acceleration.y += 100
            elif self.position.y > height - padding:
                self.position.y = 2*(height - padding) - self.position.y
                self.velocity.y = -abs(self.velocity.y)
                self.acceleration.y -= 100


            #self.position.x = max(padding, self.position.x)
            #self.position.x = min(width-padding, self.position.x)
            #self.position.y = max(padding, self.position.y)
            #self.position.y = min(height-padding, self.position.y)

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
        

    def update(self, dt, max_velocity_ang_diff=math.pi/16):
        v_initiale = Vector(self.velocity.x, self.velocity.y)
        self.velocity += self.acceleration * dt
        self.velocity.cap_magnitude(self.max_speed)
        self.velocity.cap_angle_diff(v_initiale, max_velocity_ang_diff)
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
    


