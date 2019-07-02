import pygame as pg
import numpy as np
from Utils import *
from TStructure import Queue
from Strategies import *


class BoatSprite(pg.sprite.Sprite):
    def __init__(self, filename, scale_factor, boat):
        super().__init__()
        self.boat = boat
        self.original_image = pg.image.load(filename)
        self.image = self.original_image
        self.scale_factor = scale_factor
        self.rect = self.image.get_rect()
        self.rect.center = scale_convert_vector(
            self.boat.pos, self.scale_factor)

    def __del__(self):
        del self.boat

    def update(self):
        self.boat.update()
        self.image = pg.transform.rotate(self.original_image, self.boat.angle)
        self.rect = self.image.get_rect()
        intPos = scale_convert_vector(self.boat.pos, self.scale_factor)
        self.rect.center = intPos

    def draw_trajectory(self, screen):
        if len(self.boat.pastTrajectory) > 1:
            convTraj = scale_convert_vector(
                self.boat.pastTrajectory.to_list(), self.scale_factor)
            pg.draw.lines(screen, (255, 0, 0), False, convTraj, 1)

    def save_pos(self):
        self.boat.save_pos()


class Boat():
    def __init__(self, boatName, nav_strat, start, targets, starting_speed=(0, 0), starting_angle=-90):
        self.name = boatName
        self.start = np.array(start, dtype=int)
        self.pos = np.array(start, dtype=float)
        self.angle = starting_angle
        self.angular_speed = 0
        self.speed = np.array(starting_speed, dtype=float)
        self.next_targets = Queue(targets)
        self.target = np.array(self.next_targets.pop(), dtype=int)
        self.target_reached = False
        self.engine_on = True
        self.gear = 1
        self.reverse = False
        self.thrust_power = 70
        self.mass = 700
        self.cape = 0
        self.pastTrajectory = Queue()
        self.dir = self.get_target_dir()
        self.nav_strat = nav_strat

    def update(self):
        if distance(self.target, self.pos) < 15:
            if len(self.next_targets) == 0:
                self.target_reached = True
                self.cape = 0
                self.gear = 0
            else:
                self.target = np.array(self.next_targets.pop(), dtype=int)
        if not self.target_reached:
            self.nav_strat(self, self.target)
            self.update_angle()
            self.update_speed()

    def update_speed(self):
        if self.engine_on:
            if self.reverse:
                self.speed -= self.thrust_power / self.mass * self.gear * self.dir
            else:
                self.speed += self.thrust_power / self.mass * self.gear * self.dir
        speedNorm = np.linalg.norm(self.speed)
        # Frottements fluides
        if speedNorm > 0:
            self.speed -= 10 * speedNorm * self.speed / self.mass
        elif speedNorm < 0:
            self.speed -= 10 * speedNorm * self.speed / self.mass
        self.pos = self.pos + self.speed

    def update_angle(self):
        self.angular_speed += 2 * self.thrust_power * self.cape / self.mass * self.gear
        self.angular_speed -= 100 / self.mass * self.angular_speed * self.gear
        self.angle += self.angular_speed
        angleRad = (self.angle + 90) * np.pi / 180
        self.dir = np.array([np.cos(angleRad), -np.sin(angleRad)])

    def get_target_dir(self):
        direc = self.target - self.pos
        return direc / np.linalg.norm(direc)

    def angle_with_target(self):
        return None  # TODO

    def save_pos(self):
        self.pastTrajectory.append(self.pos)
        if len(self.pastTrajectory) > 1000:
            _ = self.pastTrajectory.pop()
