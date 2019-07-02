from Ocean import *
from Utils import *
import pygame as pg
from pygame.locals import *
import numpy as np
from Strategies import *

pg.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

scale_factor = 1 / 10

screen_size = screen_width, screen_height = [900, 600]
screen = pg.display.set_mode(screen_size)
screen_rect = screen.get_rect()

boatFile = "boat2.png"
boatList = pg.sprite.Group()

done = False
clock = pg.time.Clock()

targets = [(1000, 2000), (3000, 1000), (6000, 4000), (7000, 1000)]
boat1 = Boat(boatFile, scale_factor, "Bateau 1", follow_target,
             (200, 200), targets)
boat2 = Boat(boatFile, scale_factor, "Bateau 2", follow_target,
             (5000, 5000), targets[::-1])
boatList.add(boat1)
boatList.add(boat2)

paused = False
i = 0
while not done:
    for event in pg.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == KEYDOWN:
            if event.key == K_p:
                paused = not paused
            if event.key == K_SPACE:
                boat1.gear = 0
                boat1.cape = 0
        elif event.type == KEYUP:
            if event.key == K_SPACE:
                boat1.gear = 2
                boat1.cape = 1

    if not paused:
        key = pg.key.get_pressed()
        boat1.cape = 0
        if key[K_RIGHT]:
            boat1.cape = -1
        if key[K_LEFT]:
            boat1.cape = 1
        '''
        for boat in boatList:
            if boat.target_reached:
                boatList.remove(boat)
                del boat
        '''
        '''
        if pg.sprite.collide_rect(boat1, boat2):
            print("Collision")
        '''
        screen.fill(WHITE)

        for boat in boatList:
            boat.draw_trajectory(screen)
            #pg.draw.line(screen, WHITE, boat.start, boat.target, 1)

        # collsions
        col = pg.sprite.groupcollide(boatList, boatList, False, False)
        for b1 in col:
            for b2 in col[b1]:
                if not(b1 is b2):
                    print("Collision")
                    paused = True

        if i % 10 == 0:
            for boat in boatList:
                boat.save_pos()

        boatList.update()
        boatList.draw(screen)
        for t in targets:
            pg.draw.circle(
                screen, RED, scale_convert_vector(t, scale_factor), 5)

        clock.tick(6000)
        pg.display.flip()
        i += 1
pg.quit()
