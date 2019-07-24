from Boats import *
from Utils import *
from BoatFunctions import *
import pygame as pg
from pygame.locals import *
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class SimDisplay():
    def __init__(self, screen_size, boatFile):
        self.screen_size = self.screen_width, self.screen_height = [900, 600]
        self.boatFile = boatFile

    def initDisplay(self, boats, scale_factor, targets):
        pg.init()
        self.scale_factor = scale_factor
        self.boats = boats
        self.boatGroup = pg.sprite.Group()
        for b in self.boats:
            bSprite = BoatSprite(self.boatFile, self.scale_factor, b)
            self.boatGroup.add(bSprite)
        self.targets = targets
        self.screen = pg.display.set_mode(self.screen_size)
    
    def step(self):
        self.screen.fill(WHITE)
        for boat in self.boatGroup:
            boat.draw_trajectory(self.screen)

        self.boatGroup.update()
        '''
        for b in self.boatGroup:
            j = 0
            for p in b.boat.phantom_boat.pastTrajectory:
                if j % 100 == 0:
                    pos = scale_convert_vector(p, self.scale_factor)
                    pg.draw.circle(self.screen, BLUE, pos, 5)
                j += 1
        '''
        self.boatGroup.draw(self.screen)
        for t in self.targets:
            pos = scale_convert_vector(t, self.scale_factor)
            pg.draw.circle(self.screen, RED, pos, 5)

        for b in self.boats:
            if b.isColliding:
                #paused = True
                pass
        pg.display.flip()

    def runSim(self, framerate = 60, nb_step = -1,pause_on_start = True):
        done = False
        clock = pg.time.Clock()
        paused = False
        i = 0
        while not done:
            for event in pg.event.get():
                if event.type == QUIT:
                    done = True
                elif event.type == KEYDOWN:
                    if event.key == K_p:
                        paused = not paused

            if not paused:
                self.step()
                i += 1
            clock.tick(framerate)
            if pause_on_start and i == 1:
                paused = True
            if i == nb_step:
                done = True
        pg.quit()


class BoatSprite(pg.sprite.Sprite):
    def __init__(self, filename, scale_factor, boat, scale_icon=False):
        super().__init__()
        self.boat = boat
        self.scale_factor = scale_factor
        self.size = int(self.boat.colRadius * self.scale_factor)
        self.original_image = pg.image.load(filename)
        if scale_icon:
            im_size = self.original_image.get_size()
            self.scaled_image = pg.transform.scale(
                self.original_image, (self.size, int(self.size * im_size[1] / im_size[0])))
        else:
            self.scaled_image = self.original_image
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = scale_convert_vector(
            self.boat.pos, self.scale_factor)

    def __del__(self):
        del self.boat

    def update(self):
        self.boat.update()
        self.image = pg.transform.rotate(self.scaled_image, self.boat.angle)
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
