import pygame, math, sys, random, time
from pygame.locals import *


class player(object):

    def __init__(self, x, y, width, height, vel, life):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.checkJump = False
        self.jumpCalc = 6
        self.move = False

        self.lface = False
        self.rface = True
        self.uface = False
        self.dface = False

        self.left = False
        self.right = False
        self.up = False
        self.down = False

        self.slash = False
        self.slashCount = 0
        self.hit = 0
        self.nov = 0
        self.novAttack = 0
        self.noz = 0
        self.nozAttack = 0
        self.walkCount = 0

        self.follow = True
        self.life = life
        self.sick = False
        self.dead = False
        self.incHealth = 0
        self.levelFinish = False
        self.wsCount = 0
    
        self.virusKilled = 0
        self.bossKilled = False

        self.saber = pygame.mixer.Sound('sounds/saber.wav')
        self.walk = [pygame.mixer.Sound('sounds/mwalk1.wav'), pygame.mixer.Sound('sounds/mwalk2.wav')]
        self.jump = pygame.mixer.Sound('sounds/jump.wav')

        self.walkRight = [pygame.image.load('sprites/Angel/27.png'), pygame.image.load('sprites/Angel/28.png'), pygame.image.load('sprites/Angel/29.png'), pygame.image.load('sprites/Angel/30.png'), pygame.image.load('sprites/Angel/31.png'), pygame.image.load('sprites/Angel/32.png'), pygame.image.load('sprites/Angel/33.png'), pygame.image.load('sprites/Angel/34.png'), pygame.image.load('sprites/Angel/35.png')]
        self.walkLeft = [pygame.image.load('sprites/Angel/9.png'), pygame.image.load('sprites/Angel/10.png'), pygame.image.load('sprites/Angel/11.png'), pygame.image.load('sprites/Angel/12.png'), pygame.image.load('sprites/Angel/13.png'), pygame.image.load('sprites/Angel/14.png'), pygame.image.load('sprites/Angel/15.png'), pygame.image.load('sprites/Angel/16.png'), pygame.image.load('sprites/Angel/17.png')]
        self.walkUp = [pygame.image.load('sprites/Angel/0.png'), pygame.image.load('sprites/Angel/1.png'), pygame.image.load('sprites/Angel/2.png'), pygame.image.load('sprites/Angel/3.png'), pygame.image.load('sprites/Angel/4.png'), pygame.image.load('sprites/Angel/5.png'), pygame.image.load('sprites/Angel/6.png'), pygame.image.load('sprites/Angel/7.png'), pygame.image.load('sprites/Angel/8.png')]
        self.walkDown = [pygame.image.load('sprites/Angel/18.png'), pygame.image.load('sprites/Angel/19.png'), pygame.image.load('sprites/Angel/20.png'), pygame.image.load('sprites/Angel/21.png'), pygame.image.load('sprites/Angel/22.png'), pygame.image.load('sprites/Angel/23.png'), pygame.image.load('sprites/Angel/24.png'), pygame.image.load('sprites/Angel/25.png'), pygame.image.load('sprites/Angel/26.png')]
        
        self.slashRight = [pygame.image.load('sprites/Angel/54.png'), pygame.image.load('sprites/Angel/56.png'), pygame.image.load('sprites/Angel/57.png'), pygame.image.load('sprites/Angel/58.png'), pygame.image.load('sprites/Angel/59.png')] 
        self.slashLeft = [pygame.image.load('sprites/Angel/42.png'), pygame.image.load('sprites/Angel/44.png'), pygame.image.load('sprites/Angel/45.png'), pygame.image.load('sprites/Angel/46.png'), pygame.image.load('sprites/Angel/47.png')] 
        self.slashUp = [pygame.image.load('sprites/Angel/36.png'), pygame.image.load('sprites/Angel/38.png'), pygame.image.load('sprites/Angel/39.png'), pygame.image.load('sprites/Angel/40.png'), pygame.image.load('sprites/Angel/41.png')] 
        self.slashDown = [pygame.image.load('sprites/Angel/48.png'), pygame.image.load('sprites/Angel/50.png'), pygame.image.load('sprites/Angel/51.png'), pygame.image.load('sprites/Angel/52.png'), pygame.image.load('sprites/Angel/53.png')] 
        
        self.lc = pygame.image.load('sprites/Angel/9.png')
        self.rc = pygame.image.load('sprites/Angel/27.png') 
        self.uc = pygame.image.load('sprites/Angel/0.png')
        self.dc = pygame.image.load('sprites/Angel/18.png')

    def update(self, screen, virusAttack, zAttack, gSound):
        
        if (self.life+self.incHealth) <= 0:
            self.dead = True
       
        if virusAttack:
            self.life -= 0.5 * self.nov
        
        if zAttack:
            self.life -= 1 * self.noz
        
        if not self.sick:
            self.blood = (255, 0, 0)
        else:
            self.blood = (164, 203, 110)
            self.life -= 0.10

        pygame.draw.line(screen, self.blood, (10, 53), (10 + (((100+self.incHealth)/(100 + self.incHealth))*(self.life + self.incHealth)), 53), 6)
        pygame.draw.rect(screen, (250, 250, 250), (10, 50, 102+self.incHealth, 8), 2) 

        self.angelBlade = pygame.Rect(0, 0, 0, 0)
        
        if self.walkCount + 1 > 9:
            self.walkCount = 0
        
        if gSound:
            if self.wsCount + 1 > 2:
                self.wsCount = 0
        
            if self.move and not self.checkJump:
                if self.walkCount + 1 == 1: 
                    pygame.mixer.Sound.play(self.walk[self.wsCount])
                    self.wsCount += 1 

        if self.left:
            if self.lface and self.slash:
                screen.blit(self.slashLeft[self.slashCount], (self.x - 80, self.y - 70))
                self.angelBlade = pygame.Rect(self.x - 62, self.y + 5, self.width + 28, self.height - 15)
                
            else: 
                if self.checkJump:
                    self.x -= 4
                screen.blit(self.walkLeft[self.walkCount], (self.x, self.y))
                self.walkCount += 1

        elif self.right:
            if self.rface and self.slash:
                screen.blit(self.slashRight[self.slashCount], (self.x - 80, self.y - 70))
                self.angelBlade = pygame.Rect(self.x + 34, self.y + 5, self.width + 28, self.height - 15)

            else:
                if self.checkJump and self.x <= 800 - (self.width + 5): 
                    self.x += 4  
                screen.blit(self.walkRight[self.walkCount], (self.x, self.y))
                self.walkCount += 1
          
        elif self.up:
            if self.uface and self.slash:
                screen.blit(self.slashUp[self.slashCount], (self.x - 80, self.y - 70))
                self.angelBlade = pygame.Rect(self.x - 25, self.y - 15, self.width + 50, self.height - 25)

            else:
                screen.blit(self.walkUp[self.walkCount], (self.x, self.y))
                self.walkCount += 1

        elif self.down:
            if self.dface and self.slash:
                screen.blit(self.slashDown[self.slashCount], (self.x - 80, self.y - 70))
                self.angelBlade = pygame.Rect(self.x - 25, self.y + 40, self.width + 50, self.height - 25)

            else:
                screen.blit(self.walkDown[self.walkCount], (self.x, self.y))          
                self.walkCount += 1
            
        else:
            if self.lface:
                if self.slash:
                    screen.blit(self.slashLeft[self.slashCount], (self.x - 80, self.y - 70))
                    self.angelBlade = pygame.Rect(self.x - 62, self.y + 5, self.width + 28, self.height - 15)
                else:
                    screen.blit(self.lc, (self.x, self.y))

            elif self.rface:
                if self.slash:
                    screen.blit(self.slashRight[self.slashCount], (self.x - 80, self.y - 70))
                    self.angelBlade = pygame.Rect(self.x + 34, self.y + 5, self.width + 28, self.height - 15)
                else:
                    screen.blit(self.rc, (self.x, self.y)) 
                 
            elif self.uface:
                if self.slash:
                    screen.blit(self.slashUp[self.slashCount], (self.x - 80, self.y - 70))
                    self.angelBlade = pygame.Rect(self.x - 25, self.y - 15, self.width + 50, self.height - 25)
                else:
                    screen.blit(self.uc, (self.x, self.y))

            else:
                if self.slash:
                    screen.blit(self.slashDown[self.slashCount], (self.x - 80, self.y - 70))    
                    self.angelBlade = pygame.Rect(self.x - 25, self.y + 40, self.width + 50, self.height - 25)
                else:
                    screen.blit(self.dc, (self.x, self.y))
        
        keys = pygame.key.get_pressed()
        self.kdata = []
        gfile = open('Config/config.txt', 'r')
        for i in range(9):
            self.kdata.append(gfile.readline())

        if keys[int(self.kdata[2])]:
            self.left = True
            self.right = False
            self.up = False
            self.down = False
            self.lface = True
            self.rface = False
            self.uface = False
            self.dface = False
            self.move = True

            if self.x > 5:

                if keys[pygame.K_UP] and self.y > (self.height + 220):
                    self.x -= self.vel * 0.5
                    self.y -= self.vel * 0.5
                    
                elif keys[pygame.K_DOWN] and self.y < 600 - (self.height + 5):    
                    self.x -= self.vel * 0.5
                    self.y += self.vel * 0.5
                    
                else:
                    self.x -= self.vel
                
        elif keys[int(self.kdata[3])]:
            self.left = False
            self.right = True
            self.up = False
            self.down = False
            self.lface = False
            self.rface = True
            self.uface = False
            self.dface = False
            self.move = True
            if not self.levelFinish:
                if self.x < 800 - (self.width + 5):

                    if keys[pygame.K_UP] and self.y > (self.height + 220):
                        self.x += self.vel * 0.5
                        self.y -= self.vel * 0.5
                        
                    elif keys[pygame.K_DOWN] and self.y < 600 - (self.height + 5):    
                        self.x += self.vel * 0.5 
                        self.y += self.vel * 0.5
                        
                    else:
                        self.x += self.vel

            else:
                if keys[pygame.K_UP] and self.y > (self.height + 220):
                    self.x += self.vel * 0.5
                    self.y -= self.vel * 0.5
                    
                elif keys[pygame.K_DOWN] and self.y < 600 - (self.height + 5):    
                    self.x += self.vel * 0.5 
                    self.y += self.vel * 0.5
                    
                else:
                    self.x += self.vel

        elif keys[int(self.kdata[0])]:
            self.up = True
            self.down = False
            self.left = False
            self.right = False
            self.lface = False
            self.rface = False
            self.uface = True
            self.dface = False
            self.move = True
            
            if self.y > (self.height + 220): 
                self.y -= self.vel

        elif keys[int(self.kdata[1])]:    
            self.up = False
            self.down = True
            self.left = False
            self.right = False
            self.lface = False
            self.rface = False
            self.uface = False
            self.dface = True
            self.move = True
        
            if self.y < 600 - (self.height + 5):
                self.y += self.vel
            
        else:
            self.right = False
            self.left = False
            self.up = False
            self.down = False
            self.walkCount = 0
            self.move = False
            self.wsCount = 0

        if not self.checkJump:

            if keys[int(self.kdata[5])]:
                if gSound:
                    pygame.mixer.Sound.play(self.jump)
                self.checkJump = True
                self.right = False
                self.left = False
                self.up = False
                self.down = False
                self.walkCount = 0
            
        else:
            if self.jumpCalc >= -6:
                jumper = 0.5 * self.jumpCalc
                
                if self.jumpCalc < 0:
                    jumper = -0.5 * self.jumpCalc

                self.y -= self.jumpCalc * jumper 
                self.jumpCalc -= 1
                if self.x < (self.width - 25):
                    self.x = (self.width - 25)
                if self.x > 800 - (self.width + 5) and not self.levelFinish:
                    self.x = 800 - (self.width + 5)
                if self.y > 600 - (self.height + 5):
                    self.y = 600 - (self.height + 5)
            else:
                self.checkJump = False
                self.jumpCalc = 6
     
        if not self.slash:
            if keys[int(self.kdata[4])]:
                self.slash = True
                if gSound:
                    pygame.mixer.Sound.play(self.saber)
        else:
            if self.slashCount < 4:
                self.slashCount += 1
            else:
                self.slash = False
                self.slashCount = 0

        if keys[int(self.kdata[6])]:
            self.vel = 8
        else:
            self.vel = 4

class crush(object):    
    def __init__(self, x, y, width, height, vel, life):
        
        self.life = life
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.move = False

        self.left = False
        self.right = False
        self.up = False
        self.down = False

        self.lface = False
        self.rface = False
        self.uface = False
        self.dface = False

        self.walkCount = 0
        self.wsCount = 0
        self.heal = False
        self.attacked = False
        self.dead = False
        
        self.walk = [pygame.mixer.Sound('sounds/fwalk1.wav'), pygame.mixer.Sound('sounds/fwalk2.wav')]

        self.walkRight = [pygame.image.load('sprites/Crush/27.png'), pygame.image.load('sprites/Crush/28.png'), pygame.image.load('sprites/Crush/29.png'), pygame.image.load('sprites/Crush/30.png'), pygame.image.load('sprites/Crush/31.png'), pygame.image.load('sprites/Crush/32.png'), pygame.image.load('sprites/Crush/33.png'), pygame.image.load('sprites/Crush/34.png'), pygame.image.load('sprites/Crush/35.png')]
        self.walkLeft = [pygame.image.load('sprites/Crush/9.png'), pygame.image.load('sprites/Crush/10.png'), pygame.image.load('sprites/Crush/11.png'), pygame.image.load('sprites/Crush/12.png'), pygame.image.load('sprites/Crush/13.png'), pygame.image.load('sprites/Crush/14.png'), pygame.image.load('sprites/Crush/15.png'), pygame.image.load('sprites/Crush/16.png'), pygame.image.load('sprites/Crush/17.png')]
        self.walkUp = [pygame.image.load('sprites/Crush/0.png'), pygame.image.load('sprites/Crush/1.png'), pygame.image.load('sprites/Crush/2.png'), pygame.image.load('sprites/Crush/3.png'), pygame.image.load('sprites/Crush/4.png'), pygame.image.load('sprites/Crush/5.png'), pygame.image.load('sprites/Crush/6.png'), pygame.image.load('sprites/Crush/7.png'), pygame.image.load('sprites/Crush/8.png')]
        self.walkDown = [pygame.image.load('sprites/Crush/18.png'), pygame.image.load('sprites/Crush/19.png'), pygame.image.load('sprites/Crush/20.png'), pygame.image.load('sprites/Crush/21.png'), pygame.image.load('sprites/Crush/22.png'), pygame.image.load('sprites/Crush/23.png'), pygame.image.load('sprites/Crush/24.png'), pygame.image.load('sprites/Crush/25.png'), pygame.image.load('sprites/Crush/26.png')]

    def update(self, screen, angelx, angely, angelcheckJump, angelfollow, gSound):

        pygame.draw.line(screen, (255, 0, 0), (10, 119), (10 + ((100/100)*self.life), 119), 6)
        pygame.draw.rect(screen, (255, 255, 255), (10, 116, 102, 8), 2)

        self.crushPos = pygame.Rect(self.x, self.y, self.width, self.height)
        self.heal = False

        if angelfollow:
            if self.walkCount + 1 > 9:
                self.walkCount = 0

            if gSound:
                if self.wsCount + 1 > 2:
                    self.wsCount = 0

                if self.move:
                    if self.walkCount + 1 == 3: 
                        pygame.mixer.Sound.play(self.walk[self.wsCount])
                        self.wsCount += 1
            
            if self.left:
                screen.blit(self.walkLeft[self.walkCount], (self.x, self.y))
                self.walkCount += 1       
                self.lface = True
                self.rface = False
                self.uface = False
                self.dface = False
                self.move = True
                
            elif self.right:    
                screen.blit(self.walkRight[self.walkCount], (self.x, self.y))
                self.walkCount += 1
                self.rface = True
                self.lface = False
                self.uface = False
                self.dface = False
                self.move = True

            elif self.up:    
                screen.blit(self.walkUp[self.walkCount], (self.x, self.y))
                self.walkCount += 1
                self.uface = True
                self.lface = False
                self.rface = False
                self.dface = False
                self.move = True

            elif self.down:
                screen.blit(self.walkDown[self.walkCount], (self.x, self.y))
                self.walkCount += 1
                self.dface = True
                self.lface = False
                self.rface = False
                self.uface = False
                self.move = True

            else:
                self.move = False
                self.wsCount = 0

                if self.lface:
                    screen.blit(self.walkLeft[0], (self.x, self.y))
                elif self.rface:
                    screen.blit(self.walkRight[0], (self.x, self.y))
                elif self.uface:
                    screen.blit(self.walkUp[0], (self.x, self.y))
                else:
                    screen.blit(self.walkDown[0], (self.x, self.y))

            if self.x > angelx and self.y > angely:
                if angelcheckJump:
                    self.x -= self.vel
                else:
                    self.x -= self.vel * 0.5
                    self.y -= self.vel * 0.5
                self.left = True
                self.right = False
                self.up = False
                self.down = False

            elif self.x > angelx and self.y < angely:       
                if angelcheckJump:
                    self.x -= self.vel
                else:
                    self.x -= self.vel * 0.5
                    self.y += self.vel * 0.5
                self.left = True
                self.right = False
                self.up = False
                self.down = False

            elif self.x > angelx+10 and self.y == angely:
                self.x -= self.vel
                self.left = True
                self.right = False
                self.up = False
                self.down = False
                
            elif self.x < angelx and self.y > angely:
                if angelcheckJump:
                    self.x += self.vel
                else:
                    self.x += self.vel * 0.5
                    self.y -= self.vel * 0.5
                self.left = False
                self.right = True
                self.up = False
                self.down = False

            elif self.x < angelx and self.y < angely:
                if angelcheckJump:
                    self.x += self.vel
                else:
                    self.x += self.vel * 0.5
                    self.y += self.vel * 0.5 
                self.left = False
                self.right = True
                self.up = False
                self.down = False
                
            elif self.x < angelx-10 and  self.y == angely:
                self.x += self.vel
                self.left = False
                self.right = True
                self.up = False
                self.down = False
                
            elif self.x == angelx and self.y > angely+10:
                self.y -= self.vel
                self.up = True
                self.right = False
                self.left = False
                self.right = False
            elif self.x == angelx and self.y < angely-10:
                self.y += self.vel
                self.up = False
                self.down = True
                self.left = False
                self.right = False

            else:
                self.heal = True
                self.up = False
                self.down = False
                self.left = False
                self.right = False
            
        else:
            if self.lface:
                screen.blit(self.walkLeft[0], (self.x, self.y))
            elif self.rface:
                screen.blit(self.walkRight[0], (self.x, self.y))
            elif self.uface:
                screen.blit(self.walkUp[0], (self.x, self.y))
            else:
                screen.blit(self.walkDown[0], (self.x, self.y))

