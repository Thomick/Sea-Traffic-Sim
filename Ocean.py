import pygame as pg
import numpy as np
from Utils import *
from TStructure import Queue
from Strategies import *
import copy


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
    def __init__(self, boatName, nav_strat, start, targets, starting_speed=(0, 0), starting_angle=-90, angular_speed=0, mass=700):
        self.name = boatName
        self.start = np.array(start, dtype=int)
        self.pos = np.array(start, dtype=float)
        self.angle = starting_angle
        self.angular_speed = angular_speed
        self.speed = np.array(starting_speed, dtype=float)
        self.next_targets = Queue(targets)
        if len(self.next_targets) > 0:
            self.target = np.array(self.next_targets.pop(), dtype=int)
            self.target_reached = False
        else:
            self.target = None
            self.target_reached = True
        self.engine_on = True
        self.gear = 1
        self.reverse = False
        self.thrust_power = 70
        self.mass = mass
        self.cape = 0
        angleRad = (self.angle + 90) * np.pi / 180
        self.dir = np.array([np.cos(angleRad), -np.sin(angleRad)])
        self.nav_strat = nav_strat
        self.is_phantom = False
        self.phantom_boat = None
        self.reset_history()
        self.max_step_history = 1000
        self.save_delay = 10
        print(f'{self.name} created')

    def update(self):
        if not self.is_phantom:
            if self.phantom_boat == None or self.total_step % 1000 == 0:
                self.reset_phantom()
            else:
                self.phantom_boat.update()

        if not self.target_reached:
            self.nav_strat(self, self.target)
            self.update_angle()
            self.update_speed()
            if distance(self.target, self.pos) < 15:
                if len(self.next_targets) == 0:
                    self.target = None
                    self.target_reached = True
                    self.cape = 0
                    self.gear = 0
                else:
                    self.target = np.array(self.next_targets.pop(), dtype=int)
        if self.total_step % self.save_delay == 0:
            self.save_pos()
        self.total_step += 1

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

    def angle_with_target(self):
        return None  # TODO

    def save_pos(self):
        self.pastTrajectory.append(self.pos)
        while len(self.pastTrajectory) > self.max_step_history:
            _ = self.pastTrajectory.pop()

    def reset_history(self):
        self.total_step = 0
        self.pastTrajectory = Queue()

    def reset_phantom(self):
        self.phantom_boat = PhantomBoat(self)
        for i in range(1001):
            self.phantom_boat.update()


class PhantomBoat(Boat):
    def __init__(self, boat):
        self.name = boat.name
        self.start = boat.start
        self.pos = copy.copy(boat.pos)
        self.angle = boat.angle
        self.angular_speed = boat.angular_speed
        self.speed = copy.copy(boat.speed)
        self.next_targets = boat.next_targets
        self.target = copy.deepcopy(boat.target)
        self.target_reached = boat.target_reached
        self.engine_on = boat.engine_on
        self.gear = boat.gear
        self.reverse = boat.reverse
        self.thrust_power = boat.thrust_power
        self.mass = boat.mass
        self.cape = boat.cape
        self.dir = copy.copy(boat.dir)
        self.nav_strat = boat.nav_strat
        self.is_phantom = True
        self.phantom_boat = None
        self.reset_history()
        self.max_step_history = 9
        self.save_delay = 100
        print(f'Phantom of {self.name} created')
