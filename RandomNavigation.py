from Ocean import *
from Utils import *
import pygame as pg
from pygame.locals import *
import numpy as np

pg.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen_size = screen_width, screen_height = [600, 400]
screen = pg.display.set_mode(screen_size)
screen_rect = screen.get_rect()

boatFile = "boat.png"
boatList = pg.sprite.Group()

done = False
clock = pg.time.Clock()
angle = 0

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

    for boat in boatList:
        if boat.target_reached:
            boatList.remove(boat)
            del boat

    while len(boatList) < 10:
        start = random_point_on_edge(screen_rect)
        target = random_point_on_edge(screen_rect)
        boat = Boat(boatFile, np.random.randint(1, 4), start, target)
        boatList.add(boat)

    screen.fill(BLACK)

    for boat in boatList:
        boat.draw_trajectory(screen)

    boatList.update()
    boatList.draw(screen)

    clock.tick(60)
    pg.display.flip()

pg.quit()
