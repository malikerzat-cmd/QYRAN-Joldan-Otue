import pygame
from settings import CELL, COLS, HEIGHT, asset_path

class Player:
    def __init__(self):
        self.frames = [pygame.image.load(asset_path(f"player_{i}.png")).convert_alpha() for i in range(2)]
        self.frames = [pygame.transform.scale(img, (48, 54)) for img in self.frames]
        self.reset()

    def reset(self):
        self.x, self.y = 4, 0
        self.is_alive = True
        self.frame = 0
        self.last_frame = pygame.time.get_ticks()

    def move(self, direction):
        if not self.is_alive: return
        if direction == "up": self.y += 1
        elif direction == "down": self.y = max(0, self.y - 1)
        elif direction == "left": self.x -= 1
        elif direction == "right": self.x += 1
        self.x = max(0, min(COLS - 1, self.x))

    def update(self, camera):
        now = pygame.time.get_ticks()
        if now - self.last_frame > 180:
            self.frame = (self.frame + 1) % len(self.frames)
            self.last_frame = now

    def get_rect(self, camera):
        y = HEIGHT - 120 - (self.y - camera) * CELL
        return self.frames[self.frame].get_rect(topleft=(self.x * CELL + 6, y + 3))

    def draw(self, screen, camera):
        if self.is_alive:
            screen.blit(self.frames[self.frame], self.get_rect(camera))
