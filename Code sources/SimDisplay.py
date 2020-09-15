from Utils import scale_convert_vector
import pygame as pg
from VectorFieldViewer import plot_vectorfield
import os

c = {"BLACK": (0, 0, 0),
     "WHITE": (255, 255, 255),
     "RED": (255, 0, 0),
     "GREEN": (0, 255, 0),
     "BLUE": (0, 0, 255)}


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

    def step(self, draw_traj=False):
        self.screen.fill(c["WHITE"])
        for boat in self.boatGroup:
            boat.draw_trajectory(self.screen)

        self.boatGroup.update()
        if draw_traj:
            for b in self.boatGroup:
                j = 0
                for p in b.boat.phantom_boat.pastTrajectory:
                    if j % 10 == 0:
                        pos = scale_convert_vector(p, self.scale_factor)
                        pg.draw.circle(self.screen, c["BLUE"], pos, 2)
                    j += 1

        self.boatGroup.draw(self.screen)
        for t in self.targets:
            pos = scale_convert_vector(t, self.scale_factor)
            pg.draw.circle(self.screen, c["BLUE"], pos, 30, 3)

        for b in self.boats:
            if b.isColliding:
                #paused = True
                pass
        pg.display.flip()

    def runSim(self, framerate=100, nb_step=-1, pause_on_start=True, draw_traj=False, vector_field=False):
        done = False
        clock = pg.time.Clock()
        paused = False
        i = 0
        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        paused = not paused
                    elif vector_field and event.key == pg.K_v:
                        plot_vectorfield(
                            self.boats, self.screen_size, self.screen_size[0] // 30)

            if not paused:
                self.step(draw_traj)
                i += 1
            clock.tick(framerate)
            if pause_on_start and i == 1:
                paused = True
            if i == nb_step:
                done = True
        print(f"Duree Sim : {i}")
        pg.quit()


class BoatSprite(pg.sprite.Sprite):
    def __init__(self, filepath, scale_factor, boat, scale_icon=False):
        super().__init__()
        self.boat = boat
        self.icon_path = os.path.join(os.path.dirname(
            __file__), self.boat.icon_path)
        self.color = c[self.boat.color]
        self.scale_factor = scale_factor
        self.size = int(self.boat.colRadius * self.scale_factor)
        self.original_image = pg.image.load(self.icon_path)
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
            pg.draw.lines(screen, self.color, False, convTraj, 1)

    def save_pos(self):
        self.boat.save_pos()
