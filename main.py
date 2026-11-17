import pygame, sys
from settings import WIDTH, HEIGHT, FPS
from game import GameManager

def main():
    pygame.init()
    try: pygame.mixer.init()
    except pygame.error: pass
    screen=pygame.display.set_mode((WIDTH,HEIGHT)); pygame.display.set_caption("QYRAN - Жолдан өту")
    clock=pygame.time.Clock(); game=GameManager(); running=True
    while running:
        dt=min(clock.tick(FPS)/1000,0.05)
        for event in pygame.event.get():
            if event.type==pygame.QUIT: running=False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: running=False
                elif game.state=="start" and event.key in (pygame.K_SPACE,pygame.K_RETURN): game.start()
                elif game.state=="over" and event.key==pygame.K_r: game.start()
                elif game.state=="play":
                    if event.key in (pygame.K_UP,pygame.K_w): game.player.move("up")
                    elif event.key in (pygame.K_DOWN,pygame.K_s): game.player.move("down")
                    elif event.key in (pygame.K_LEFT,pygame.K_a): game.player.move("left")
                    elif event.key in (pygame.K_RIGHT,pygame.K_d): game.player.move("right")
                    if game.player.y>=game.last_safe_lane+5:
                        game.add_score(1); game.last_safe_lane+=5
                    game.check_coin(); game.check_collision()
        game.update(dt); game.draw(screen); pygame.display.flip()
    pygame.quit(); sys.exit()
if __name__=="__main__": main()
