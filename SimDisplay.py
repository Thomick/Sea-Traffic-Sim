from Ocean import *
from Utils import *
import pygame as pg
from pygame.locals import *
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


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

    def runSim(self, framerate):
        done = False
        clock = pg.time.Clock()
        t1 = time.time()
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
                self.screen.fill(WHITE)
                for boat in self.boatGroup:
                    '''
                    if boat.boat.target_reached:
                        print(time.time() - t1)
                        done = True
                    '''
                    boat.draw_trajectory(self.screen)

                # collisions
                col = pg.sprite.groupcollide(
                    self.boatGroup, self.boatGroup, False, False)
                for b1 in col:
                    for b2 in col[b1]:
                        if not(b1 is b2):
                            print("Collision")
                            paused = True

                self.boatGroup.update()
                self.boatGroup.draw(self.screen)
                for t in self.targets:
                    pos = scale_convert_vector(t, self.scale_factor)
                    pg.draw.circle(self.screen, RED, pos, 5)

                for b in self.boatGroup:
                    for p in b.boat.phantom_boat.pastTrajectory:
                        pos = scale_convert_vector(p, self.scale_factor)
                        pg.draw.circle(self.screen, RED, pos, 5)

                pg.display.flip()
                i += 1
            clock.tick(framerate)
        pg.quit()
