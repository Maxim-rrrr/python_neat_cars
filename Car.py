import pygame
import random
import math

from config import width, height, bg, speed


class Car:
    car_sprites = ("Audi", "Black_viper", "Orange")

    def __init__(self):
        self.random_sprite()

        self.angle = 0
        self.speed = 5

        self.radars = []
        self.collision_points = []

        self.is_alive = True
        self.goal = False
        self.distance = 0
        self.time_spent = 0

    def random_sprite(self):
        self.car_sprite = pygame.image.load('sprites/' + random.choice(self.car_sprites) + '.png')
        self.car_sprite = pygame.transform.scale(self.car_sprite,
                                                 (math.floor(self.car_sprite.get_size()[0] / 2),
                                                  math.floor(self.car_sprite.get_size()[1] / 2)))
        self.car = self.car_sprite

        self.pos = [650, 930]
        self.compute_center()

    def compute_center(self):
        self.center = (self.pos[0] + (self.car.get_size()[0] / 2), self.pos[1] + (self.car.get_size()[1] / 2))

    def draw(self, screen):
        screen.blit(self.car, self.pos)
        self.draw_radars(screen)

    def draw_center(self, screen):
        pygame.draw.circle(screen, (0, 72, 186), (math.floor(self.center[0]), math.floor(self.center[1])), 5)

    def draw_radars(self, screen):
        for r in self.radars:
            p, d = r
            pygame.draw.line(screen, (183, 235, 70), self.center, p, 1)
            pygame.draw.circle(screen, (183, 235, 70), p, 5)

    def compute_radars(self, degree, road):
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        while not road.get_at((x, y)) == bg and length < 300:
            length = length + 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])

    def compute_collision_points(self):
        self.compute_center()
        lw = 65
        lh = 65

        lt = [self.center[0] + math.cos(math.radians(360 - (self.angle + 20))) * lw,
              self.center[1] + math.sin(math.radians(360 - (self.angle + 20))) * lh]
        rt = [self.center[0] + math.cos(math.radians(360 - (self.angle + 160))) * lw,
              self.center[1] + math.sin(math.radians(360 - (self.angle + 160))) * lh]
        lb = [self.center[0] + math.cos(math.radians(360 - (self.angle + 200))) * lw,
              self.center[1] + math.sin(math.radians(360 - (self.angle + 200))) * lh]
        rb = [self.center[0] + math.cos(math.radians(360 - (self.angle + 340))) * lw,
              self.center[1] + math.sin(math.radians(360 - (self.angle + 340))) * lh]

        self.collision_points = [lt, rt, lb, rb]

    def draw_collision_points(self, road, screen):
        if not self.collision_points:
            self.compute_collision_points()

        for p in self.collision_points:
            if road.get_at((int(p[0]), int(p[1]))) == bg:
                pygame.draw.circle(screen, (255, 0, 0), (int(p[0]), int(p[1])), 5)
            else:
                pygame.draw.circle(screen, (15, 192, 252), (int(p[0]), int(p[1])), 5)

    def check_collision(self, road):
        self.is_alive = True

        for p in self.collision_points:
            try:
                if road.get_at((int(p[0]), int(p[1]))) == bg:
                    self.is_alive = False
                    break
            except IndexError:
                self.is_alive = False

    def rotate(self, angle):
        orig_rect = self.car_sprite.get_rect()
        rot_image = pygame.transform.rotate(self.car_sprite, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()

        self.car = rot_image

    def get_data(self):
        radars = self.radars
        data = [0, 0, 0, 0, 0]

        for i, r in enumerate(radars):
            data[i] = int(r[1] / 30)

        return data

    def get_reward(self):
        return self.distance / 50.0

    def update(self, road):
        self.speed = speed

        self.rotate(self.angle)

        self.pos[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        if self.pos[0] < 20:
            self.pos[0] = 20
        elif self.pos[0] > width - 120:
            self.pos[0] = width - 120

        self.pos[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        if self.pos[1] < 20:
            self.pos[1] = 20
        elif self.pos[1] > height - 120:
            self.pos[1] = height - 120

        self.distance += self.speed
        self.time_spent += 1  # aka turns

        self.compute_collision_points()
        self.check_collision(road)

        self.radars.clear()
        for d in range(-90, 120, 45):
            self.compute_radars(d, road)
