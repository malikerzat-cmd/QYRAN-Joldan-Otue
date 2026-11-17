import pygame, random
from settings import WIDTH, HEIGHT, CELL, COLS
class Coin:
    def __init__(self,lane): self.x=random.randint(0,COLS-1); self.lane=lane; self.collected=False
    def get_rect(self,camera):
        y=HEIGHT-120-(self.lane-camera)*CELL
        return pygame.Rect(self.x*CELL+18,int(y+18),24,24)
    def draw(self,screen,camera):
        if not self.collected:
            r=self.get_rect(camera)
            if -30<r.y<HEIGHT+30:
                pygame.draw.circle(screen,(255,215,0),r.center,13)
                pygame.draw.circle(screen,(240,140,20),r.center,8,2)
