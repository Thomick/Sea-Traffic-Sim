import pygame as pg
import numpy as np
from TStructure import Queue


def distance(A, B):
    return np.linalg.norm(A - B)


class Boat(pg.sprite.Sprite):
    def __init__(self, filename, boatName, start, target, starting_speed=(0, 0), starting_angle=-90):
        super().__init__()
        self.original_image = pg.image.load(filename)
        self.image = self.original_image
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
        self.gear = 2
        self.reverse = False
        self.thrust_power = 60
        self.mass = 700
        self.cape = 1
        self.pastTrajectory = Queue()
        self.dir = self.get_target_dir()

    def update(self):
        if distance(self.target, self.pos) < 5:
            self.target_reached = True
        if not self.target_reached:
            self.update_angle()
            self.update_speed()
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        intPos = np.around(self.pos)
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
            self.speed -= 0.02 * speedNorm**2 * self.speed
        elif speedNorm < 0:
            self.speed -= 0.02 * speedNorm**2 * self.speed
        self.pos = self.pos + self.speed

    def update_angle(self):
        self.angular_speed += 10 * self.cape / self.mass
        self.angular_speed -= 0.2 * self.angular_speed**3
        self.angle += self.angular_speed
        angleRad = (self.angle + 90) * np.pi / 180
        self.dir = np.array([np.cos(angleRad), -np.sin(angleRad)])

    def get_target_dir(self):
        direc = self.target - self.pos
        return direc / np.linalg.norm(direc)
