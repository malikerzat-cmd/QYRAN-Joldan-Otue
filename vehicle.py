import pygame, random
from settings import WIDTH, HEIGHT, CELL, asset_path

class Vehicle:
    def __init__(self, lane, direction, speed, image_name, size):
        self.lane, self.direction, self.speed = lane, direction, speed
        self.image = pygame.image.load(asset_path(image_name)).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.width = size[0]
        self.x = float(random.randint(-80, WIDTH))

    def update(self, dt):
        self.x += self.speed * self.direction * dt
        if self.direction == 1 and self.x > WIDTH: self.x = -self.width - random.randint(50, 180)
        elif self.direction == -1 and self.x + self.width < 0: self.x = WIDTH + random.randint(50, 180)

    def get_rect(self, camera):
        y = HEIGHT - 120 - (self.lane - camera) * CELL
        return pygame.Rect(int(self.x), int(y + 8), self.width, 48)

    def draw(self, screen, camera):
        rect = self.get_rect(camera)
        if -70 < rect.y < HEIGHT + 70: screen.blit(self.image, rect)

class Car(Vehicle):
    def __init__(self, lane, direction, level):
        super().__init__(lane, direction, random.randint(100,150)+level*15, "car.png", (64,42))

class Truck(Vehicle):
    def __init__(self, lane, direction, level):
        super().__init__(lane, direction, random.randint(70,110)+level*10, "truck.png", (86,48))
