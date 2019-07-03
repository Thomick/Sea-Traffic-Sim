import numpy as np
from Utils import *
from TStructure import Queue
from Strategies import *
import copy


class Boat():
    def __init__(self, boatName, nav_strat, avoid_strat, start, targets, starting_speed=(0, 0), starting_angle=-90, angular_speed=0, mass=700):
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
        self.common_nav_strat = nav_strat
        self.avoid_strat = avoid_strat
        self.nav_strat = strat_or_maneuver
        self.maneuver = []
        self.is_phantom = False
        self.phantom_advance = 300
        self.reset_history()
        self.max_step_history = 1000
        self.save_delay = 10
        self.colRadius = 20
        print(f'{self.name} created')
        self.reset_phantom()

    def update(self):
        if not self.is_phantom:
            if self.phantom_boat == None:
                self.reset_phantom()
            else:
                self.phantom_boat.update()

        if not self.target_reached:
            self.nav_strat(self, self.target)
            if distance(self.target, self.pos) < self.colRadius:
                if len(self.next_targets) == 0:
                    self.target = None
                    self.target_reached = True
                    self.cape = 0
                    self.gear = 0
                else:
                    self.target = np.array(self.next_targets.pop(), dtype=int)
        else:
            gear = 0
        self.update_angle()
        self.update_speed()
        if self.total_step % self.save_delay == 0:
            self.save_pos()
        self.total_step += 1

    def update_speed(self):
        if self.engine_on:
            if self.reverse:
                self.speed -= 0.1 * self.thrust_power / self.mass * self.gear * self.dir
            else:
                self.speed += 0.1 * self.thrust_power / self.mass * self.gear * self.dir
        speedNorm = np.linalg.norm(self.speed)
        # Frottements fluides
        self.speed -= 10 * speedNorm * self.speed / self.mass
        self.pos = self.pos + self.speed

    def update_angle(self):
        self.angular_speed += 2 * self.thrust_power * self.cape / self.mass * self.gear
        self.angular_speed -= 100 / self.mass * self.angular_speed
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
        self.phantom_boat = PhantomBoat(self, self.phantom_advance)
        for i in range(self.phantom_advance):
            self.phantom_boat.update()

    def establish_maneuver(self):
        if not self.target_reached:
            self.avoid_strat(self)
            self.reset_phantom()
            return True
        return False


class PhantomBoat(Boat):
    def __init__(self, boat, advance):
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
        self.common_nav_strat = boat.common_nav_strat
        self.nav_strat = strat_or_maneuver
        self.maneuver = copy.deepcopy(boat.maneuver)
        self.is_phantom = True
        self.phantom_boat = None
        self.reset_history()
        self.max_step_history = advance
        self.save_delay = 1
        self.colRadius = boat.colRadius
        print(f'Phantom of {self.name} created')
