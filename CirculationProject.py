from Ocean import *
from Utils import *
import pygame as pg
from pygame.locals import *
import numpy as np

pg.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen_size = screen_width, screen_height = [900, 600]
screen = pg.display.set_mode(screen_size)
screen_rect = screen.get_rect()

boatFile = "boat.png"
boatList = pg.sprite.Group()

done = False
clock = pg.time.Clock()
boat1 = Boat(boatFile, "Bateau 1", (10, 200), (590, 200))
boat2 = Boat(boatFile, "Bateau 2", (590, 200), (10, 200), starting_angle=90)
boatList.add(boat1)
boatList.add(boat2)

while not done:
    for event in pg.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                boat1.gear = 0
        elif event.type == KEYUP:
            if event.key == K_SPACE:
                boat1.gear = 2

    for boat in boatList:
        if boat.target_reached:
            boatList.remove(boat)
            del boat

    if pg.sprite.collide_rect(boat1, boat2):
        print("Collision")

    screen.fill(WHITE)

    for boat in boatList:
        boat.draw_trajectory(screen)
        #pg.draw.line(screen, WHITE, boat.start, boat.target, 1)

    boatList.update()
    boatList.draw(screen)

    clock.tick(100)
    pg.display.flip()

pg.quit()
