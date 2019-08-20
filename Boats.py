import numpy as np
from Utils import *
from TStructure import Queue
from Strategies import *
from BoatFunctions import *
import copy


class Boat():
    def __init__(self, param, initState, targets):
        self.name = param['boatName']
        self.pos = np.array(initState['pos'], dtype=float)
        self.speed = np.array(initState['speed'], dtype=float)
        self.angle = initState['angle']
        self.angular_speed = initState['angular_speed']
        self.next_targets = Queue(targets)
        if len(self.next_targets) > 0:
            self.target = np.array(self.next_targets.pop(), dtype=float)
            self.target_reached = False
        else:
            self.target = self.pos
            self.target_reached = True
        self.engine_on = initState['engine_on']
        self.gear = initState['gear']
        self.max_gear = param['max_gear']
        self.reverse = initState['reverse']
        self.thrust_power = param['thrust_power']
        self.mass = param['mass']
        self.cape = initState['cape']
        angleRad = (self.angle + 90) * np.pi / 180
        self.dir = np.array([np.cos(angleRad), -np.sin(angleRad)])
        self.max_step_history = param['max_step_history']
        self.reset_history()
        self.save_delay = param['save_delay']
        self.colRadius = param['colRadius']
        self.boatList = [self]
        self.isColliding = False
        #print(f'{self.name} created')

    def update(self):
        if not self.target_reached:
            self.do_action()
            if distance(self.target, self.pos) < self.colRadius:
                if len(self.next_targets) == 0:
                    self.target_reached = True
                    self.cape = 0
                    self.gear = 0
                else:
                    self.target = np.array(self.next_targets.pop(), dtype=int)
        else:
            self.gear = 0
        self.update_angle()
        self.update_speed()
        self.collision()
        if self.total_step % self.save_delay == 0:
            self.save_pos()
        self.total_step += 1

    def do_action(self):
        pass

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
        if self.engine_on:
            self.angular_speed += 2 * self.thrust_power * self.cape / self.mass * self.gear
        # Coupe resistant
        self.angular_speed -= 100 / self.mass * self.angular_speed
        self.angle += self.angular_speed
        angleRad = (self.angle + 90) * np.pi / 180
        self.dir = np.array([np.cos(angleRad), -np.sin(angleRad)])

    def save_pos(self):
        self.pastTrajectory.append(self.pos)

    def reset_history(self):
        self.total_step = 0
        self.pastTrajectory = Queue(max_length=self.max_step_history)

    def add_target(targetList):
        self.target_reached = False
        for t in targetList:
            self.next_targets.append(t)

    def change_gear(self, increase=True):
        if increase:
            if self.gear < self.max_gear:
                self.gear += 1
        elif self.gear > 0:
            self.gear -= 1

    def collision(self):
        for boat in self.boatList:
            if not boat is self:
                if collide(self, boat):
                    self.isColliding = True
                    #print(f"Collision entre {self.name} et {boat.name}")
                    return None
        self.isColliding = False


class LocTRBoat(Boat):
    def __init__(self, param, initState, targets):
        super().__init__(param, initState, targets)
        self.common_nav_strat = follow_target
        self.maneuver = []
        self.phantom_advance = param['phantom_advance']
        self.phantom_boat = PhantomBoat(self, self.phantom_advance)
        self.reset_phantom()
        self.excluded = []

    def update(self):
        self.excluded.append(self)
        self.phantom_step()
        for b in self.boatList:
            if not any(b is ex for ex in self.excluded):
                col, _ = prev_collision(self, b, step=0, nb_test=3)
                if col:
                    self.maneuver.append(-1)
                    self.reset_phantom()
                    b.excluded.append(self)
                    break
        self.excluded = []
        super().update()

    def do_action(self):
        if len(self.maneuver) > 0:
            self.cape = self.maneuver.pop()
        else:
            follow_target(self)

    def phantom_step(self):
        i = 0
        while True:
            self.phantom_boat.update()
            i += 1
            if len(self.phantom_boat.pastTrajectory) == self.phantom_advance:
                break

    def reset_phantom(self):
        #self.phantom_boat = PhantomBoat(self, self.phantom_advance)
        self.phantom_boat.reset(self)
        self.phantom_step()


class PhantomBoat(Boat):
    def __init__(self, boat, advance):
        self.name = boat.name
        self.thrust_power = boat.thrust_power
        self.mass = boat.mass
        self.max_step_history = advance
        self.save_delay = 1
        self.colRadius = boat.colRadius
        self.boatList = boat.boatList
        self.reset(boat)
        #print(f'Phantom of {self.name} created')

    def do_action(self):
        if len(self.maneuver) > 0:
            self.cape = self.maneuver.pop()
        else:
            follow_target(self)

    def collision(self):
        pass

    def reset(self, boat):
        self.pos = copy.copy(boat.pos)
        self.angle = boat.angle
        self.angular_speed = boat.angular_speed
        self.speed = copy.copy(boat.speed)
        self.next_targets = copy.deepcopy(boat.next_targets)
        self.target = copy.deepcopy(boat.target)
        self.target_reached = boat.target_reached
        self.engine_on = boat.engine_on
        self.gear = boat.gear
        self.reverse = boat.reverse
        self.cape = boat.cape
        self.dir = copy.copy(boat.dir)
        self.maneuver = copy.copy(boat.maneuver)
        self.reset_history()
