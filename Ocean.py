import pygame as pg
import numpy as np
from Utils import *
from TStructure import Queue
from Strategies import *
from TNeuralNetwork import *


class Boat(pg.sprite.Sprite):
    def __init__(self, filename, scale_factor, boatName, nav_strat, start, target, starting_speed=(0, 0), starting_angle=-90):
        super().__init__()
        self.original_image = pg.image.load(filename)
        self.image = self.original_image
        self.scale_factor = scale_factor
        self.rect = self.image.get_rect()
        self.name = boatName
        self.start = np.array(start, dtype=int)
        self.pos = np.array(start, dtype=float)
        self.rect.center = self.pos
        self.angle = starting_angle
        self.angular_speed = 0
        self.speed = np.array(starting_speed, dtype=float)
        self.target = np.array(target, dtype=int)
        self.target_reached = False
        self.engine_on = True
        self.gear = 1
        self.reverse = False
        self.thrust_power = 40
        self.mass = 700
        self.cape = 0
        self.pastTrajectory = Queue()
        self.dir = self.get_target_dir()
        self.nav_strat = nav_strat

    def update(self):
        if distance(self.target, self.pos) < 15:
            self.target_reached = True
        if not self.target_reached:
            self.nav_strat(self, self.target)
            self.update_angle()
            self.update_speed()
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        intPos = scale_convert_vector(self.pos, self.scale_factor)
        self.rect.center = intPos
        self.pastTrajectory.append(intPos)
        if len(self.pastTrajectory) > 500:
            _ = self.pastTrajectory.pop()

    def draw_trajectory(self, screen):
        if len(self.pastTrajectory) > 1:
            pg.draw.lines(screen, (255, 0, 0), False,
                          self.pastTrajectory.to_list(), 1)

    def update_speed(self):
        if self.engine_on:
            if self.reverse:
                self.speed -= self.thrust_power / self.mass * self.gear * self.dir
            else:
                self.speed += self.thrust_power / self.mass * self.gear * self.dir
        speedNorm = np.linalg.norm(self.speed)
        # Frottements fluides
        if speedNorm > 0:
            self.speed -= 10 / self.mass * speedNorm * self.speed
        elif speedNorm < 0:
            self.speed -= 10 / self.mass * speedNorm * self.speed
        self.pos = self.pos + self.speed

    def update_angle(self):
        self.angular_speed += 10 * self.cape / self.mass
        self.angular_speed -= 3 / self.mass * self.angular_speed
        self.angle += self.angular_speed
        angleRad = (self.angle + 90) * np.pi / 180
        self.dir = np.array([np.cos(angleRad), -np.sin(angleRad)])

    def get_target_dir(self):
        direc = self.target - self.pos
        return direc / np.linalg.norm(direc)

    def angle_with_target(self):
        return None  # TODO


def BoatNN(Boat):
    def __init__(self, filename, scale_factor, boatName, NNType, weigths, start, target, starting_speed=(0, 0), starting_angle=-90):
        self.weigths = weigths
        self.NNType = NNType
        super().__init__(filename, scale_factor, boatName, nav_strat,
                         start, target, starting_speed, starting_angle)

    def nextCape(self)
        Ninput = [self.pos[0], self.pos[2], self.speed[0], self.speed[1],
                  self.angle, self.angular_speed, self.angle_with_target]
