import pygame, random
class Particle(pygame.sprite.Sprite):
    def __init__(self,center,color):
        super().__init__(); self.image=pygame.Surface((7,7),pygame.SRCALPHA); pygame.draw.circle(self.image,color,(3,3),3)
        self.rect=self.image.get_rect(center=center); self.dx=random.randint(-4,4); self.dy=random.randint(-6,-1); self.life=28
    def update(self):
        self.rect.x+=self.dx; self.rect.y+=self.dy; self.dy+=1; self.life-=1
        if self.life<=0: self.kill()