class viruses(object):    
    def __init__(self, x, y, width, height, vel, life, move):
        
        self.alive = True
        self.life = life
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel

        self.move = False
        self.moveCount = 0
        self.attack = False
        self.attacked = False

        self.moveVirus = move
                  
    def update(self, screen, angelx, angely, angelcheckJump):
        
        self.attack = False

        pygame.draw.line(screen, (255, 0, 0), (self.x, self.y-5), ((self.x) + ((self.width/100)*(self.life)), self.y-5), 4)
        if self.moveCount + 1 > 16:
            self.moveCount = 0
            
        if self.move:
            screen.blit(self.moveVirus[self.moveCount//8], (self.x + ((self.moveCount//8)*2), self.y))
            self.moveCount += 1       
                
        self.virusPos = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.x > angelx and self.y > angely:
            if angelcheckJump:
                self.x -= self.vel
            else:
                self.x -= self.vel * 0.5
                self.y -= self.vel * 0.5
            self.move = True

        elif self.x > angelx and self.y < angely:       
            if angelcheckJump:
                self.x -= self.vel
            else:
                self.x -= self.vel * 0.5
                self.y += self.vel * 0.5
            self.move = True

        elif self.x > angelx + 18 and self.y == angely:
            self.x -= self.vel
            self.move = True
            
        elif self.x < angelx and self.y > angely:
            if angelcheckJump:
                self.x += self.vel
            else:
                self.x += self.vel * 0.5
                self.y -= self.vel * 0.5
            self.move = True

        elif self.x < angelx and self.y < angely:
            if angelcheckJump:
                self.x += self.vel
            else:
                self.x += self.vel * 0.5
                self.y += self.vel * 0.5 
            self.move = True
                
        elif self.x < angelx - (self.width - 18) and  self.y == angely:
            self.x += self.vel
            self.move = True
                
        elif self.x == angelx and self.y > angely + 18:
            self.y -= self.vel
            self.move = True

        elif self.x == angelx and self.y < angely - 16:
            self.y += self.vel
            self.move = True

        else:
            self.attack = True

class mainBoss(object):    
    def __init__(self, x, y, width, height, vel, life, move):
        
        self.alive = True
        self.life = life
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel

        self.move = False

        self.moveCount = 0
        self.attack = False
        self.attacked = False
        self.mbAttack = False
        self.boss = False

        self.healCount = 0
        self.moveVirus = move
                  
    def update(self, screen, angelx, angely, angelcheckJump):
        
        pygame.draw.line(screen, (255, 0, 0), (self.x, self.y-5), ((self.x) + ((self.width/1000)*(self.life)), self.y-5), 4)
        
        if self.moveCount + 1 > 72:
            self.moveCount = 0
            
        if self.move:
            screen.blit(self.moveVirus[self.moveCount//4], (self.x + ((self.moveCount//36)*2), self.y))
            self.moveCount += 1      
            
        self.virusPos = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.life > 0 and self.life < 600:

            if self.move:
                self.healCount += 1

            if self.healCount <= 30000:
                self.life += 0.05
                self.healCount = 0

        self.mbAttack = False

        if self.x > angelx and self.y > angely-16:
            if angelcheckJump:
                self.x -= self.vel
            else:
                self.x -= self.vel * 0.5
                self.y -= self.vel * 0.5
            self.move = True

        elif self.x > angelx and self.y < angely-16: 
            if angelcheckJump:
                self.x -= self.vel
            else:      
                self.x -= self.vel * 0.5
                self.y += self.vel * 0.5
            self.move = True

        elif self.x > angelx + 18 and self.y == angely-16:
            self.x -= self.vel
            self.move = True
                
        elif self.x < angelx and self.y > angely-16:
            if angelcheckJump:
                self.x += self.vel
            else:
                self.x += self.vel * 0.5
                self.y -= self.vel * 0.5
            self.move = True

        elif self.x < angelx and self.y < angely-16:
            if angelcheckJump:
                self.x += self.vel
            else:    
                self.x += self.vel * 0.5
                self.y += self.vel * 0.5 
            self.move = True
                

        elif self.x < angelx - 64 and  self.y == angely-16:
            self.x += self.vel
            self.move = True
                
        elif self.x == angelx and self.y > angely + 28:
            self.y -= self.vel
            self.move = True

        elif self.x == angelx and self.y < angely - 16:
            self.y += self.vel
            self.move = True

        else:
            self.mbAttack = True
            
class zombies(object):
    def __init__(self, x, y, width, height, vel, life):
        
        self.alive = True
        self.life = life
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.move = False

        self.left = False
        self.right = False
        self.up = False
        self.down = False

        self.walkCount = 0
        self.wsCount = 0
        self.attack = False
        self.attacked = False
        self.growl = 0
        self.grst = 0
        self.grwlCount = 0

        self.walk = [pygame.mixer.Sound('sounds/zwalk1.wav'), pygame.mixer.Sound('sounds/zwalk2.wav')]
        self.voices = [pygame.mixer.Sound('sounds/growl1.wav'), pygame.mixer.Sound('sounds/growl2.wav'), pygame.mixer.Sound('sounds/growl3.wav'), pygame.mixer.Sound('sounds/growl4.wav')] 
        
        self.walkRight = [pygame.image.load('sprites/Zombies/27.png'), pygame.image.load('sprites/Zombies/28.png'), pygame.image.load('sprites/Zombies/29.png'), pygame.image.load('sprites/Zombies/30.png'), pygame.image.load('sprites/Zombies/31.png'), pygame.image.load('sprites/Zombies/32.png'), pygame.image.load('sprites/Zombies/33.png'), pygame.image.load('sprites/Zombies/34.png'), pygame.image.load('sprites/Zombies/35.png')]
        self.walkLeft = [pygame.image.load('sprites/Zombies/9.png'), pygame.image.load('sprites/Zombies/10.png'), pygame.image.load('sprites/Zombies/11.png'), pygame.image.load('sprites/Zombies/12.png'), pygame.image.load('sprites/Zombies/13.png'), pygame.image.load('sprites/Zombies/14.png'), pygame.image.load('sprites/Zombies/15.png'), pygame.image.load('sprites/Zombies/16.png'), pygame.image.load('sprites/Zombies/17.png')]
        self.walkUp = [pygame.image.load('sprites/Zombies/0.png'), pygame.image.load('sprites/Zombies/1.png'), pygame.image.load('sprites/Zombies/2.png'), pygame.image.load('sprites/Zombies/3.png'), pygame.image.load('sprites/Zombies/4.png'), pygame.image.load('sprites/Zombies/5.png'), pygame.image.load('sprites/Zombies/6.png'), pygame.image.load('sprites/Zombies/7.png'), pygame.image.load('sprites/Zombies/8.png')]
        self.walkDown = [pygame.image.load('sprites/Zombies/18.png'), pygame.image.load('sprites/Zombies/19.png'), pygame.image.load('sprites/Zombies/20.png'), pygame.image.load('sprites/Zombies/21.png'), pygame.image.load('sprites/Zombies/22.png'), pygame.image.load('sprites/Zombies/23.png'), pygame.image.load('sprites/Zombies/24.png'), pygame.image.load('sprites/Zombies/25.png'), pygame.image.load('sprites/Zombies/26.png')]

    def update(self, screen, angelx, angely, angelcheckJump, gSound):

        pygame.draw.line(screen, (255, 0, 0), (self.x, self.y-5), (self.x + ((self.width/100)*self.life), self.y-5), 4)
        self.zombiePos = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.walkCount + 1 > 9:
            self.walkCount = 0

        if gSound:
            if self.wsCount + 1 > 2:
                self.wsCount = 0
            
            if self.growl+1 >= 10:
                self.growl = 0
                self.grst += 1

            if self.grwlCount >= 9:
                self.grwlCount = 0

            if self.grst + 1 > 4:
                self.grst = 0
            

            if self.move:
                if self.walkCount + 1 == 1: 
                    pygame.mixer.Sound.play(self.walk[self.wsCount])
                    self.wsCount += 1
                    self.growl += 1
            

            if self.life >= 85 and self.growl == 1:
                self.grwlCount += 1
                if self.grwlCount == 8:
                    pygame.mixer.Sound.play(self.voices[self.grst]) 

        if self.left:
            self.move = True
            screen.blit(self.walkLeft[self.walkCount], (self.x, self.y))
            self.walkCount += 1       
            if self.attacked:
                if self.life !=0 and self.life%10 == 0:
                    self.x += 4
            
        
        elif self.right:    
            self.move = True
            screen.blit(self.walkRight[self.walkCount], (self.x, self.y))
            self.walkCount += 1
            if self.attacked:
                if self.life !=0 and self.life%10 == 0:
                    self.x -= 4

        elif self.up:   
            self.move = True 
            screen.blit(self.walkUp[self.walkCount], (self.x, self.y))
            self.walkCount += 1
            if self.attacked:
                if self.life !=0 and self.life%10 == 0:
                    self.y -= 4

        else:
            self.move = True
            screen.blit(self.walkDown[self.walkCount], (self.x, self.y))
            self.walkCount += 1
            if self.attacked:
                if self.life !=0 and self.life%10 == 0:
                    self.y += 4
        
        self.attack = False

        if self.x > angelx and self.y > angely:
            if angelcheckJump:
                self.x -= self.vel
            else:
                self.x -= self.vel * 0.5
                self.y -= self.vel * 0.5
            self.left = True
            self.right = False
            self.up = False
            self.down = False

        elif self.x > angelx and self.y < angely:     
            if angelcheckJump:
                self.x -= self.vel
            else:  
                self.x -= self.vel * 0.5
                self.y += self.vel * 0.5
            self.left = True
            self.right = False
            self.up = False
            self.down = False

        elif self.x > angelx + 18 and self.y == angely:
            self.x -= self.vel
            self.left = True
            self.right = False
            self.up = False
            self.down = False
            
        elif self.x < angelx and self.y > angely:
            if angelcheckJump:
                self.x += self.vel
            else:
                self.x += self.vel * 0.5
                self.y -= self.vel * 0.5
            self.left = False
            self.right = True
            self.up = False
            self.down = False

        elif self.x < angelx and self.y < angely:
            if angelcheckJump:
                self.x += self.vel
            else:
                self.x += self.vel * 0.5
                self.y += self.vel * 0.5 
            self.left = False
            self.right = True
            self.up = False
            self.down = False
            

        elif self.x < angelx - 14 and  self.y == angely:
            self.x += self.vel
            self.left = False
            self.right = True
            self.up = False
            self.down = False
            
        elif self.x == angelx and self.y > angely + 18:
            self.y -= self.vel
            self.up = True
            self.right = False
            self.left = False
            self.right = False
        elif self.x == angelx and self.y < angely - 16:
            self.y += self.vel
            self.up = False
            self.down = True
            self.left = False
            self.right = False

        else:
            self.attack = True
            self.move = False

class audio(object):
    def __init__(self):
        self.gameMusic = True
        self.gameSound = True

def toWrite(screen, text, ws, tx, ty):
    text = pygame.font.SysFont("18thCentury", ws).render(text, True, (225, 225, 225))
    screen.blit(text, (tx, ty))

def newGame():
    game()

def game():

    pygame.init()
    pygame.mouse.set_cursor(*pygame.cursors.diamond)
    screenWidth = 800
    screenHeight = 600
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Lucid Dream")        
    pygame.display.set_icon(pygame.image.load('gallery/icon.png'))

    clock = pygame.time.Clock()
    fps = 18
    aud = audio()

    her = pygame.image.load('gallery/utn.png') 
    me = pygame.image.load('gallery/ang.png')
    pse = pygame.image.load('gallery/pause.png')
    
    class cutScenes(object):

        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.black = (0, 0, 0)
            self.white = (230, 230, 230)
            self.red = (200, 54, 46)
            self.blue = (20, 98, 108)
            self.purple = (177, 156, 217)
            self.teal = (32,178,170)
            self.gold = (249, 215, 126)
            self.dist = 300
            self.ad = 0
            self.help = False
            self.dskip = False
            self.power = ""
            self.pressed = False
            self.walk = [pygame.mixer.Sound('sounds/mwalk1.wav'), pygame.mixer.Sound('sounds/mwalk2.wav')]
            self.walk2 = [pygame.mixer.Sound('sounds/fwalk1.wav'), pygame.mixer.Sound('sounds/fwalk2.wav')]
            self.walk3 = [pygame.mixer.Sound('sounds/zwalk1.wav'), pygame.mixer.Sound('sounds/zwalk2.wav')]
            self.next = pygame.mixer.Sound('sounds/next.wav')
            self.next.set_volume(0.3)
            self.loadImg =  pygame.image.load('gallery/grave.png') 
            self.atk = pygame.image.load('gallery/attack.png')
            self.hel = pygame.image.load('gallery/health.png')
            self.rgn = pygame.image.load('gallery/regeneration.png')
            self.dBox = pygame.image.load('gallery/dialogbox.png')
            self.ngel = pygame.font.SysFont("18thCentury", 20).render("- Angel -", True, self.red) 
            self.crsh = pygame.font.SysFont("18thCentury", 20).render("- Crush -", True, self.blue)
            self.sujin = pygame.font.SysFont("18thCentury", 20).render("- Sujin -", True, self.purple)
            self.oldman = pygame.font.SysFont("18thCentury", 20).render("- Oldman -", True, self.teal)
            self.vai = pygame.font.SysFont("18thCentury", 20).render("- Siddarth -", True, self.gold)
            self.evils = pygame.font.SysFont("18thCentury", 20).render("- ??? -", True, self.black)
            self.lc = pygame.image.load('sprites/Angel/9.png')
            self.rc = pygame.image.load('sprites/Angel/27.png')
            self.uc = pygame.image.load('sprites/Angel/0.png') 
            self.cuc = pygame.image.load('sprites/Crush/0.png')
            self.clc = pygame.image.load('sprites/Crush/9.png')
            self.crc = pygame.image.load('sprites/Crush/27.png')
            self.zlc = pygame.image.load('sprites/Zombies/9.png')
            self.zrc = pygame.image.load('sprites/Zombies/27.png')
            self.zuc = pygame.image.load('sprites/Zombies/0.png')
            self.viruscn = pygame.image.load('sprites/COVID19/virus/0.png')
            self.evilexpSet = [pygame.image.load('sprites/Evils/0.png'), pygame.image.load('sprites/Evils/1.png')]
            self.wakeUp = [pygame.image.load('sprites/Angel/60.png'), pygame.image.load('sprites/Angel/61.png'), pygame.image.load('sprites/Angel/62.png'), pygame.image.load('sprites/Angel/63.png'), pygame.image.load('sprites/Angel/64.png')]
            self.expSet = [pygame.image.load('sprites/Angel/a0.png'), pygame.image.load('sprites/Angel/a1.png'), pygame.image.load('sprites/Angel/a2.png'), pygame.image.load('sprites/Angel/a3.png'), pygame.image.load('sprites/Angel/a4.png'), pygame.image.load('sprites/Angel/a5.png'), pygame.image.load('sprites/Angel/a6.png')]
            self.cwakeUp = [pygame.image.load('sprites/Crush/36.png'), pygame.image.load('sprites/Crush/37.png'), pygame.image.load('sprites/Crush/38.png'), pygame.image.load('sprites/Crush/39.png'), pygame.image.load('sprites/Crush/40.png'), pygame.image.load('sprites/Crush/41.png')]
            self.cexpSet = [pygame.image.load('sprites/Crush/u0.png'), pygame.image.load('sprites/Crush/u1.png'), pygame.image.load('sprites/Crush/u2.png'), pygame.image.load('sprites/Crush/u3.png'), pygame.image.load('sprites/Crush/u4.png'), pygame.image.load('sprites/Crush/u5.png'), pygame.image.load('sprites/Crush/u6.png'), pygame.image.load('sprites/Crush/u7.png'), pygame.image.load('sprites/Crush/u8.png')]
            self.sLeft = [pygame.image.load('sprites/Sujin/0.png'), pygame.image.load('sprites/Sujin/1.png'), pygame.image.load('sprites/Sujin/2.png'), pygame.image.load('sprites/Sujin/3.png'), pygame.image.load('sprites/Sujin/4.png'), pygame.image.load('sprites/Sujin/5.png'), pygame.image.load('sprites/Sujin/6.png'), pygame.image.load('sprites/Sujin/7.png'), pygame.image.load('sprites/Sujin/8.png')]
            self.sexpSet = [pygame.image.load('sprites/Sujin/s0.png'), pygame.image.load('sprites/Sujin/s1.png'), pygame.image.load('sprites/Sujin/s2.png'), pygame.image.load('sprites/Sujin/s3.png')]
            self.old = [pygame.image.load('sprites/Oldman/0.png'), pygame.image.load('sprites/Oldman/1.png')]
            self.oexpSet = [pygame.image.load('sprites/Oldman/o0.png'), pygame.image.load('sprites/Oldman/o1.png'), pygame.image.load('sprites/Oldman/o2.png'), pygame.image.load('sprites/Oldman/o3.png')]
            self.vaiLeft = [pygame.image.load('sprites/Sid/0.png'), pygame.image.load('sprites/Sid/1.png'), pygame.image.load('sprites/Sid/2.png'), pygame.image.load('sprites/Sid/3.png'), pygame.image.load('sprites/Sid/4.png'), pygame.image.load('sprites/Sid/5.png'), pygame.image.load('sprites/Sid/6.png'), pygame.image.load('sprites/Sid/7.png'), pygame.image.load('sprites/Sid/8.png')]
            self.vexpSet = [pygame.image.load('sprites/Sid/v0.png'), pygame.image.load('sprites/Sid/v1.png'), pygame.image.load('sprites/Sid/v2.png')]
            self.other1 = [pygame.image.load('sprites/Others/27.png'), pygame.image.load('sprites/Others/28.png'), pygame.image.load('sprites/Others/29.png'), pygame.image.load('sprites/Others/30.png'), pygame.image.load('sprites/Others/31.png'), pygame.image.load('sprites/Others/32.png'), pygame.image.load('sprites/Others/33.png'), pygame.image.load('sprites/Others/34.png'), pygame.image.load('sprites/Others/35.png')]
            self.other2 = [pygame.image.load('sprites/Others/9.png'), pygame.image.load('sprites/Others/10.png'), pygame.image.load('sprites/Others/11.png'), pygame.image.load('sprites/Others/12.png'), pygame.image.load('sprites/Others/13.png'), pygame.image.load('sprites/Others/14.png'), pygame.image.load('sprites/Others/15.png'), pygame.image.load('sprites/Others/16.png'), pygame.image.load('sprites/Others/17.png')]
            self.other3 = [pygame.image.load('sprites/Others/0.png'), pygame.image.load('sprites/Others/1.png'), pygame.image.load('sprites/Others/2.png'), pygame.image.load('sprites/Others/3.png'), pygame.image.load('sprites/Others/4.png'), pygame.image.load('sprites/Others/5.png'), pygame.image.load('sprites/Others/6.png'), pygame.image.load('sprites/Others/7.png'), pygame.image.load('sprites/Others/8.png')]
            self.other4 = [pygame.image.load('sprites/Others/18.png'), pygame.image.load('sprites/Others/19.png'), pygame.image.load('sprites/Others/20.png'), pygame.image.load('sprites/Others/21.png'), pygame.image.load('sprites/Others/22.png'), pygame.image.load('sprites/Others/23.png'), pygame.image.load('sprites/Others/24.png'), pygame.image.load('sprites/Others/25.png'), pygame.image.load('sprites/Others/26.png')]
            self.other5 = [pygame.image.load('sprites/Others/36.png'), pygame.image.load('sprites/Others/37.png'), pygame.image.load('sprites/Others/38.png'), pygame.image.load('sprites/Others/39.png'), pygame.image.load('sprites/Others/40.png'), pygame.image.load('sprites/Others/41.png'), pygame.image.load('sprites/Others/42.png'), pygame.image.load('sprites/Others/43.png'), pygame.image.load('sprites/Others/44.png')]

        def loadBar(self, screen, clock, fps):
            screen.fill(self.black)
            
            for i in range(100):
                clock.tick(fps)
                screen.blit(self.loadImg, (0,0))
                toWrite(screen, "RIP to those dead soul", 24, 320, 220)
                toWrite(screen, "Stay Home, Stay Safe", 24, 325, 250)
                pygame.draw.rect(screen, self.white, ((195, 510), (408, 22)), 5)
                pygame.draw.line(screen, self.red, (200, 520), (200+(i*4), 520), 10)
                txt = str(i+1)+"%"
                toWrite(screen, txt, 28, 620, 510)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

            pygame.time.delay(500)
        
        def scene1(self, screen, bg, clock, fps):
            self.sc = 1
            self.scene = True
            self.awake = True
            self.cawake = True
            while self.scene:
                clock.tick (fps)

                if self.sc == 1:
                    self.gdelay(1000)
                    screen.fill(self.black)
                    screen.blit(self.wakeUp[4], (self.x, self.y))
                    self.angeldBox(screen, 0)
                    self.charText("...!!! Ouch! my head hurts so bad. Where am I?", 170, 535, screen)
                    self.charText("If I recall correctly then our city is locked down due to Corona pandemic.", 170, 550, screen)
                    self.charText("And I was at home developing a game.", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)          
                
                elif self.sc == 2:
                    if self.awake:
                        self.angelAwake(screen, bg)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.wakeUp[0], (self.x, self.y))
                    screen.blit(self.cwakeUp[5], (self.x-60, self.y))
                    self.angeldBox(screen, 1)
                    self.charText("Wait a minute!, Last night I was finishing my game and what the f***?", 170, 535, screen)
                    self.charText("Is this some kind of dream or what?", 170, 550, screen)
                    self.charText("Oh my f***ing GOD!, I can't believe I am inside my own game.", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 3:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.wakeUp[0], (self.x, self.y))
                    screen.blit(self.cwakeUp[5], (self.x-60, self.y))
                    self.angeldBox(screen, 6)
                    self.charText("Ok! don't panic and remember about the game.", 170, 535, screen)
                    self.charText("As far as I remember is my crush must be lying somewhere near.", 170, 550, screen)
                    self.charText("Alex dai was talking about quarantined with crush and looks like wish came true.", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 4:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.cwakeUp[5], (self.x-60, self.y))
                    screen.blit(self.lc, (self.x-30, self.y))
                    self.angeldBox(screen, 4)
                    self.charText("Oh! there she is. What should I do?, Should I wake her up?", 170, 535, screen) 
                    self.charText("Hey! are you alright? Damn! She isn't moving. Should I give her CPR?", 170, 550, screen)
                    self.charText("Damn it! this is really a dream.(I ain't telling her name here :D)", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 5:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.cwakeUp[5], (self.x-60, self.y))
                    screen.blit(self.lc, (self.x-30, self.y))
                    self.crushdBox(screen, 0)
                    self.charText("... ... ... ... ... ... ... ...", 170, 535, screen) 
                    self.charText("- Press ENTER -", 400, 580, screen)
                
                elif self.sc == 6:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.cwakeUp[5], (self.x-60, self.y))
                    screen.blit(self.rc, (self.x-30, self.y))
                    screen.blit(self.viruscn, (self.x+600, self.y))
                    self.angeldBox(screen, 3)
                    self.charText("What is that?", 170, 535, screen) 
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 7:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.cwakeUp[5], (self.x-60, self.y))
                    screen.blit(self.rc, (self.x-30, self.y))
                    screen.blit(self.viruscn, (self.x+680, self.y))
                    self.angeldBox(screen, 5)
                    self.charText("Oh! I forgot I made COVID virus as enemy. Ok! I should act natural. ", 170, 535, screen)
                    self.charText("If she wakes up and found about game then the chance of getting her will be 0%.", 170, 550, screen)
                    self.charText("I must wake her up as soon as possible.", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 8:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    if self.cawake:
                        self.crushAwake(screen, bg)
                    screen.blit(self.cwakeUp[0], (self.x-60, self.y))
                    screen.blit(self.lc, (self.x-30, self.y))
                    self.crushdBox(screen, 1)
                    self.charText("My head is so heavy!!!. I don't think I was drunk last night.", 170, 535, screen)
                    self.charText("Mom! Can I get something to drink with lemon.", 170, 550, screen) 
                    self.charText("- Press ENTER -", 400, 580, screen)
                    self.dskip = False

                elif self.sc == 9:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.cwakeUp[0], (self.x-60, self.y))
                    screen.blit(self.lc, (self.x-30, self.y))
                    self.angeldBox(screen, 0)
                    self.charText("Hey! hey slow down girl! I am not your MOM!!!.", 170, 535, screen)
                    self.charText("They call me the great Nepali Supersayan Uchiha Naruto 5 punch man Tribbiani.", 170, 550, screen) 
                    self.charText("And I am here to save the WORLD from the CHAOS.", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 10:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (self.x-60, self.y))
                    screen.blit(self.lc, (self.x-30, self.y))
                    self.crushdBox(screen, 4)
                    self.charText("What the f***!!! Who are you?", 170, 535, screen)
                    self.charText("Why I am here?", 170, 550, screen) 
                    self.charText("What is this place?", 170, 565, screen) 
                    self.charText("- Press ENTER -", 400, 580, screen)
                
                elif self.sc == 11:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (self.x-60, self.y))
                    screen.blit(self.lc, (self.x-30, self.y))
                    self.angeldBox(screen, 0)
                    self.charText("They call me the great Nepali Supersayan Uchiha Naruto 5 punch man Tribbiani Hamal.", 170, 535, screen) 
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 12:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (self.x-60, self.y))
                    screen.blit(self.lc, (self.x-30, self.y))
                    self.crushdBox(screen, 8)
                    self.charText("Not again!!! you freak,", 170, 535, screen)
                    self.charText("And you literally added Hamal at last.", 170, 550, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 13:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (self.x-60, self.y))
                    screen.blit(self.lc, (self.x-30, self.y))
                    self.angeldBox(screen, 0)
                    self.charText("Oh that!!! I forgot last time.", 170, 535, screen) 
                    self.charText("- Press ENTER -", 400, 580, screen)
                
                elif self.sc == 14:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (self.x-60, self.y))
                    screen.blit(self.lc, (self.x-30, self.y))
                    self.crushdBox(screen, 8)
                    self.charText("Forget about that dumbhead,", 170, 535, screen)
                    self.charText("What's happeing here? Wasn't our city locked down?", 170, 550, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 15:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (self.x-60, self.y))
                    screen.blit(self.rc, (self.x-20, self.y))
                    self.angeldBox(screen, 3)
                    self.charText("Call me that one more time and I am leaving you right here with the virus.", 170, 535, screen) 
                    self.charText("- Press ENTER -", 400, 580, screen)
                
                elif self.sc == 16:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (self.x-60, self.y))
                    screen.blit(self.rc, (self.x-20, self.y))
                    self.crushdBox(screen, 4)
                    self.charText("Wait what? really what virus?", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 17:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (self.x-60, self.y))
                    screen.blit(self.rc, (self.x-20, self.y))
                    self.angeldBox(screen, 0)
                    self.charText("The same virus that made you stay at your home.", 170, 535, screen) 
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 18:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (self.x-60, self.y))
                    screen.blit(self.rc, (self.x-20, self.y))
                    self.crushdBox(screen, 3)
                    self.charText("Ok alright I am sorry, I was just joking, I won't do that again.", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 19:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (self.x-60, self.y))
                    screen.blit(self.lc, (self.x-30, self.y))
                    self.angeldBox(screen, 6)
                    self.charText("Yeah, never joke with the Nepali Supersayan Uchiha Naruto 5 punch man Tribbiani Hamal Stark.", 170, 535, screen) 
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 20:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (self.x-60, self.y))
                    screen.blit(self.lc, (self.x-30, self.y))
                    self.crushdBox(screen, 5)
                    self.charText("Yeah yeah Whatever whatever!!!", 170, 535, screen)
                    self.charText("So the great Blah! Blah! BLah!, How are you gonna save the world from virus?", 170, 550, screen)
                    self.charText("Now don't tell me you are gonna fight them with that toy sword and you can even see them?", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 21:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (self.x-60, self.y))
                    screen.blit(self.lc, (self.x-30, self.y))
                    self.angeldBox(screen, 6)
                    self.charText("Toy Sword? this is a sacred saber used by Anakain Skywalker...", 170, 535, screen) 
                    self.charText("Leave it! Just stay behind my back and watch !!! My Princess", 170, 550, screen) 
                    self.charText("- Press ENTER -", 400, 580, screen)

                else:
                    self.scene = False
                    self.gdelay(300)    


                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYDOWN:
                        if event.key==K_RETURN and not self.dskip:
                            if aud.gameSound:
                                pygame.mixer.Sound.play(self.next)
                            self.sc += 1
                        else:
                            self.sc += 0

                    self.sdata = []
                    gfile = open('Config/config.txt', 'r')
                    for i in range(9):
                        self.sdata.append(gfile.readline())
            
                    if event.type == KEYUP:
                        if event.key == int(self.sdata[8]):
                            gamePause()
                pygame.display.update()

        def scene1a(self, screen, bg, clock, fps, ax, ay, cx, cy):
            self.sc = 1
            self.scene = True
            self.sRun = True
            self.sGone = True
            while self.scene:
                clock.tick (fps)

                if self.sc == 1:
                    if self.sRun:
                        self.sujinRunning(screen, bg, clock, fps, ax, ay, cx, cy)
                        
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (cx, cy))
                    screen.blit(self.sLeft[0], (ax+20, ay))
                    self.sujindBox(screen, 0)
                    self.charText("!!! Hey! Pasa !!! What are you doing outside?", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)       
                    self.dlg = 1
                
                elif self.sc == 2:
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (cx, cy))
                    screen.blit(self.sLeft[0], (ax+20, ay))
                    self.angeldBox(screen, 4)
                    self.charText("Hold on pasa take a breath !! ", 170, 535, screen)
                    self.charText("I don't know myself how to answer that but here I am.", 170, 550, screen)
                    self.charText("By the way, why are you running?", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 3:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (cx, cy))
                    screen.blit(self.sLeft[0], (ax+20, ay))
                    self.sujindBox(screen, 0) 
                    self.charText("I saw something unusual pasa, maybe you won't believe me too.", 170, 535, screen)
                    self.charText("None of them believed me back. So I just became upset and ran from them.", 170, 550, screen)
                    self.charText("And what's that red saber for? don't tell me you are cosplaying at this time?", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 4:
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (cx, cy))
                    screen.blit(self.sLeft[0], (ax+20, ay))
                    self.angeldBox(screen, 4)
                    self.charText("No, pasa as you already know", 170, 535, screen)
                    self.charText("I the great Nepali Supersayan Uchiha Naruto 5 punch man Tribbiani Hamal Stark is", 170, 550, screen)
                    self.charText("fighthing with that unusual things. And you see that girl behind I am saving her.", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 5:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (cx, cy))
                    screen.blit(self.sLeft[0], (ax+20, ay))
                    self.sujindBox(screen, 2) 
                    self.charText("HeHe pasa, who's that? Is she the one you always talk about?", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 6:
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (ax-20, ay))
                    screen.blit(self.sLeft[0], (ax+20, ay))
                    self.crushdBox(screen, 7)
                    self.charText("What are you guys talking about?", 170, 535, screen)
                    self.charText("Hey, you purple hair guy! do you know Angel?", 170, 550, screen)
                    self.charText("He said he isn't from here. But looks like you know him.", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 7:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (ax-20, ay))
                    screen.blit(self.sLeft[0], (ax+20, ay))
                    self.sujindBox(screen, 3) 
                    self.charText("What are you talking about girl? he lives just !!", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 8:
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (ax-20, ay))
                    screen.blit(self.sLeft[0], (ax+20, ay))
                    self.angeldBox(screen, 0)
                    self.charText("Ahem Ahem!!! pasa, did you close the portal?", 170, 535, screen)
                    self.charText("If someone finds it open then we may be in problem.", 170, 550, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 9:
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (ax-20, ay))
                    screen.blit(self.sLeft[0], (ax+20, ay))
                    self.crushdBox(screen, 3)
                    self.charText("... ... ...", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 10:
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (ax-20, ay))
                    screen.blit(self.sLeft[0], (ax+20, ay))
                    self.sujindBox(screen, 2)
                    self.charText("Oh! don't worry about that. You girl, you don't know him?", 170, 535, screen)
                    self.charText("He's the great Nepali Supersayan Uchiha Naruto 5 punch man Tribbiani Hamal Stark.", 170, 550, screen)
                    self.charText("And I am the great Nepali Supersayan Uzumaki Sasuke 5 punchman Joey Rajesh Tony.", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 11:
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (ax-20, ay))
                    screen.blit(self.sLeft[0], (ax+20, ay))
                    self.crushdBox(screen, 8)
                    self.charText("You know what you guys are some crazy animal planet things.", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 12:
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (ax-20, ay))
                    screen.blit(self.sLeft[0], (ax+20, ay))
                    self.sujindBox(screen, 2)
                    self.charText("But you can call me Sujin.", 170, 535, screen)
                    self.charText("By the way, Aren't you a Nurse by preofession?", 170, 550, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 13:
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (ax-20, ay))
                    screen.blit(self.sLeft[0], (ax+20, ay))
                    self.crushdBox(screen, 4)
                    self.charText("Wait!!! How do you know that?", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 14:
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (ax-20, ay))
                    screen.blit(self.sLeft[0], (ax+20, ay))
                    self.angeldBox(screen, 0)
                    self.charText("He knows everything girl thats his power.", 170, 535, screen)
                    self.charText("He can see anyone past, present and future.", 170, 550, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 15:
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (ax-20, ay))
                    screen.blit(self.sLeft[0], (ax+20, ay))
                    self.crushdBox(screen, 5)
                    self.charText("Great! now you can fight along with him.", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 16:
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (ax-20, ay))
                    screen.blit(self.sLeft[0], (ax+20, ay))
                    self.sujindBox(screen, 3)
                    self.charText("Hold a second girl. I know I have great powers.", 170, 535, screen)
                    self.charText("But there's something only he can handle. I saw this future and sent him here.", 170, 550, screen)
                    self.charText("So, if you are nurse then you can heal him when you are close to him.", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 17:
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (ax-20, ay))
                    screen.blit(self.sLeft[0], (ax+20, ay))
                    self.crushdBox(screen, 7)
                    self.charText("Nice! now I can be helpable too.", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 18:
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (ax-20, ay))
                    screen.blit(self.sLeft[0], (ax+20, ay))
                    self.angeldBox(screen, 0)
                    self.charText("Really, you know how to bandage? seems not so reliable.", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 19:
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (ax-20, ay))
                    screen.blit(self.sLeft[0], (ax+20, ay))
                    self.crushdBox(screen, 8)
                    self.charText("Then you can die.", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 20:
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (ax-20, ay))
                    screen.blit(self.sLeft[0], (ax+20, ay))
                    self.sujindBox(screen, 0)
                    self.charText("OK OK! you guys can do this later", 170, 535, screen)
                    self.charText("Be careful Angel. ", 170, 550, screen)
                    self.charText("And you girl just help him. I have somewhere to save.", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 21:
                    if self.sGone:
                        self.sujinGoing(screen, bg, clock, fps, ax, ay, cy)                
                    screen.blit(bg, (0, 0))
                    screen.blit(self.lc, (ax, ay))
                    screen.blit(self.clc, (ax-20, ay))
                    self.crushdBox(screen, 7)
                    self.charText("So your name is Angel hmm!", 170, 535, screen)
                    self.charText("And you got some nice friend to concern.", 170, 550, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 22:
                    screen.blit(bg, (0, 0))
                    screen.blit(self.lc, (ax, ay))
                    screen.blit(self.clc, (ax-20, ay))
                    self.angeldBox(screen, 0)
                    self.charText("Yeah, I don't have many.", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                else:
                    self.help = True
                    self.scene = False
                    self.gdelay(300)    

                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYDOWN:
                        if event.key==K_RETURN and not self.dskip:
                            self.sc += 1
                            if aud.gameSound:
                                pygame.mixer.Sound.play(self.next)
                        else:
                            self.sc += 0
                    
                    self.sdata = []
                    gfile = open('Config/config.txt', 'r')
                    for i in range(9):
                        self.sdata.append(gfile.readline())
            
                    if event.type == KEYUP:
                        if event.key == int(self.sdata[8]):
                            gamePause()
                        
                pygame.display.update()
                
        def scene2(self, screen, bg, clock, fps, ax, ay, cx, cy):
            self.sc = 1
            self.scene = True
            while self.scene:
                clock.tick (fps)

                if self.sc == 1:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (cx, ay))
                    screen.blit(self.old[1], (390,300))
                    screen.blit(self.zrc, (360, 300))
                    screen.blit(self.zlc, (430, 300))
                    screen.blit(self.zuc, (390, 330))
                    self.oldmandBox(screen, 0)
                    self.charText("Someone help me!!!", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 2:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (cx, ay))
                    screen.blit(self.old[1], (390,300))
                    screen.blit(self.zlc, (360, 300))
                    screen.blit(self.zlc, (430, 300))
                    screen.blit(self.zlc, (390, 330))
                    self.angeldBox(screen, 3)
                    self.charText("Wait someone's there!!!", 170, 535, screen)
                    self.charText("Hey! What are you guys doing? (What are these things?)", 170, 550, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)
                
                elif self.sc == 3:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.rc, (ax+50, ay))
                    screen.blit(self.crc, (cx, ay))
                    screen.blit(self.old[1], (390,300))
                    screen.blit(self.zlc, (360, 300))
                    screen.blit(self.zlc, (430, 300))
                    screen.blit(self.zlc, (390, 330))
                    self.crushdBox(screen, 4)
                    self.charText("Wait Angel!", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                else:
                    self.scene = False
                    self.gdelay(300)    


                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYUP:
                        if event.key==K_RETURN:
                            self.sc += 1
                            if aud.gameSound:
                                pygame.mixer.Sound.play(self.next)
                        
                        self.sdata = []
                        gfile = open('Config/config.txt', 'r')
                        for i in range(9):
                            self.sdata.append(gfile.readline())
                
                        if event.key == int(self.sdata[8]):
                            gamePause()
                pygame.display.update()

        def scene2a(self, screen, bg, clock, fps, ax, ay, cx, cy):
            self.sc = 1
            self.scene = True
            self.tel = True
            while self.scene:
                clock.tick (fps)

                if self.sc == 1:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.old[0], (390, 300))
                    screen.blit(self.uc, (390, 320))
                    screen.blit(self.crc, (370, 320))
                    self.oldmandBox(screen, 1)
                    self.charText("Thank you my child, May God always bless you.", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 2:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.old[0], (390, 300))
                    screen.blit(self.uc, (390, 320))
                    screen.blit(self.crc, (370, 320))
                    self.angeldBox(screen, 6)
                    self.charText("Don't worry about that old man.", 170, 535, screen)
                    self.charText("What were you doing here?", 170, 550, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)
                
                elif self.sc == 3:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.old[0], (390, 300))
                    screen.blit(self.uc, (390, 320))
                    screen.blit(self.crc, (370, 320))
                    self.crushdBox(screen, 4)
                    self.charText("Wow! Angel you really don't have manners.", 170, 535, screen)
                    self.charText("Sorry! Grandpa this guy is rude.", 170, 550, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 4:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.old[0], (390, 300))
                    screen.blit(self.uc, (390, 320))
                    screen.blit(self.crc, (370, 320))
                    self.oldmandBox(screen, 2)
                    self.charText("Oh! I don't mind them. He just saved me.", 170, 535, screen)
                    self.charText("Actually, I am a traveller, I came from faraway.", 170, 550, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 5:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.old[0], (390, 300))
                    screen.blit(self.uc, (390, 320))
                    screen.blit(self.crc, (370, 320))
                    self.angeldBox(screen, 2)
                    self.charText("(Manners, rude, mind??? What are they even talking about?)", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 6:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.old[0], (390, 300))
                    screen.blit(self.uc, (390, 320))
                    screen.blit(self.crc, (370, 320))
                    self.crushdBox(screen, 4)
                    self.charText("And what were you doing here?", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 7:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.old[0], (390, 300))
                    screen.blit(self.uc, (390, 320))
                    screen.blit(self.crc, (370, 320))
                    self.oldmandBox(screen, 2)
                    self.charText("I was just getting out of the bar those monsters circled me.", 170, 535, screen)
                    self.charText("Listen Angel, I thought your powers were enough to destroy these viruses.", 170, 550, screen)
                    self.charText("But I was wrong, so I came here to give you something.", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 8:
                    self.dskip = True
                    self.gdelay(100)
                    
                    screen.blit(bg, (0, 0))
                    screen.blit(self.old[0], (390, 300))
                    screen.blit(self.uc, (390, 320))
                    screen.blit(self.crc, (370, 320))
                    self.oldmandBox(screen, 2)
                    self.charText("Choose any one from these?", 170, 535, screen)
                    self.charText("Increases Attack", 170, 580, screen)
                    self.charText("Increases Life", 300, 580, screen)
                    self.charText("Increases Healing", 430, 580, screen)

                    b1 = pygame.Rect(202, 545, 28, 28)
                    b2 = pygame.Rect(332, 545, 28, 28)
                    b3 = pygame.Rect(462, 545, 28, 28)
                    
                    if b1.collidepoint((pygame.mouse.get_pos())):
                        screen.blit(pygame.transform.scale(self.atk, (28, 28)), (203, 549))
                        screen.blit(self.hel, (335, 550))
                        screen.blit(self.rgn, (465, 550))
                        if self.pressed:
                            if aud.gameSound:
                                pygame.mixer.Sound.play(pygame.mixer.Sound('sounds/potion.wav'))
                            self.sc += 1
                            self.dskip = False
                            self.power = "a"
                            
                    elif b2.collidepoint((pygame.mouse.get_pos())):
                        screen.blit(self.atk, (205, 550))
                        screen.blit(pygame.transform.scale(self.hel, (28, 28)), (333, 549))
                        screen.blit(self.rgn, (465, 550))
                        if self.pressed:
                            if aud.gameSound:
                                pygame.mixer.Sound.play(pygame.mixer.Sound('sounds/potion.wav'))
                            self.sc += 1
                            self.dskip = False
                            self.power = "h"
                            
                    elif b3.collidepoint((pygame.mouse.get_pos())):
                        screen.blit(self.atk, (205, 550))
                        screen.blit(self.hel, (335, 550))
                        screen.blit(pygame.transform.scale(self.rgn, (28, 28)), (463, 549))
                        if self.pressed:
                            if aud.gameSound:
                                pygame.mixer.Sound.play(pygame.mixer.Sound('sounds/potion.wav'))
                            self.sc += 1
                            self.dskip = False
                            self.power = "r"

                    else: 
                        screen.blit(self.atk, (205, 550))
                        screen.blit(self.hel, (335, 550))
                        screen.blit(self.rgn, (465, 550))

                    self.pressed = False
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        if event.type == MOUSEBUTTONDOWN:
                            if event.button == 1:
                                self.pressed = True
                        
                        self.sdata = []
                        gfile = open('Config/config.txt', 'r')
                        for i in range(9):
                            self.sdata.append(gfile.readline())
                
                        if event.type == KEYUP:
                            if event.key == int(self.sdata[8]):
                                gamePause()

                elif self.sc == 9:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.old[0], (390, 300))
                    screen.blit(self.uc, (390, 320))
                    screen.blit(self.crc, (370, 320))
                    self.angeldBox(screen, 6)
                    if self.power == "a":
                        self.charText("Yeah I wanted to increase my attack.", 170, 535, screen)
                    if self.power == "r":
                        self.charText("Nice, you can heal me more faster now.", 170, 535, screen)
                    if self.power == "h":
                        self.charText("Whoa! that really grew my life bar.", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 10:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.old[0], (390, 300))
                    screen.blit(self.uc, (390, 320))
                    screen.blit(self.crc, (370, 320))
                    self.oldmandBox(screen, 2)
                    self.charText("Goodbye Angel, we will meet again", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)
                
                elif self.sc == 11:
                    if aud.gameSound and self.tel:
                        pygame.mixer.Sound.play(pygame.mixer.Sound('sounds/teleport.wav'))
                        self.tel = False
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.uc, (390, 320))
                    screen.blit(self.crc, (370, 320))
                    self.crushdBox(screen, 4)
                    self.charText("WTF!!! he just vanished.", 170, 535, screen)
                    self.charText("Things are being weird and I am getting headache.", 170, 550, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 12:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.uc, (390, 320))
                    screen.blit(self.crc, (370, 320))
                    self.angeldBox(screen, 0)
                    self.charText("So guess what he wasn't just a traveller, he was a time traveller.", 170, 535, screen)
                    self.charText("(Hold a sec! he mentioned my name, how did he?! and he also knew my powers.)", 170, 550, screen)
                    self.charText("(Was he Sujin came to warn me? No, that can't be. We made that up.)", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 13:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.uc, (390, 320))
                    screen.blit(self.crc, (370, 320))
                    self.crushdBox(screen, 4)
                    self.charText("Look out! some more viruses are coming Angel.", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)


                else:
                    self.scene = False
                    self.gdelay(300)
                    return(self.power)    

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYDOWN and not self.dskip:
                        if event.key==K_RETURN:
                            self.sc += 1
                            if aud.gameSound:
                                pygame.mixer.Sound.play(self.next)

                    self.sdata = []
                    gfile = open('Config/config.txt', 'r')
                    for i in range(9):
                        self.sdata.append(gfile.readline())
            
                    if event.type == KEYUP:
                        if event.key == int(self.sdata[8]):
                            gamePause()

                pygame.display.update()

        def scene2b(self, screen, bg, clock, fps, ax, ay, cx, cy):
            self.sc = 1
            self.scene = True
            while self.scene:
                clock.tick (fps)

                if self.sc == 1:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax-30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.crushdBox(screen, 7)
                    self.charText("So!!! you really can fight.", 170, 535, screen)
                    self.charText("I haven't introduced my self, have I?", 170, 550, screen)
                    self.charText("I am #### and I live around here.", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 2:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax-30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.angeldBox(screen, 5)
                    self.charText("(What was she thinking I did till now?)", 170, 535, screen)
                    self.charText("(Girls are really weird.)", 170, 550, screen)  
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 3:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax-30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.crushdBox(screen, 8)
                    self.charText("You get lost so easily.", 170, 535, screen)
                    self.charText("Anyway where do you live?", 170, 550, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 4:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax-30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.angeldBox(screen, 4)
                    self.charText("(God! what should I say?? come on brain think of something.))", 170, 535, screen)  
                    self.charText("Sorry, Were you saying something???", 170, 550, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 5:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax-30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.crushdBox(screen, 4)
                    self.charText("Finally!!! you really took an eternity to get out of your thoughts.", 170, 535, screen)
                    self.charText("So! Angel, you live around here?", 170, 550, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 6:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax-30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.angeldBox(screen, 3)
                    self.charText("(Wtf! Is that even a question, of course I live near your place. Our parents know each other.)", 170, 535, screen)
                    self.charText("(That kid you parents always praised about is me, I am that guy.)", 170, 550, screen)
                    self.charText("(But I never stepped out of my house, such an introvert. All I ever do is sit infront of Laptop.)", 170, 565, screen)  
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 7:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax-30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.crushdBox(screen, 7)
                    self.charText("Hey! Hamal Stark where do you go? hmmm! Lost in thoughts again?", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 8:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax-30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.angeldBox(screen, 0)
                    self.charText("No no!, like I before said, I came here to save the WORLD from the CHAOS.", 170, 535, screen)
                    self.charText("I came here through portal, When I finish eliminating every virus from here I will go back.", 170, 550, screen) 
                    self.charText("(Stupid brain and mouth, whata am I even saying!)", 170, 565, screen) 
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 9:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax-30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.crushdBox(screen, 4)
                    self.charText("You are so delusional but I can't even reject to believe that.", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 10:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax-30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.angeldBox(screen, 2)
                    self.charText("(I know right. So much delusional, the main reason why girls don't like me. :())", 170, 535, screen)
                    self.charText("Don't worry my lady, I will save you and walk you home safely.", 170, 550, screen)
                    self.charText("(My lady! who says that!!!, stop thinking shit stupid brain.)", 170, 565, screen)  
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 11:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax-30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.crushdBox(screen, 7)
                    self.charText("Oh! thank you, you are really a good guy. Why aren't there any guys like you here?", 170, 535, screen)
                    self.charText("There's a jerk who doesn't come out that my parents always praise.", 170, 550, screen)
                    self.charText("I don't even like him and another jerk is my boyfriend.", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 12:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax-30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.angeldBox(screen, 4)
                    self.charText("(what? she already hates me, those are such a heartaching words)", 170, 535, screen)
                    self.charText("(And thats where a conversation becomes bitter. Also meddling your bf here)", 170, 550, screen)
                    self.charText("Yeah! Seems like people are jerk around here.", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                else:
                    self.scene = False
                    self.gdelay(300)    


                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYUP:
                        if event.key==K_RETURN:
                            self.sc += 1
                            if aud.gameSound:
                                pygame.mixer.Sound.play(self.next)

                        self.sdata = []
                        gfile = open('Config/config.txt', 'r')
                        for i in range(9):
                            self.sdata.append(gfile.readline())
    
                        if event.key == int(self.sdata[8]):
                            gamePause()

                pygame.display.update()
        
        def scene3(self, screen, bg, clock, fps, ax, ay, cx, cy):
            self.sc = 1
            self.scene = True
            while self.scene:
                clock.tick (fps)

                if self.sc == 1:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.crushdBox(screen, 4)
                    self.charText("I wonder when will these places open again?", 170, 535, screen)
                    self.charText("If you finish your job then we can come here.", 170, 550, screen)
                    self.charText("Oh! By the way do you have any girlfreind?", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 2:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.angeldBox(screen, 1)
                    self.charText("(Yeah, nice place to ask that.)", 170, 535, screen)  
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 3:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.crushdBox(screen, 7)
                    self.charText("You are thinking too long. That means...", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 4:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.angeldBox(screen, 4)
                    self.charText("Wait a minute, you are judging too fast.", 170, 535, screen) 
                    self.charText("And what that means???", 170, 550, screen) 
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 5:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.crushdBox(screen, 5)
                    self.charText("Obviously, you don't have any girlfriend.", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 6:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.angeldBox(screen, 0)
                    self.charText("(Yeah! yeah!, embarrass me with all you have.)", 170, 535, screen)
                    self.charText("Actually I don't need one. I am doing good all alone.", 170, 550, screen)
                    self.charText("(God help me to escape, just change her mind.)", 170, 565, screen)  
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 7:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.crushdBox(screen, 3)
                    self.charText("Oh! poor boy.", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 8:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.angeldBox(screen, 4)
                    self.charText("Stop doing that!", 170, 535, screen)
                    self.charText("(Time to rotate the wheel)", 170, 550, screen) 
                    self.charText("Do you know which mouse walks on two feet?", 170, 565, screen) 
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 9:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.crushdBox(screen, 7)
                    self.charText("Trying to change the subject?", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 10:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.angeldBox(screen, 0)
                    self.charText("If you guess the answer right, I will share you a secret.", 170, 535, screen)
                    self.charText("And if I win you'll stop embarrassing me.", 170, 550, screen)
                    self.charText("(Heard somewhre that girls like secrets, perfect time to plant here.)", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 11:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.crushdBox(screen, 4)
                    self.charText("Hamsters maybe? else don't know", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 12:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.angeldBox(screen, 5)
                    self.charText("MICKEY MOUSE, let me give you another chance", 170, 535, screen)
                    self.charText("Whick duck walks on two legs?", 170, 550, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 13:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.crushdBox(screen, 5)
                    self.charText("Thats easy DONALD DUCK.", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 14:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.angeldBox(screen, 0)
                    self.charText("Every ducks you bubblehead, How did you even get a boyfriend?", 170, 535, screen)
                    self.charText("Now stop talking and let me focus on my fight.", 170, 550, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                else:
                    self.scene = False
                    self.gdelay(300)    


                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYUP:
                        if event.key==K_RETURN:
                            self.sc += 1
                            if aud.gameSound:
                                pygame.mixer.Sound.play(self.next)

                        self.sdata = []
                        gfile = open('Config/config.txt', 'r')
                        for i in range(9):
                            self.sdata.append(gfile.readline())
            
                        if event.key == int(self.sdata[8]):
                            gamePause()

                pygame.display.update()

        def scene3a(self, screen, bg, clock, fps, ax, ay, cx, cy):
            self.sc = 1
            self.oGone = True
            self.scene = True
            while self.scene:
                clock.tick (fps)

                if self.sc == 1:
                    self.gdelay(100)
                    if self.oGone:
                        self.othersRunning(screen, bg, clock, fps, ax, ay, cy)
                    
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.rc, (ax, ay))
                    self.crushdBox(screen, 4)
                    self.charText("Whoa! where are they running?", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 2:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.clc, (ax - 30, ay))
                    screen.blit(self.rc, (ax, ay))
                    self.angeldBox(screen, 3)
                    self.charText("I am feeling some strong energy from there.", 170, 535, screen)  
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 3:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.rc, (ax, ay))
                    self.crushdBox(screen, 4)
                    self.charText("What, what energy? which energy?", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 4:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.rc, (ax, ay))
                    self.angeldBox(screen, 3)
                    self.charText("You will see that let's go!", 170, 535, screen)  
                    self.charText("- Press ENTER -", 400, 580, screen)

                
                else:
                    self.scene = False
                    self.gdelay(300)    


                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYDOWN:
                        if event.key==K_RETURN and not self.dskip:
                            self.sc += 1
                            if aud.gameSound:
                                pygame.mixer.Sound.play(self.next)
                            
                        else:
                            self.sc += 0

                    self.sdata = []
                    gfile = open('Config/config.txt', 'r')
                    for i in range(9):
                        self.sdata.append(gfile.readline())
            
                    if event.type == KEYUP:
                        if event.key == int(self.sdata[8]):
                            gamePause()

                pygame.display.update()

        def scene4(self, screen, bg, clock, fps, ax, ay, cx, cy, mvirus):
            self.sc = 1
            self.scene = True
            while self.scene:
                clock.tick (fps)
                if self.sc == 1:
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(mvirus, (700, 300))
                    self.crushdBox(screen, 4)
                    self.charText("I thought it was just a hallucination that these viruse were getting bigger.", 170, 535, screen)
                    self.charText("But this one looks really big.", 170, 550, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 2:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(mvirus, (700, 300))
                    self.angeldBox(screen, 3)
                    self.charText("Yeah!, this was the one they were running from.", 170, 535, screen)  
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 3:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(mvirus, (700, 300))
                    self.crushdBox(screen, 4)
                    self.charText("You got some big challenge boy, go on time to save world.", 170, 535, screen)
                    self.charText("And if you want some treatment just come to me.", 170, 550, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 4:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(mvirus, (700, 300))
                    self.angeldBox(screen, 4)
                    self.charText("Actually, I am just saving people's world.", 170, 535, screen)  
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 5:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(mvirus, (700, 300))
                    self.crushdBox(screen, 4)
                    self.charText("What do you mean?", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 6:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(mvirus, (700, 300))
                    self.angeldBox(screen, 0)
                    self.charText("You will never understand that.", 170, 535, screen)  
                    self.charText("- Press ENTER -", 400, 580, screen)


                else:
                    self.scene = False
                    self.gdelay(300)    


                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYUP:
                        if event.key==K_RETURN:
                            self.sc += 1
                            if aud.gameSound:
                                pygame.mixer.Sound.play(self.next)
                    
                        self.sdata = []
                        gfile = open('Config/config.txt', 'r')
                        for i in range(9):
                            self.sdata.append(gfile.readline())
        
                        if event.key == int(self.sdata[8]):
                            gamePause()

                pygame.display.update()

        def endScene(self, screen, bg, clock, fps, ax, ay, cx, cy):
            self.sc = 1
            self.vaiRun = True
            self.scene = True
            while self.scene:
                clock.tick (fps)
                if self.sc == 1:
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax-30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.crushdBox(screen, 7)
                    self.charText("Finally, you did it.", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 2:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.angeldBox(screen, 3)
                    self.charText("Seems so, maybe there aren't anymore at this place now.", 170, 535, screen)  
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 3:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.crushdBox(screen, 4)
                    self.charText("So you are leaving?", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 4:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.crc, (ax - 30, ay))
                    screen.blit(self.lc, (ax, ay))
                    self.angeldBox(screen, 0)
                    self.charText("I have to be somewhere.", 170, 535, screen)  
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 5:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.cuc, (390, 255))
                    screen.blit(self.uc, (360, 255))
                    self.crushdBox(screen, 4)
                    self.charText("Oh! yeah saving the world thing right.", 170, 535, screen)
                    self.charText("My house is over there if you ever come back and want to see me.", 170, 550, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 6:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.cuc, (390, 255))
                    screen.blit(self.uc, (360, 255))
                    self.angeldBox(screen, 0)
                    self.charText("Why would I ever come to see you?", 170, 535, screen)  
                    self.charText("- Press ENTER -", 400, 580, screen)


                elif self.sc == 7:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.clc, (390, 255))
                    screen.blit(self.uc, (360, 255))
                    self.crushdBox(screen, 8)
                    self.charText("Never come back then. Just die somewhere.", 170, 535, screen)  
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 8:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.cuc, (390, 255))
                    screen.blit(self.uc, (360, 255))
                    self.angeldBox(screen, 4)
                    self.charText("People thanks like that for saving them?", 170, 535, screen)
                    self.charText("Time to reconsider about helping humans.", 170, 550, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 9:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.cuc, (390, 240))
                    screen.blit(self.uc, (360, 255))
                    self.crushdBox(screen, 4)
                    self.charText("Yeah yeah, do wahtever you want and thanks for saving.", 170, 535, screen)  
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 10:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.cuc, (390, 225))
                    screen.blit(self.uc, (360, 255))
                    self.angeldBox(screen, 0)
                    self.charText("Ok Ok! since you are showing this much of gratitude,", 170, 535, screen)
                    self.charText("I may visit you if I am injured.", 170, 550, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 11:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.cuc, (390, 205))
                    screen.blit(self.uc, (360, 255))
                    self.crushdBox(screen, 4)
                    self.charText("Think as you like.", 170, 535, screen)  
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 12:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.cuc, (390, 185))
                    screen.blit(self.uc, (360, 255))
                    self.angeldBox(screen, 2)
                    self.charText("(What was I even thinking? Oh God!)", 170, 535, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 13:
                    self.gdelay(100)
                    if self.vaiRun:
                        self.vaiWalking(screen, bg, clock, fps, 565, 255)

                        screen.blit(bg, (0, 0))
                        screen.blit(self.vaiLeft[0], (595, 255))
                        screen.blit(self.rc, (565, 255))
                        self.vaidBox(screen, 2)
                        self.charText("Dai, where have you been?, I was looking for you.", 170, 535, screen)
                        self.charText("And who was that?", 170, 550, screen)  
                        self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 14:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    screen.blit(self.vaiLeft[0], (595, 255))
                    screen.blit(self.rc, (565, 255))
                    self.angeldBox(screen, 6)
                    self.charText("Long story yar vai, will share you some other time.", 170, 535, screen)
                    self.charText("Let's go home and make some future track.", 170, 550, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 15:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    self.evilsdBox(screen, 1)
                    self.charText("He must be thinking this is the end.", 170, 535, screen)
                    self.charText("And he is also forgetting about the reality.", 170, 550, screen)
                    self.charText("My Lord! your plans are as smooth as ever.", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                elif self.sc == 16:
                    self.gdelay(100)
                    screen.blit(bg, (0, 0))
                    self.evilsdBox(screen, 0)
                    self.charText("Turning the creator himself into a character.", 170, 535, screen)
                    self.charText("This time, I am the one who will be writing his story.", 170, 550, screen)
                    self.charText("HAHAHA! Nothing amuses me better than playing with humans.", 170, 565, screen)
                    self.charText("- Press ENTER -", 400, 580, screen)

                else:
                    self.scene = False
                    self.gdelay(300)    


                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYDOWN:
                        if event.key==K_RETURN and not self.dskip:
                            self.sc += 1
                            if aud.gameSound:
                                pygame.mixer.Sound.play(self.next)
                        else:
                            self.sc += 0
                    self.sdata = []
                    gfile = open('Config/config.txt', 'r')
                    for i in range(9):
                        self.sdata.append(gfile.readline())
            
                    if event.type == KEYUP:
                        if event.key == int(self.sdata[8]):
                            gamePause()
                pygame.display.update()

        def gdelay(self, dtime):
            pygame.time.delay(dtime)

        def angelAwake(self, screen, bg):
            self.wk = 4
            self.dskip = True
            for i in range(5):
                pygame.time.delay(100)
                screen.blit(bg, (0, 0))
                screen.blit(self.wakeUp[self.wk], (self.x, self.y))
                self.wk -= 1   
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYDOWN:
                        if event.key==K_RETURN and self.dskip:
                            self.sc += 0

                    self.sdata = []
                    gfile = open('Config/config.txt', 'r')
                    for i in range(9):
                        self.sdata.append(gfile.readline())
                    if event.type == KEYUP:
                        if event.key == int(self.sdata[8]):
                            gamePause()
                pygame.display.update()
            
            self.dskip = False
            self.awake = False

        def crushAwake(self, screen, bg):
            self.wk = 5
            self.dskip = True
            for i in range(6):
                pygame.time.delay(250)
                screen.blit(bg, (0, 0))
                screen.blit(self.lc, (self.x-30, self.y))
                screen.blit(self.cwakeUp[self.wk], (self.x-60, self.y))
                self.wk -= 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYDOWN:
                        if event.key==K_RETURN and self.dskip:
                            self.sc += 0

                    self.sdata = []
                    gfile = open('Config/config.txt', 'r')
                    for i in range(9):
                        self.sdata.append(gfile.readline())
                    if event.type == KEYUP:
                        if event.key == int(self.sdata[8]):
                            gamePause()
                pygame.display.update()

            self.dskip = False
            self.cawake = False

        def angelDying(self, screen, bg, ax, ay, cx, cz):
            for i in range(5):
                pygame.time.delay(100)
                screen.blit(bg, (0, 0))
                screen.blit(self.crc, (cx, cz))
                screen.blit(self.wakeUp[i], (ax, ay + (i*3)))
                pygame.display.update()

        def crushDying(self, screen, bg, ax, ay, cx, cy):
            for i in range(6):
                pygame.time.delay(100)
                screen.blit(bg, (0, 0))
                screen.blit(self.lc, (ax, ay))
                screen.blit(self.cwakeUp[i], (cx, cy))
                pygame.display.update()

        def sujinRunning(self, screen, bg, clock, fps, ax, ay, cx, cy):
            self.run = 0
            self.sx = 800 
            self.dskip = True
            self.smove = True 
            self.swsCount = 0
            while self.sx >= ax + 20:
                clock.tick(fps)
                screen.blit(bg, (0, 0))
                screen.blit(self.rc, (ax, ay))
                screen.blit(self.crc, (cx, cy))
                screen.blit(self.sLeft[self.run], (self.sx - 4, ay))
                self.run += 1
                self.sx -= 4
                if self.run + 1 > 9:
                    self.run = 0

                if aud.gameSound:
                    if self.swsCount + 1 > 2:
                        self.swsCount = 0
            
                    if self.smove:
                        if self.run + 1 == 1: 
                            pygame.mixer.Sound.play(self.walk[self.swsCount])
                            self.swsCount += 1    

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYDOWN:
                        if event.key==K_RETURN and self.dskip:
                            self.sc += 0

                    self.sdata = []
                    gfile = open('Config/config.txt', 'r')
                    for i in range(9):
                        self.sdata.append(gfile.readline())
                    if event.type == KEYUP:
                        if event.key == int(self.sdata[8]):
                            gamePause()

                pygame.display.update()

            self.dskip = False
            self.smove = False
            self.sRun = False

        def sujinGoing(self, screen, bg, clock, fps, ax, ay, cy):
            self.go = 0
            self.sx = ax + 20
            self.dskip = True
            self.smove = True
            self.swsCount = 0
            while self.sx > 0:
                clock.tick(fps)
                screen.blit(bg, (0, 0))
                screen.blit(self.lc, (ax, ay))
                screen.blit(self.clc, (ax-20, ay))
                screen.blit(self.sLeft[self.go], (self.sx - 4, ay))
                self.go += 1
                self.sx -= 4
                if self.go + 1 > 9:
                    self.go = 0

                if aud.gameSound:
                    if self.swsCount + 1 > 2:
                        self.swsCount = 0
            
                    if self.smove:
                        if self.go + 1 == 1: 
                            pygame.mixer.Sound.play(self.walk[self.swsCount])
                            self.swsCount += 1    

                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYDOWN:
                        if event.key==K_RETURN and self.dskip:
                            self.sc += 0
                    self.sdata = []
                    gfile = open('Config/config.txt', 'r')
                    for i in range(9):
                        self.sdata.append(gfile.readline())
                    if event.type == KEYUP:
                        if event.key == int(self.sdata[8]):
                            gamePause()

                pygame.display.update()
            self.dskip = False
            self.smove = False
            self.sGone = False

        def othersRunning(self, screen, bg, clock, fps, ax, ay, cy):
            self.orun = 0
            self.ox = 800
            self.dskip = True
            self.omove = True
            self.owsCount = 0
            while self.ox > 0:
                clock.tick(fps)
                screen.blit(bg, (0, 0))
                if ay == 320 or ay == 350 or ay == 390 or ay == 440 or ay == 490:
                    screen.blit(self.other1[self.orun], ((self.ox-3) - 5, 320))
                    screen.blit(self.other2[self.orun], ((self.ox-1) - 5, 350))
                    screen.blit(self.other3[self.orun], (self.ox-5, 390))
                    screen.blit(self.other4[self.orun], ((self.ox+5) - 5, 440))
                    screen.blit(self.other5[self.orun], ((self.ox-5) - 5, 490))
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (ax-30, ay))
                else:
                    screen.blit(self.rc, (ax, ay))
                    screen.blit(self.crc, (ax-30, ay))
                    screen.blit(self.other1[self.orun], ((self.ox-3) - 5, 320))
                    screen.blit(self.other2[self.orun], ((self.ox-1) - 5, 350))
                    screen.blit(self.other3[self.orun], (self.ox-5, 390))
                    screen.blit(self.other4[self.orun], ((self.ox+5) - 5, 440))
                    screen.blit(self.other5[self.orun], ((self.ox-5) - 5, 490))
                
                self.orun += 1
                self.ox -= 5
                if self.orun + 1 > 9:
                    self.orun = 0
                
                if  aud.gameSound:
                    if self.owsCount + 1 > 2:
                        self.owsCount = 0
            
                    if self.omove:
                        if self.orun + 1 == 1: 
                            pygame.mixer.Sound.play(self.walk[self.owsCount])
                            
                        if self.orun + 1 == 1: 
                            pygame.mixer.Sound.play(self.walk2[self.owsCount])
                            
                        if self.orun + 1 == 1: 
                            pygame.mixer.Sound.play(self.walk3[self.owsCount])

                        if self.orun + 1 == 1: 
                            pygame.mixer.Sound.play(self.walk2[self.owsCount])    
                        
                        if self.orun + 1 == 1: 
                            pygame.mixer.Sound.play(self.walk[self.owsCount])
                            self.owsCount += 1 

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYDOWN:
                        if event.key==K_RETURN and self.dskip:
                            self.sc += 0

                    self.sdata = []
                    gfile = open('Config/config.txt', 'r')
                    for i in range(9):
                        self.sdata.append(gfile.readline())
                    if event.type == KEYUP:
                        if event.key == int(self.sdata[8]):
                            gamePause()
                
                pygame.display.update()
            self.dskip = False
            self.omove = False
            self.oGone = False

        def vaiWalking(self, screen, bg, clock, fps, ax, ay):
            self.vrun = 0
            self.vx = 800 
            self.dskip = True
            self.vmove = True
            self.vwsCount = 0
            while self.vx >= ax + 30:
                clock.tick(fps)
                screen.blit(bg, (0, 0))
                screen.blit(self.uc, (ax, ay))
                screen.blit(self.vaiLeft[self.vrun], (self.vx - 4, ay))
                self.vrun += 1
                self.vx -= 4
                if self.vrun + 1 > 9:
                    self.vrun = 0

                if  aud.gameSound:
                    if self.vwsCount + 1 > 2:
                        self.vwsCount = 0
            
                    if self.vmove:
                        if self.vrun + 1 == 1: 
                            pygame.mixer.Sound.play(self.walk[self.vwsCount])
                            self.vwsCount += 1 

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYDOWN:
                        if event.key==K_RETURN and self.dskip:
                            self.sc += 0
                    
                    self.sdata = []
                    gfile = open('Config/config.txt', 'r')
                    for i in range(9):
                        self.sdata.append(gfile.readline())
                    if event.type == KEYUP:
                        if event.key == int(self.sdata[8]):
                            gamePause()

                pygame.display.update()
            self.dskip = False
            self.vmove = False
            self.vaiRun = False

        def angeldBox(self, screen, exp):
            screen.blit(self.expSet[exp], (0, 456))
            pygame.draw.rect(screen, self.white, ((144, 500),(655, 98)), 4)
            screen.blit(self.dBox, (144, 500))
            screen.blit(self.ngel, (160, 510))

        def crushdBox(self, screen, exp):
            screen.blit(self.cexpSet[exp], (0, 456))
            pygame.draw.rect(screen, self.white, ((144, 500),(655, 98)), 4)
            screen.blit(self.dBox, (144, 500))
            screen.blit(self.crsh, (160, 510))

        def sujindBox(self, screen, exp):
            screen.blit(self.sexpSet[exp], (0, 456))
            pygame.draw.rect(screen, self.white, ((144, 500),(655, 98)), 4)
            screen.blit(self.dBox, (144, 500))
            screen.blit(self.sujin, (160, 510))

        def oldmandBox(self, screen, exp):
            screen.blit(self.oexpSet[exp], (0, 456))
            pygame.draw.rect(screen, self.white, ((144, 500),(655, 98)), 4)
            screen.blit(self.dBox, (144, 500))
            screen.blit(self.oldman, (160, 510))

        def vaidBox(self, screen, exp):
            screen.blit(self.vexpSet[exp], (0, 456))
            pygame.draw.rect(screen, self.white, ((144, 500),(655, 98)), 4)
            screen.blit(self.dBox, (144, 500))
            screen.blit(self.vai, (160, 510))

        def evilsdBox(self, screen, exp):
            screen.blit(self.evilexpSet[exp], (0, 456))
            pygame.draw.rect(screen, self.white, ((144, 500),(655, 98)), 4)
            screen.blit(self.dBox, (144, 500))
            screen.blit(self.evils, (160, 510))

        def charText(self, says, tx, ty, screen):
            screen.blit(pygame.font.SysFont("18thCentury", 16).render(says, True, (255, 255, 255)), (tx, ty))

        def farAway(self, screen, bg, ax, ay, af, cx, cy, acj):
            if self.ad == 1:
                self.dist = 750
            else: 
                self.dist = 300
                self.ad = 0
            
            if af and not acj:
                if ax - self.dist > cx or ay - self.dist > cy or ax + self.dist < cx or ay + self.dist < cy:
                    self.scene = True
                    self. sc = 1

                    while self.scene:
                        if self.sc == 1:
                            self.gdelay(100)
                            screen.blit(bg, (0, 0))
                            self.crushdBox(screen, 3)
                            if ax > cx:
                                screen.blit(self.crc, (cx, cy))
                                screen.blit(self.lc, (ax, ay))
                            if ax < cx:
                                screen.blit(self.clc, (cx, cy))
                                screen.blit(self.rc, (ax, ay))
                            self.charText("Hey wait for me!!, I am not an alien like you, I don't have powers.", 170, 535, screen)
                            self.charText("Don't leave me here, you promised to save me.", 170, 550, screen)
                            self.charText("- Press ENTER -", 400, 580, screen)

                        elif self.sc == 2:
                            self.gdelay(100)
                            screen.blit(bg, (0, 0))
                            if ax > cx:
                                screen.blit(self.crc, (cx, cy))
                                screen.blit(self.rc, (ax, ay))
                            if ax < cx:
                                screen.blit(self.clc, (cx, cy))
                                screen.blit(self.lc, (ax, ay))
                            self.angeldBox(screen, 5)
                            self.charText("(Why do I even promise things like that?)", 170, 535, screen)
                            self.charText("- Press ENTER -", 400, 580, screen)
                            
                        else:
                            self.ad += 1
                            self.scene = False
                            self.gdelay(100)    

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                            if event.type == KEYUP:
                                if event.key==K_RETURN:
                                    self.sc += 1

                                self.sdata = []
                                gfile = open('Config/config.txt', 'r')
                                for i in range(9):
                                    self.sdata.append(gfile.readline())
                                if event.key == int(self.sdata[8]):
                                    gamePause()

                        pygame.display.update()    

    def gameMenu(plc):

        menu = True
        pressed = False
        menuBg = [pygame.image.load('gallery/menu/menu1.png'), pygame.image.load('gallery/menu/menu2.png'), pygame.image.load('gallery/menu/menu3.png'), pygame.image.load('gallery/menu/menu4.png'), pygame.image.load('gallery/menu/menu5.png'), pygame.image.load('gallery/menu/menu6.png'), pygame.image.load('gallery/menu/menu7.png'), pygame.image.load('gallery/menu/menu8.png'), pygame.image.load('gallery/menu/menu9.png')]
        menuCount = 0

        if aud.gameMusic:
            pygame.mixer.music.load('sounds/menumusic.wav')
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()    

        while menu:
            clock.tick(fps)

            if menuCount + 1 > 36:
                menuCount = 0

            screen.blit(menuBg[menuCount//4], (0,0))
            menuCount += 1

            pressed = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pressed = True

            b1 = pygame.Rect(550, 250, 180, 30)
            b2 = pygame.Rect(550, 300, 130, 30)
            b3 = pygame.Rect(550, 350, 130, 30)
            b4 = pygame.Rect(550, 400, 80, 30)
                
                
            if b1.collidepoint((pygame.mouse.get_pos())):
                toWrite(screen, "New Game", 56, 550, 250)
                toWrite(screen, "Options", 48, 550, 300)
                toWrite(screen, "Credits", 48, 550, 350)
                toWrite(screen, "Exit", 48, 550, 400)
            
                if pressed:
                    pygame.mixer.music.stop()
                    menu = False
                    if plc == "b":
                        menu = False

                    if plc == "m": 
                        gameRunning = True
                        newGame()

            elif b2.collidepoint((pygame.mouse.get_pos())):
                toWrite(screen, "New Game", 48, 550, 250)
                toWrite(screen, "Options", 56, 550, 300)
                toWrite(screen, "Credits", 48, 550, 350)
                toWrite(screen, "Exit", 48, 550, 400)
            
                if pressed:
                    menu = False
                    loc = "m"
                    gameOptions(loc)

            elif b3.collidepoint((pygame.mouse.get_pos())):
                toWrite(screen, "New Game", 48, 550, 250)
                toWrite(screen, "Options", 48, 550, 300)
                toWrite(screen, "Credits", 56, 550, 350)
                toWrite(screen, "Exit", 48, 550, 400)
            
                if pressed:
                    pygame.mixer.music.pause()
                    menu = False
                    gameCredits()
                
            elif b4.collidepoint((pygame.mouse.get_pos())):
                toWrite(screen, "New Game", 48, 550, 250)
                toWrite(screen, "Options", 48, 550, 300)
                toWrite(screen, "Credits", 48, 550, 350)
                toWrite(screen, "Exit", 56, 550, 400)
            
                if pressed:
                    pygame.mixer.music.stop()
                    pygame.quit()

            else: 
                toWrite(screen, "New Game", 48, 550, 250)
                toWrite(screen, "Options", 48, 550, 300)
                toWrite(screen, "Credits", 48, 550, 350)
                toWrite(screen, "Exit", 48, 550, 400)
            

            pygame.display.flip()

    def gameOptions(loc):
        
        goptions = True 
        pressed = False
        optn = pygame.image.load('gallery/jungle.png')
        keyImg = pygame.image.load('gallery/key.png')
        keyb = pygame.image.load('gallery/keyb.png')

        def toConfig(screen, text, ws, tx, ty):
            screen.blit(keyImg, (tx-12, ty-10))
            text = pygame.font.SysFont("18thCentury", ws).render(text, True, (50, 50, 50))
            screen.blit(text, (tx, ty))

        def configKey(loc):
            conKey = True
            data = []
            gfile = open('config/config.txt', 'r')
            for i in range(9):
                data.append(gfile.readline())

            up =  pygame.key.name(int(data[0])).upper()
            down =  pygame.key.name(int(data[1])).upper()
            left =  pygame.key.name(int(data[2])).upper()
            right =  pygame.key.name(int(data[3])).upper()
            attack =  pygame.key.name(int(data[4])).upper()
            jump =  pygame.key.name(int(data[5])).upper()
            run =  pygame.key.name(int(data[6])).upper()
            call = pygame.key.name(int(data[7])).upper()
            pause = pygame.key.name(int(data[8])).upper()

            pressed = False
            k = 0
            configData = [int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5]), int(data[6]), int(data[7]), int(data[8])]
            while conKey:
                clock.tick(fps)

                screen.blit(optn, (0, 0))

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYUP and pressed:
                        k = event.key
                        if event.key == K_ESCAPE:   
                            conKey = False
                            gameOptions(loc)
                        
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            pressed = True
                            k = 0


                gfile = open('Config/config.txt', 'r')
                toWrite(screen, "Key Binding", 48, 350, 50)
                toWrite(screen, "Up", 24, 350, 120)
                toWrite(screen, "Down", 24, 350, 160)
                toWrite(screen, "Left", 24, 350, 200)
                toWrite(screen, "Right", 24, 350, 240) 
                toWrite(screen, "Attack", 24, 350, 280)
                toWrite(screen, "Jump", 24, 350, 320)
                toWrite(screen, "Run", 24, 350, 360)
                toWrite(screen, "Call", 24, 350, 400)
                toWrite(screen, "Pause", 24, 350, 440) 
                
                toConfig(screen, up, 20, 440, 120) 
                toConfig(screen, down, 20, 440, 160)
                toConfig(screen, left, 20, 440, 200)
                toConfig(screen, right, 20, 440, 240)
                toConfig(screen, attack, 20, 440, 280)
                toConfig(screen, jump, 20, 440, 320)
                toConfig(screen, run, 20, 440, 360)
                toConfig(screen, call, 20, 440, 400)
                toConfig(screen, pause, 20, 440, 440) 
                
                b1 = pygame.Rect(428, 110, 120, 32)
                b2 = pygame.Rect(428, 150, 120, 32)
                b3 = pygame.Rect(428, 190, 120, 32)
                b4 = pygame.Rect(428, 230, 120, 32)
                b5 = pygame.Rect(428, 270, 120, 32)
                b6 = pygame.Rect(428, 310, 120, 32)
                b7 = pygame.Rect(428, 350, 120, 32)
                b8 = pygame.Rect(428, 390, 120, 32)
                b9 = pygame.Rect(428, 430, 120, 32)
                b10 = pygame.Rect(380, 500, 60, 20)
                
                if b1.collidepoint((pygame.mouse.get_pos())):
                    screen.blit(keyb, (428, 110))
                    if pressed:
                        if k>0:
                            up1 = pygame.key.name(k).upper()
                            if down == up1 or left == up1 or right == up1 or attack == up1 or jump == up1 or run == up1 or call == up1 or pause == up1:
                                k = 0
                            else:
                                up = pygame.key.name(k).upper()
                                configData[0] = k
                                pressed = False
                    
                elif b2.collidepoint((pygame.mouse.get_pos())):
                    screen.blit(keyb, (428, 150))
                    if pressed:
                        if k>0:
                            down1 = pygame.key.name(k).upper()
                            if up == down1 or left == down1 or right == down1 or attack ==down1 or jump == down1 or run == down1 or call == down1 or pause == down1:
                                k = 0
                            else:
                                down = pygame.key.name(k).upper()
                                configData[1] = k
                                pressed = False
                    
                elif b3.collidepoint((pygame.mouse.get_pos())):
                    screen.blit(keyb, (428, 190))
                    if pressed:
                        if k>0:
                            left1 = pygame.key.name(k).upper()
                            if up == left1 or down == left1 or right == left1 or attack == left1 or jump == left1 or run == left1 or call == left1 or pause == left1:
                                k = 0
                            else:
                                left = pygame.key.name(k).upper()
                                configData[2] = k
                                pressed = False

                elif b4.collidepoint((pygame.mouse.get_pos())):
                    screen.blit(keyb, (428, 230))
                    if pressed:
                        if k>0:
                            right1 = pygame.key.name(k).upper()
                            if up == right1 or down == right1 or left == right1 or attack == right1 or jump == right1 or run == right1 or call == right1 or pause == right1:
                                k = 0
                            else:
                                right = pygame.key.name(k).upper()
                                configData[3] = k
                                pressed = False

                elif b5.collidepoint((pygame.mouse.get_pos())):
                    screen.blit(keyb, (428, 270))
                    if pressed:
                        if k>0:
                            attack1 = pygame.key.name(k).upper()
                            if up == attack1 or down == attack1 or left == attack1 or right == attack1 or jump == attack1 or run == attack1 or call == attack1 or pause == attack1:
                                k = 0
                            else:
                                attack = pygame.key.name(k).upper()
                                configData[4] = k
                                pressed = False

                elif b6.collidepoint((pygame.mouse.get_pos())):
                    screen.blit(keyb, (428, 310))
                    if pressed:
                        if k>0:
                            jump1 = pygame.key.name(k).upper()
                            configData[5] = k
                            if up == jump1 or down == jump1 or left == jump1 or right == jump1 or attack == jump1 or run == jump1 or call == jump1 or pause == jump1:
                                k = 0
                            else:
                                jump = pygame.key.name(k).upper()
                                configData[5] = k
                                pressed = False

                elif b7.collidepoint((pygame.mouse.get_pos())):
                    screen.blit(keyb, (428, 350))
                    if pressed:
                        if k>0:
                            run1 = pygame.key.name(k).upper()
                            if up == run1 or down == run1 or left == run1 or right == run1 or attack == run1 or jump == run1 or call == run1 or pause == run1:
                                k = 0
                            else:
                                run = pygame.key.name(k).upper()
                                configData[6] = k
                                pressed = False

                elif b8.collidepoint((pygame.mouse.get_pos())):
                    screen.blit(keyb, (428, 390))
                    if pressed:
                        if k>0:
                            call1 = pygame.key.name(k).upper()
                            if up == call1 or down == call1 or left == call1 or right == call1 or attack == call1 or jump == call1 or run == call1 or pause == call1: 
                                k = 0
                            else:
                                call = pygame.key.name(k).upper()
                                configData[7] = k
                                pressed = False

                elif b9.collidepoint((pygame.mouse.get_pos())):
                    screen.blit(keyb, (428, 430))
                    if k>0:
                        pause1 = pygame.key.name(k).upper()
                        if up == pause1 or down == pause1 or left == pause1 or right == pause1 or attack == pause1 or jump == pause1 or run == pause1 or call == pause1:
                            k = 0
                        else:
                            pause = pygame.key.name(k).upper()
                            configData[8] = k                       
                            pressed = False

                elif b10.collidepoint((pygame.mouse.get_pos())):
                    toWrite(screen, "Save", 36, 385, 498)
                    if pressed:
                        gfile = open('config/config.txt', 'w')
                        for cdata in configData:
                            gfile.write(str(cdata))
                            gfile.write("\n")
                        gfile.close()
                        conKey = False
                        gameOptions(loc)
                else: 
                    toWrite(screen, "Save", 28, 390, 500)
                    pressed = False
                    k = 0

                pygame.display.flip()
        
        while goptions:
            clock.tick(fps)

            screen.blit(optn, (0, 0))
            pressed = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYUP:
                    if event.key == K_ESCAPE and loc == "m":
                        goptions = False
                        plc = "m"
                        gameMenu(plc)

                    if event.key == K_ESCAPE and loc == "p":
                        goptions = False

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pressed = True

            gfile = open('config/config.txt', 'r')
            toWrite(screen, "CONTROLS", 48, 345, 50)
            toWrite(screen, "Up", 24, 350, 120)
            toWrite(screen, "Down", 24, 350, 160)
            toWrite(screen, "Left", 24, 350, 200)
            toWrite(screen, "Right", 24, 350, 240) 
            toWrite(screen, "Attack", 24, 350, 280)
            toWrite(screen, "Jump", 24, 350, 320)
            toWrite(screen, "Run", 24, 350, 360)
            toWrite(screen, "Call", 24, 350, 400)
            toWrite(screen, "Pause", 24, 350, 440) 

            ndata = []
            for i in range(9):
                ndata.append(gfile.readline())

            toConfig(screen, pygame.key.name(int(ndata[0])).upper(), 20, 440, 120)
            toConfig(screen, pygame.key.name(int(ndata[1])).upper(), 20, 440, 160)
            toConfig(screen, pygame.key.name(int(ndata[2])).upper(), 20, 440, 200)
            toConfig(screen, pygame.key.name(int(ndata[3])).upper(), 20, 440, 240)
            toConfig(screen, pygame.key.name(int(ndata[4])).upper(), 20, 440, 280)
            toConfig(screen, pygame.key.name(int(ndata[5])).upper(), 20, 440, 320)
            toConfig(screen, pygame.key.name(int(ndata[6])).upper(), 20, 440, 360)
            toConfig(screen, pygame.key.name(int(ndata[7])).upper(), 20, 440, 400)
            toConfig(screen, pygame.key.name(int(ndata[8])).upper(), 20, 440, 440) 


            toWrite(screen, "AUDIO", 48, 140, 50)
            toWrite(screen, "Music", 24, 145, 120)
            if aud.gameMusic:
                pygame.draw.rect(screen, (81, 210, 13), ((210, 116), (40, 25)), 5)
                toWrite(screen, "ON", 20, 218, 122)
            else :
                pygame.draw.rect(screen, (200, 54, 46), ((210, 116), (40, 25)), 5)
                toWrite(screen, "OFF", 20, 216, 122)

            toWrite(screen, "Sound", 24, 145, 160)
            if aud.gameSound:
                pygame.draw.rect(screen, (81, 210, 13), ((210, 156), (40, 25)), 5)
                toWrite(screen, "ON", 20, 218, 162)
            else :
                pygame.draw.rect(screen, (200, 54, 46), ((210, 156), (40, 25)), 5)
                toWrite(screen, "OFF", 20, 216, 162)


            b1 = pygame.Rect(210, 116, 40, 25)
            b2 = pygame.Rect(210, 156, 40, 25)
            b3 = pygame.Rect(345, 495, 130, 30)

            if b1.collidepoint((pygame.mouse.get_pos())):
                toWrite(screen, "Keys Binding", 24, 360, 500)
                if pressed:
                    if aud.gameMusic:
                        aud.gameMusic = False
                    else:
                        aud.gameMusic = True 

            elif b2.collidepoint((pygame.mouse.get_pos())):
                toWrite(screen, "Keys Binding", 24, 360, 500)
                if pressed:
                    if aud.gameSound:
                        aud.gameSound = False
                    else:
                        aud.gameSound = True 


            elif b3.collidepoint((pygame.mouse.get_pos())):
                toWrite(screen, "Keys Binding", 32, 350, 498)
                if pressed:
                    goptions = False 
                    configKey(loc)

            else: 
                toWrite(screen, "Keys Binding", 24, 360, 500)

            pygame.display.flip()

    def gameCredits():
        gcredits = True

        gcdts = pygame.image.load('gallery/night.png')
        ngl = pygame.image.load('sprites/Angel/36.png')
        crs = pygame.image.load('sprites/Crush/0.png')
        sid = pygame.image.load('sprites/Sid/9.png')
        suj = pygame.image.load('sprites/Sujin/9.png')

        if aud.gameMusic:
            pygame.mixer.music.load('sounds/gcreditmusic.wav')
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

        while gcredits:
            clock.tick(fps)

            screen.blit(gcdts, (0, 0))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.mixer.music.stop()
                        gcredits = False
                        plc = "m"
                        gameMenu(plc)

            screen.blit(random.choice([virus1Move[0], virus2Move[0], virus3Move[1]]), (random.randint(100, 700), random.randint(100, 450)))
            screen.blit(random.choice([virus4Move[1], virus5Move[0], virus6Move[1]]), (random.randint(100, 700), random.randint(100, 450)))
            screen.blit(random.choice([virus7Move[0], virus8Move[0], virus9Move[1]]), (random.randint(100, 700), random.randint(100, 450)))
            
            screen.blit(suj, (330, 510))
            screen.blit(crs, (360, 510))
            screen.blit(ngl, (320, 440))
            screen.blit(sid, (440, 510))

            toWrite(screen, "Art and Design", 35, 320, 40)
            toWrite(screen, "BackGround Design", 24, 325, 80)
            toWrite(screen, "Craftpix team", 18, 350, 105)
            toWrite(screen, "Characters Design", 24, 325, 135)   
            toWrite(screen, "Universal-LPC-Spritesheet-Character-Generator", 18, 250, 160)
            toWrite(screen, "Also from rpg maker-mv", 18, 315, 180)
            toWrite(screen, "Edited by", 24, 360, 210)
            toWrite(screen, "Totally by MYSELF :D", 18, 325, 235)

            toWrite(screen, "Music and Sound Design", 35, 260, 285)
            toWrite(screen, "Music by", 24, 360, 325)
            toWrite(screen, "Siddarth Karki", 18, 350, 350)
            toWrite(screen, "Sound Design", 24, 340, 380)
            toWrite(screen, "Again by me :D", 18, 350, 405)

            toWrite(screen, "I don't wanna give credit to myself more :D", 24, 225, 445)
            toWrite(screen, "Made in python(pygame Library)", 24, 260, 470)


            pygame.display.flip() 

    def gamePause():
        pause = True
        pressed = False
        while pause:
            clock.tick(fps)
            pressed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type==KEYUP:
                    if event.key == int(angel.kdata[8]):
                        pause = False

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pressed = True
            screen.blit(bg, (0,0))
            screen.blit(pse, (0,0))
            b1 = pygame.Rect(340, 230, 185, 30)
            b2 = pygame.Rect(340, 300, 130, 30)
            b3 = pygame.Rect(340, 370, 115, 30)
            
            if b1.collidepoint((pygame.mouse.get_pos())):
                toWrite(screen, "Main Menu", 56, 340, 230)
                toWrite(screen, "Options", 48, 340, 300)
                toWrite(screen, "Return", 48, 340, 370)
                if pressed:
                    pause = False
                    plc = "m"
                    gameMenu(plc)

            elif b2.collidepoint((pygame.mouse.get_pos())):
                toWrite(screen, "Main Menu", 48, 340, 230)
                toWrite(screen, "Options", 56, 340, 300)
                toWrite(screen, "Return", 48, 340, 370)
                if pressed:
                    pause = False
                    gameOptions("p")

            elif b3.collidepoint((pygame.mouse.get_pos())):
                toWrite(screen, "Main Menu", 48, 340, 230)
                toWrite(screen, "Options", 48, 340, 300)
                toWrite(screen, "Return", 56, 340, 370)
                if pressed:
                    pause = False
            else: 
                toWrite(screen, "Main Menu", 48, 340, 230)
                toWrite(screen, "Options", 48, 340, 300)
                toWrite(screen, "Return", 48, 340, 370)

            pygame.display.update()

    def virusHordes():
        for virus in vHorde:            
            virus.update(screen, angel.x, angel.y, angel.checkJump)
        
    def zombiesHordes():
        for zombie in zHorde:
            zombie.update(screen, angel.x, angel.y, angel.checkJump, aud.gameSound)

    def checkCollision():
        if angel.slash and len(vHorde) > 0:
            for nov in range(len(vHorde)):
                if (angel.angelBlade.colliderect(vHorde[nov].virusPos)):
                    vHorde[nov].attacked = True

                    if virusBoss:
                        if(angel.angelBlade.colliderect(vHorde[0].virusPos)):
                            vHorde[0].life -= 4 + a
                            angel.hit += 1
                
                        else:
                            vHorde[nov].life -= 8 + a
                    else:
                        vHorde[nov].life -= 4 + a

                    if vHorde[nov].life <= 0:
                        if virusBoss:
                            if vHorde[0].life <= 0:
                                vHorde[0].attack = False
                                del vHorde[0]
                                angel.virusKilled += 1
                                angel.bossKilled = True
                                print("boss here", angel.bossKilled)
                            else:
                                vHorde[nov].attack = False
                                del vHorde[nov]
                                print("mini here")
                        else:
                            vHorde[nov].attack = False
                            del vHorde[nov]
                            angel.virusKilled += 1
                            print("other here")
                        break        
                vHorde[nov].attacked = False
        
        if angel.virusKilled > 0 and angel.virusKilled % 14 == 0:
            angel.levelFinish = True
        
        if zombieScene:
            if angel.slash and len(zHorde) > 0:    
                for noz in range(len(zHorde)):
                    if (angel.angelBlade.colliderect(zHorde[noz].zombiePos)):
                        zHorde[noz].attacked = True
                        zHorde[noz].life -= 2
                        if zHorde[noz].life <= 0: 
                            zHorde[noz].attack = False
                            del zHorde[noz]
                            break         
                    zHorde[noz].attacked = False
            
    def crushAttacked():
        for vrs in range(len(vHorde)):
            if uten.crushPos.colliderect(vHorde[vrs].virusPos):
                uten.life -= 1
                if(uten.life <= 0):
                    scenes.crushDying(screen, bg, angel.x, angel.y, uten.x, uten.y)
                    uten.dead = True

        if zombieScene:
            for zm in range(len(zHorde)):
                if uten.crushPos.colliderect(zHorde[zm].zombiePos):
                    uten.life -= 1
                    if(uten.life <= 0):
                        scenes.crushDying(screen, bg, angel.x, angel.y, uten.x, uten.y)
                        uten.dead = True

    def vAttack():
        for v in range(len(vHorde)):
            if vHorde[v].x >= angel.x-(vHorde[v].width-18) and vHorde[v].y >= angel.y-16 and vHorde[v].x <= angel.x+18 and vHorde[v].y <= angel.y+18:
                angel.novAttack += 1
            angel.nov = angel.novAttack
        angel.novAttack = 0

    def zAttack():
        for z in range(len(zHorde)):
            if zHorde[z].x >= angel.x-22 and zHorde[z].y >= angel.y-16 and zHorde[z].x <= angel.x+18 and zHorde[z].y <= angel.y+18:
                angel.nozAttack += 1
            angel.noz = angel.nozAttack
        angel.nozAttack = 0
        
    def bossattack():
        for mvirus in range(len(vHorde)):
            if vHorde[0].mbAttack:
                angel.life -= 2
                angel.sick = True

    def lvlFinish():
        if angel.x <= 808:
            clock.tick (fps)
            screen.blit(bg, (0, 0))
            screen.blit(me, (10, 10))
            screen.blit(her, (10, 75))
            if angel.y >= uten.y or angel.checkJump: 
                uten.update(screen, angel.x, angel.y, angel.checkJump, angel.follow, aud.gameSound)
                angel.update(screen, virus.attack, zombie.attack, aud.gameSound)
            else:
                angel.update(screen, virus.attack, zombie.attack, aud.gameSound)
                uten.update(screen, angel.x, angel.y, angel.checkJump, angel.follow, aud.gameSound)

            pygame.display.update()   

    def bossPower():
        for mvirus in range(len(vHorde)):
            if angel.x < vHorde[0].x:
                minix = vHorde[0].x - 20
            else: 
                minix = vHorde[0].x +  vHorde[0].width - 20

            miniy = vHorde[0].y

            if angel.hit == 50:  

                for mini in range(2):
                    miniVirus = viruses(minix, miniy + (mini * 70), 32, 32, 4, 100, random.choice([virus1Move, virus2Move, virus3Move]))
                    vHorde.append(miniVirus)
                
                angel.hit = 0
 
    virus1Move = [pygame.image.load('sprites/COVID19/virus/0.png'), pygame.image.load('sprites/COVID19/virus/1.png')]
    virus2Move = [pygame.image.load('sprites/COVID19/virus/2.png'), pygame.image.load('sprites/COVID19/virus/3.png')]
    virus3Move = [pygame.image.load('sprites/COVID19/virus/4.png'), pygame.image.load('sprites/COVID19/virus/5.png')]

    virus4Move = [pygame.image.load('sprites/COVID19/virus/6.png'), pygame.image.load('sprites/COVID19/virus/7.png')]
    virus5Move = [pygame.image.load('sprites/COVID19/virus/8.png'), pygame.image.load('sprites/COVID19/virus/9.png')]
    virus6Move = [pygame.image.load('sprites/COVID19/virus/10.png'), pygame.image.load('sprites/COVID19/virus/11.png')]

    virus7Move = [pygame.image.load('sprites/COVID19/virus/12.png'), pygame.image.load('sprites/COVID19/virus/13.png')]
    virus8Move = [pygame.image.load('sprites/COVID19/virus/14.png'), pygame.image.load('sprites/COVID19/virus/15.png')]
    virus9Move = [pygame.image.load('sprites/COVID19/virus/16.png'), pygame.image.load('sprites/COVID19/virus/17.png')]

    mainVirus = [pygame.image.load('sprites/COVID19/virus/18.png'), pygame.image.load('sprites/COVID19/virus/19.png'), pygame.image.load('sprites/COVID19/virus/20.png'), pygame.image.load('sprites/COVID19/virus/21.png'), pygame.image.load('sprites/COVID19/virus/22.png'), pygame.image.load('sprites/COVID19/virus/23.png'), pygame.image.load('sprites/COVID19/virus/24.png'), pygame.image.load('sprites/COVID19/virus/25.png'), pygame.image.load('sprites/COVID19/virus/26.png'), pygame.image.load('sprites/COVID19/virus/27.png'), pygame.image.load('sprites/COVID19/virus/28.png'), pygame.image.load('sprites/COVID19/virus/29.png'), pygame.image.load('sprites/COVID19/virus/30.png'), pygame.image.load('sprites/COVID19/virus/31.png'), pygame.image.load('sprites/COVID19/virus/32.png'), pygame.image.load('sprites/COVID19/virus/33.png'), pygame.image.load('sprites/COVID19/virus/34.png'), pygame.image.load('sprites/COVID19/virus/35.png')]

    v1 = v2 = v3 = 2

    m = 1

    virusBoss = False
    minivHorde = False
    
    vHorde = []

    a = r = h = 0

    plc = "b"

    levelOne = True
    levelTwo = False
    levelThree = False
    levelFour = False

    scns1 = True
    scns2 = False
    scns2a = True
    scns2b = True

    zHorde = []
    zombie = zombies(360, 300, 32, 52, 2, 100)
    zHorde.append(zombie)
    zombie = zombies(430, 300, 32, 52, 2, 100)
    zHorde.append(zombie)
    zombie = zombies(390, 330, 32, 52, 2, 100)
    zHorde.append(zombie)  
    zombieScene = False                       

    angel = player(100, 330, 32, 51, 4, 100)
    angel.dead = False

    uten = crush(70, 330, 32, 51, 2, 100)
    
    gameMenu(plc)
    
    scenes = cutScenes(100, 330)
    scenes.loadBar(screen, clock, fps)
    if aud.gameMusic:
        pygame.mixer.music.load('sounds/wind.wav')
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

    gameRunning = True
    while gameRunning:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            rdata = []
            gfile = open('Config/config.txt', 'r')
            for i in range(9):
                rdata.append(gfile.readline())
       
            if event.type == KEYUP:
                if event.key == int(rdata[8]):
                    gamePause()

                if event.key == int(rdata[7]):
                    if angel.follow:
                        angel.follow = False 
                    else:
                        angel.follow = True

        if len(vHorde) == 0:
            
            if v1 <= 5:
                levelOne = True
                bg = pygame.image.load('background/bg1.png')

                if levelOne:
                    levelTwo = False
                    levelThree = False
                    levelFour = False
                    if scns1:
                        scenes.scene1(screen, bg, clock, fps)
                        scns1 = False

                    for i in range(v1):
                        zhx = 800
                        zhy = random.randint(280, 520)
                        zvel = 1 
                        virus = viruses(zhx, zhy, 32, 32, zvel, 100, random.choice([virus1Move, virus2Move, virus3Move]))
                        vHorde.append(virus)
                    v1 += 1      
            else:
                if v1 == 6:
                    angel.slash = False
                    scenes.scene1a(screen, bg, clock, fps, angel.x, angel.y, uten.x, uten.y)
                    uten.x = angel.x - 20
                    uten.y = angel.y
                    scenes.help = True
                    v1 += 1

                if v2 <= 5:
                    if angel.x > 800: 
                        angel.x = 58
                        uten.x = 8   
                        scenes.ad = 300
                        angel.virusKilled = 0
                        angel.levelFinish = False
                        levelOne = False
                        levelThree = False
                        levelFour = False
                        bg = pygame.image.load('background/bg2.png')
                        scns2 = True
                    if scns2:
                        if scns2a:
                            scenes.scene2(screen, bg, clock, fps, angel.x, angel.y, uten.x, uten.y)
                        zombieScene = True
                        angel.x += 50
                        scns2 = False

                    elif levelTwo:       
                        for i in range(v2):
                            zhx = random.choice([0, 800])
                            zhy = random.randint(280, 520)
                            zvel = random.choice([1, 2])
                            virus = viruses(zhx, zhy, 42, 42, zvel, 100, random.choice([virus4Move, virus5Move, virus6Move]))
                            vHorde.append(virus)
                        v2 += 1
                            
                    else:
                        if len(zHorde) == 0:
                            uten.x = angel.x -30
                            uten.y = angel.y -10
                            zombieScene = False
                            levelTwo = True
                            if scns2b:
                                angel.slash = False
                                p = scenes.scene2a(screen, bg, clock, fps, angel.x, angel.y, uten.x, uten.y)
                                if p == "a":
                                    a = 2
                                if p == "r":
                                    r = 0.25
                                if p == "h":
                                    angel.incHealth = 50
                                    h = 50
                        
                        if not zombieScene:
                            lvlFinish()

                else:
                    if v2 == 6:
                        scenes.scene2b(screen, bg, clock, fps, angel.x, angel.y, uten.x, uten.y)
                        uten.x = angel.x - 20
                        uten.y = angel.y
                        scenes.help = True
                        v2 += 1

                    if v3 <= 5:
                        if angel.x > 800:  
                            levelOne = False
                            levelTwo = False
                            levelThree = True
                            levelFour = False
                            angel.x = 58
                            uten.x = 8
                            scenes.ad = 300
                            scs = True
                            angel.virusKilled = 0
                            angel.levelFinish = False
                            bg = pygame.image.load('background/bg3.png')
                            scenes.scene3(screen, bg, clock, fps, angel.x, angel.y, uten.x, uten.y)
                        elif levelThree:               
                            for i in range(v3):
                                zhx = random.choice([0, 800])
                                zhy = random.randint(280, 520)
                                zvel = random.choice([2, 4])
                                virus = viruses(zhx, zhy, 52, 52, zvel, 100, random.choice([virus7Move, virus8Move, virus9Move]))
                                vHorde.append(virus)
                            v3 += 1
                            
                        else:
                            lvlFinish()
                            
                    else:
                        if angel.x > 650 and scs:
                            scenes.scene3a(screen, bg, clock, fps, angel.x, angel.y, uten.x, uten.y)
                            uten.x =  angel.x - 30
                            uten.y = angel.y
                            scs = False

                        if m == 1:
                            if angel.x > 800:  
                                levelOne = False
                                levelTwo = False
                                levelThree = False
                                levelFour = True
                                angel.x = 58
                                uten.x = 8 
                                scenes.ad = 300       
                                angel.virusKilled = 0
                                angel.levelFinish = False
                                bg = pygame.image.load('background/bg4.png')
                                scenes.scene4(screen, bg, clock, fps, angel.x, angel.y, uten.x, uten.y, mainVirus[0])

                            elif levelFour:     
                                virusBoss = True
                                mvirus = mainBoss(700, 300, 76, 76, 2, 1000, mainVirus)
                                vHorde.append(mvirus)
                                mvirus.boss = True
                                m += 1
                            else:
                                lvlFinish()
                        else:
                            scenes.endScene(screen, bg, clock, fps, angel.x, angel.y, uten.x, uten.y)
                            gameCredits()
        
        for virus in vHorde:
            clock.tick (fps)
            screen.blit(bg, (0, 0))
            screen.blit(me, (10, 10))
            screen.blit(her, (10, 75))
            
            if angel.y >= virus.y and uten.y >= virus.y or angel.checkJump: 
                virusHordes()
                if angel.y >= uten.y or angel.checkJump: 
                    uten.update(screen, angel.x, angel.y, angel.checkJump, angel.follow, aud.gameSound)
                    angel.update(screen, virus.attack, zombie.attack, aud.gameSound)
                else:
                    angel.update(screen, virus.attack, zombie.attack, aud.gameSound)
                    uten.update(screen, angel.x, angel.y, angel.checkJump, angel.follow, aud.gameSound)

            elif (angel.y < virus.y and uten.y >= virus.y) or (angel.y >= virus.y and uten.y < virus.y) or angel.checkJump:
                if angel.y >= uten.y or angel.checkJump: 
                    uten.update(screen, angel.x, angel.y, angel.checkJump, angel.follow, aud.gameSound)
                    virusHordes()
                    angel.update(screen, virus.attack, zombie.attack, aud.gameSound)
                else:
                    angel.update(screen, virus.attack, zombie.attack, aud.gameSound)
                    virusHordes()
                    uten.update(screen, angel.x, angel.y, angel.checkJump, angel.follow, aud.gameSound) 

            else:
                if angel.y >= uten.y or angel.checkJump: 
                    uten.update(screen, angel.x, angel.y, angel.checkJump, angel.follow, aud.gameSound)
                    angel.update(screen, virus.attack, zombie.attack, aud.gameSound)
                else:
                    angel.update(screen, virus.attack, zombie.attack, aud.gameSound)
                    uten.update(screen, angel.x, angel.y, angel.checkJump, angel.follow, aud.gameSound)
                virusHordes()

            pygame.display.update()

        if zombieScene:
            for zombie in zHorde:
                clock.tick (fps)
                screen.blit(bg, (0, 0))
                screen.blit(me, (10, 10))
                screen.blit(her, (10, 75))
                screen.blit(scenes.old[0], (390,300))
                                    
                if angel.y >= zombie.y and uten.y >= zombie.y or angel.checkJump: 
                    zombiesHordes()
                    if angel.y >= uten.y or angel.checkJump: 
                        uten.update(screen, angel.x, angel.y, angel.checkJump, angel.follow, aud.gameSound)
                        angel.update(screen, virus.attack, zombie.attack, aud.gameSound)
                    else:
                        angel.update(screen, virus.attack, zombie.attack, aud.gameSound)
                        uten.update(screen, angel.x, angel.y, angel.checkJump, angel.follow, aud.gameSound)
                    
                elif (angel.y < zombie.y and uten.y >= zombie.y) or (angel.y >= zombie.y and uten.y < zombie.y) or angel.checkJump:
                    if angel.y >= uten.y or angel.checkJump: 
                        uten.update(screen, angel.x, angel.y, angel.checkJump, angel.follow, aud.gameSound)
                        zombiesHordes()
                        angel.update(screen, virus.attack, zombie.attack, aud.gameSound)
                    else:
                        angel.update(screen, virus.attack, zombie.attack, aud.gameSound)
                        zombiesHordes()
                        uten.update(screen, angel.x, angel.y, angel.checkJump, angel.follow, aud.gameSound)

                else:
                    if angel.y >= uten.y or angel.checkJump: 
                        uten.update(screen, angel.x, angel.y, angel.checkJump, angel.follow, aud.gameSound)
                        angel.update(screen, virus.attack, zombie.attack, aud.gameSound)
                    else:
                        angel.update(screen, virus.attack, zombie.attack, aud.gameSound)
                        uten.update(screen, angel.x, angel.y, angel.checkJump, angel.follow, aud.gameSound)
                    zombiesHordes()


                pygame.display.update()
            
        checkCollision()
        vAttack()
        if zombieScene:
            zAttack()
        crushAttacked()
        scenes.farAway(screen, bg, angel.x, angel.y, angel.follow, uten.x, uten.y, angel.checkJump)

        if uten.heal and scenes.help:
            if h == 50:
                if (angel.life+h) < 150:
                    angel.life += 0.50 + r
                else:
                    uten.heal = False

            else:
                if angel.life < 100:
                    angel.life += 0.50 + r
                else:
                    uten.heal = False
    
            angel.sick = False
         
        if angel.bossKilled:
            virusBoss = False

        if virusBoss and not angel.bossKilled:
            bossattack()
            bossPower() 
 
        if levelOne:
            
            if angel.dead or uten.dead:    
                if angel.dead:     
                    scenes.angelDying(screen, bg, angel.x, angel.y, uten.x, uten.y)
                for vs in range(len(vHorde)):
                    del vHorde[0]
                
                del angel
                del uten
                angel = player(100, 330, 32, 51, 4, 100)
                uten = crush(70, 330, 32, 51, 2, 100)
                v1 = 2
                scns1 = False

        if not scns2 and not levelOne and not levelTwo and not levelThree and not levelFour:
        
            if angel.dead or uten.dead:  
                if angel.dead:       
                    scenes.angelDying(screen, bg, angel.x, angel.y, uten.x, uten.y)
                for zs in range(len(zHorde)):
                    del zHorde[0]
                
                del angel
                del uten
                angel = player(100, 330, 32, 51, 4, 100)
                uten = crush(70, 330, 32, 51, 2, 100)
                zHorde = []
                zombie = zombies(360, 300, 32, 52, 2, 100)
                zHorde.append(zombie)
                zombie = zombies(430, 300, 32, 52, 2, 100)
                zHorde.append(zombie)
                zombie = zombies(390, 330, 32, 52, 2, 100)
                zHorde.append(zombie)  

                scns2 = True
                scns2a = False
            
        if levelTwo:
    
            if angel.dead or uten.dead:  
                if angel.dead:       
                    scenes.angelDying(screen, bg, angel.x, angel.y, uten.x, uten.y)
                for vs in range(len(vHorde)):    
                    del vHorde[0]
                
                del angel
                del uten
                angel = player(100, 330, 32, 51, 4, 100)
                angel.incHealth = h
                uten = crush(70, 330, 32, 51, 2, 100)
                v2 = 2
                scns2b = False

        if levelThree:
        
            if angel.dead or uten.dead:    
                if angel.dead:     
                    scenes.angelDying(screen, bg, angel.x, angel.y, uten.x, uten.y)

                for vs in range(len(vHorde)):
                    del vHorde[0]
                
                del angel
                del uten
                angel = player(100, 330, 32, 51, 4, 100)
                angel.incHealth = h
                uten = crush(70, 330, 32, 51, 2, 100)
                v3 = 2

        if levelFour:

            if angel.dead or uten.dead:    
                if angel.dead:    
                    scenes.angelDying(screen, bg, angel.x, angel.y, uten.x, uten.y)
                for vs in range(len(vHorde)):
                    del vHorde[0]
                
                del angel
                del uten
                angel = player(100, 330, 32, 51, 4, 100)
                angel.incHealth = h
                uten = crush(70, 330, 32, 51, 2, 100)
                m = 1
        
game()
