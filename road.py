import pygame
from settings import WIDTH, HEIGHT, CELL
GREEN=(50,150,65); DARK_GREEN=(30,100,40); ROAD=(55,55,60); WHITE=(245,245,245)
class RoadLane:
    def __init__(self, number): self.number=number; self.is_road=number>0 and number%2==0
    def draw(self, screen, camera):
        y=HEIGHT-120-(self.number-camera)*CELL
        if y < -CELL or y > HEIGHT: return
        if self.is_road:
            pygame.draw.rect(screen, ROAD, (0,y,WIDTH,CELL))
            for x in range(0,WIDTH,90): pygame.draw.rect(screen,WHITE,(x,y+29,40,3))
        else:
            pygame.draw.rect(screen,GREEN,(0,y,WIDTH,CELL))
            for x in range(20,WIDTH,80): pygame.draw.circle(screen,DARK_GREEN,(x,y+20),4)
