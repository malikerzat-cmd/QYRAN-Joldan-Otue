import pygame, random, os
from settings import WIDTH, HEIGHT, CELL
from player import Player
from vehicle import Car, Truck
from road import RoadLane
from coin import Coin
from particle import Particle

WHITE=(255,255,255); BLACK=(20,20,20); RED=(220,40,40); YELLOW=(255,215,0)
class GameManager:
    def __init__(self):
        self.font=pygame.font.SysFont("arial",25,bold=True); self.big=pygame.font.SysFont("arial",50,bold=True); self.small=pygame.font.SysFont("arial",19)
        self.sounds={}
        if pygame.mixer.get_init():
            for key,name in [("coin","catch.wav"),("hit","hit.wav"),("over","over.wav")]:
                try: self.sounds[key]=pygame.mixer.Sound(os.path.join(os.path.dirname(__file__),"assets",name))
                except (pygame.error,FileNotFoundError): pass
        self.record=self.load_record(); self.state="start"; self.reset_game()
    def play_sound(self,name):
        if name in self.sounds: self.sounds[name].play()
    def load_record(self):
        path=os.path.join(os.path.dirname(__file__),"record.txt")
        try:
            with open(path) as f: return int(f.read())
        except (OSError,ValueError): return 0
    def save_record(self):
        with open(os.path.join(os.path.dirname(__file__),"record.txt"),"w") as f: f.write(str(self.record))
    def reset_game(self):
        self.player=Player(); self.score=0; self.level=1; self.camera=0; self.lanes=[]; self.vehicles=[]; self.coins=[]
        self.effects=pygame.sprite.Group(); self.last_safe_lane=0; self.lanes.append(RoadLane(0))
        for lane in range(1,30): self.add_lane(lane)
    def start(self): self.reset_game(); self.state="play"
    def add_lane(self,lane):
        self.lanes.append(RoadLane(lane))
        if lane%2==0:
            direction=1 if lane%4==0 else -1; count=min(2+self.level//2,5)
            for _ in range(count):
                v=Car(lane,direction,self.level) if random.random()<.7 else Truck(lane,direction,self.level)
                v.x=random.randint(-100,WIDTH); self.vehicles.append(v)
            if random.random()<.4: self.coins.append(Coin(lane))
    def add_score(self,value):
        self.score+=value
        if self.score>self.record: self.record=self.score; self.save_record()
        new_level=self.score//5+1
        if new_level>self.level:
            self.level=new_level
            for v in self.vehicles: v.speed+=15
    def burst(self,center,color):
        for _ in range(12): self.effects.add(Particle(center,color))
    def check_coin(self):
        for coin in self.coins:
            if not coin.collected and self.player.x==coin.x and self.player.y==coin.lane:
                coin.collected=True; self.add_score(1); self.play_sound("coin")
                y=HEIGHT-120-(coin.lane-self.camera)*CELL; self.burst((coin.x*CELL+30,y+30),YELLOW)
    def check_collision(self):
        player_rect=self.player.get_rect(self.camera).inflate(-12,-12)
        for v in self.vehicles:
            if v.lane==self.player.y and player_rect.colliderect(v.get_rect(self.camera)):
                self.burst(player_rect.center,(240,65,45)); self.play_sound("hit"); self.end_game(); return
    def end_game(self):
        self.state="over"; self.player.is_alive=False; self.play_sound("over")
    def update(self,dt):
        self.effects.update()
        if self.state!="play": return
        self.player.update(self.camera)
        for v in self.vehicles: v.update(dt)
        self.check_collision(); self.check_coin()
        if self.player.y>self.camera+4: self.camera=self.player.y-4
        highest=max(l.number for l in self.lanes)
        while highest<self.player.y+20: highest+=1; self.add_lane(highest)
        self.vehicles=[v for v in self.vehicles if v.lane>self.camera-3]
        self.coins=[c for c in self.coins if c.lane>self.camera-3]
    def draw_text(self,screen,text,font,color,y):
        surf=font.render(text,True,color); screen.blit(surf,(WIDTH//2-surf.get_width()//2,y))
    def draw(self,screen):
        screen.fill((50,150,65))
        for lane in self.lanes: lane.draw(screen,self.camera)
        for coin in self.coins: coin.draw(screen,self.camera)
        for v in self.vehicles: v.draw(screen,self.camera)
        self.player.draw(screen,self.camera)
        self.effects.draw(screen)
        if self.state=="start":
            self.draw_overlay(screen); self.draw_text(screen,"QYRAN",self.big,YELLOW,220); self.draw_text(screen,"ЖОЛДАН ӨТУ",self.font,WHITE,290); self.draw_text(screen,"Бастау: SPACE",self.font,WHITE,370); self.draw_text(screen,"Қозғалыс: WASD немесе бағыт пернелері",self.small,WHITE,415)
        elif self.state=="play":
            pygame.draw.rect(screen,BLACK,(0,0,WIDTH,55))
            for i,t in enumerate([f"Ұпай: {self.score}",f"Рекорд: {self.record}",f"Деңгей: {self.level}"]): screen.blit(self.small.render(t,True,WHITE),(10+i*200,17))
        else:
            self.draw_overlay(screen); self.draw_text(screen,"ОЙЫН АЯҚТАЛДЫ",self.big,RED,250); self.draw_text(screen,f"Ұпай: {self.score}",self.font,WHITE,330); self.draw_text(screen,"R - Қайта бастау",self.font,YELLOW,390); self.draw_text(screen,"ESC - Шығу",self.small,WHITE,435)
    def draw_overlay(self,screen):
        overlay=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA); overlay.fill((0,0,0,185)); screen.blit(overlay,(0,0))
