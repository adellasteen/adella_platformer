
import pygame, sys
from pygame.locals import *
import random 
vec = pygame.math.Vector2
ACC = 0.5

FRIC = -0.12
pygame.init()
width = 400
height = 300
f = pygame.font.SysFont("Arial",16)
DISPLAYSURF = pygame.display.set_mode((400, 300))

framePerTick = pygame.time.Clock()
fps = 60
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30,30))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect()
        self.acc = vec(0,0)
        self.vel = vec(0,0)
        self.pos = vec(width/2,height)
        self.score = 0
    def move(self):
        self.acc = vec(0,ACC)
        keys = pygame.key.get_pressed()
        if keys[pygame.locals.K_LEFT]:
            self.acc.x = -ACC
        if keys[pygame.locals.K_RIGHT]:
            self.acc.x = ACC


        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc 
      

        if self.pos.x < -15:
            self.pos.x = width+15 
        if self.pos.x > width+15:
            self.pos.x = -15
            
        self.rect.midbottom = self.pos 

    def update(self,platforms):
        hits = pygame.sprite.spritecollide(self,platforms,False)
        if hits:
            if p1.rect.center[1] <= hits[0].rect.top:
                self.vel.y = 0
                self.pos.y = hits[0].rect.top+1
                self.score += hits[0].point
                hits[0].point = 0

    def jump(self,platforms):
        if pygame.sprite.spritecollideany(self,platforms):
            self.vel.y = -15

    def canceljump(self):
        if self.vel.y < -5:
            self.vel.y = -5




class Platform(pygame.sprite.Sprite):

    def __init__(self) :
        super().__init__()
        self.surf = pygame.Surface((random.randint(30,50),12 ))
        self.surf.fill((24,55,189))
        self.rect=self.surf.get_rect(center=(random.randint(0,width),random.randint(0,height)))
        self.point = 1
    def move(self):
        pass 
    def update (self,group):
        if self.point == 0:
            self.surf.fill((200,0,0))

def platgen():
   while len(platforms)< 7:
        p = Platform()
        p.rect = p.surf.get_rect(center=(random.randint(0,width),random.randint(-50,0)))
        if check(p, platforms):
            all_sprites.add(p)
            platforms.add(p)

def check(p, Platforms):
    if pygame.sprite.spritecollideany(p,Platforms):
        return False 
    for plt in Platforms:
        if abs(p.rect.top - plt.rect.bottom ) < 40 and abs(plt.rect.top - p.rect.bottom) < 40:
            return False
    return True

    
p1 = None           
pt1 = None
all_sprites = None
platforms = None
playing = None 
flashcounter= None
def startgame():
    global p1
    global pt1
    global all_sprites
    global platforms
    global playing
    global flashcounter
    flashcounter = 0
    p1 = Player()
    pt1 = Platform()
    playing = True
    pt1.surf = pygame.Surface((width,20))
    pt1.surf.fill((24,55,189))
    pt1.rect=pt1.surf.get_rect(top=height-10)



    all_sprites= pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    all_sprites.add(p1)
    all_sprites.add(pt1)
    platforms.add(pt1)
    counter=0
    while  counter <7:
        p=Platform()

        if check(p,platforms): 
            all_sprites.add(p)
            platforms.add(p)
            counter += 1


        

pygame.display.set_caption('Platformer')
color=0
startgame()
while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == pygame.locals.K_UP:
                p1.jump(platforms)
        if event.type == QUIT:
            print (event)
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == pygame.locals.K_UP:
                p1.canceljump()
    if playing:
        if p1.rect.top <= height/3:  
            p1.pos.y += abs(p1.vel.y) 
            for plat in platforms:
                plat.rect.y += abs(p1.vel.y) 
                if plat.rect.top >= height:
                    plat.kill()  
        if p1.rect.top >= height:
            playing = False

        platgen()
        DISPLAYSURF.fill((0,0,0))
        for spr in all_sprites:
            DISPLAYSURF.blit(spr.surf,spr.rect)
            spr.move()
            spr.update(platforms)
        
        scoresurf = f.render(str(p1.score),True,(255,255,255))
        DISPLAYSURF.blit(scoresurf,(width/2,10))
    else:
        if flashcounter > 180:
            startgame()
        else:
            if DISPLAYSURF.get_at ((0,0)).r == 0:
                 DISPLAYSURF.fill((255,0,0))
            else:
                DISPLAYSURF.fill((0,0,0))
            flashcounter += 1
    pygame.display.update()
    framePerTick.tick(fps)






