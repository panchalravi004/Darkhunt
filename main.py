from calendar import c
from matplotlib.patches import Polygon
from matplotlib.pyplot import fill
from pygame import *
import pygame
from pygame.locals import *
import time
from button import *
from levels import *
import random
# Initialize Game
pygame.init()

# WIDTH AND HEIGHT
WIDTH = 800
HEIGHT = 400

#  SET SCREEN
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Dark-Hunt")

# SET FPS
clock = pygame.time.Clock()
FPS = 60

# DEFINE COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (104, 104, 104)
YELLOWGREY = (234, 212, 152)
DARKGREEN = (25, 65, 25)
LIGHTGREEN = (25, 250, 25)
RED = (255, 25, 25)
DARKBLUE = (20, 50, 105)
LIGHTBLUE = (20, 25, 255)
YELLOW = (255, 255, 0)
PISTA = (212,241,231)

# Game Varialble
startgame = True
dashbord = True
setting = False

# Game Button
startbtn = Button('START',120,80,120,30,WHITE,RED,14,BLACK,WHITE)
exitbtn = Button('EXIT',120,115,120,30,WHITE,RED,14,BLACK,WHITE)
backbtn = Button('BACK',5,5,50,20,WHITE,RED,12,BLACK,WHITE)
test = Button('test',100,5,50,20,WHITE,RED,12,BLACK,WHITE)

# load Images
bgimage = pygame.transform.scale(pygame.image.load('assets/DarkHub-BG.png').convert_alpha(), (WIDTH,HEIGHT))
avtar = pygame.transform.scale(pygame.image.load('assets/avtar-db.png').convert_alpha(), (150,150))
flash = pygame.transform.scale(pygame.image.load('assets/flash.png').convert_alpha(), (250,250))
bgorange = pygame.image.load('assets/bg-orange.png').convert_alpha()
bgblue =   pygame.image.load('assets/bg-blue.png').convert_alpha()
playerimg =   pygame.image.load('assets/player.png').convert_alpha()

class Dashboard:
    def __init__(self):
        pass
    def dashboard(self):
        # screen.blit(avtar,(100,100))
        pass

    def startgame(self):
        screen.blit(bgimage,(0,0))
    def setting(self):
        screen.fill(WHITE)

class World:
    def __init__(self):
        self.obs = []
    def draw(self):
        for row_index,row in enumerate(level1()):
            pos_y = row_index * 40
            for col_index,col in enumerate(row):
                pos_x = col_index * 40
                if col == 1:
                    box = Box(pos_x,pos_y)
                    box_group.add(box)
                    all_sprire.add(box)
                    self.obs.append(box)
                if col == 2:
                    player = Player(pos_x,pos_y)
                    all_sprire.add(player)
                if col == 3:
                    enemy = Enemy(pos_x,pos_y)
                    enemy_group.add(enemy)
                    all_sprire.add(enemy)
                if col == 4:
                    fire = Fire(pos_x,pos_y)
                    fire_group.add(fire)
                    all_sprire.add(fire)
        return player,self.obs

move_left = False
move_up = False
move_right = False
class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Player,self).__init__()
        self.x = x
        self.y = y
        self.image = pygame.Surface((40,40))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(topleft=(x,y))
        self.jump = False
        self.in_air = False
        self.val_y = 0
        self.screen_scroll = 0
        self.eye_x = self.rect.x + 10
        self.eye_color = WHITE
        self.eye_color_change = 120
        self.eye_color_return = 25
        self.hide = False
        self.left_particles = []
        self.right_particles = []
        self.jump_particles = []

    def eye(self):
        self.eye_color_change -= 1
        pygame.draw.circle(screen,self.eye_color, [self.eye_x,self.rect.y + 10], 2, width=2)

        if self.eye_color_change <= 0:
            self.eye_color = RED
            self.eye_color_change = 120
        else:
            self.eye_color_return -= 1
            if self.eye_color_return <= 0:
                self.eye_color = WHITE
                self.eye_color_return = 25

        if move_left:
            self.eye_x = self.rect.x + 10
        elif move_right:
            self.eye_x = self.rect.x + 30
    def tail(self):
        #player particals for tail
        if move_left:
            for i in range(2):
                self.left_particles.append([[self.rect.x, self.rect.y], [
                                random.randint(0, 15)/10, random.randint(0, 2)], random.randint(4, 8)])
            for particle in self.left_particles:
                particle[0][0] += particle[1][0]
                particle[0][1] -= particle[1][1] * 0.08
                particle[2] -= 0.1
                particle[1][1] += 0.2

                tail = pygame.surface.Surface((particle[2],particle[2]))
                tail.fill(BLACK)
                screen.blit(tail,(int(particle[0][0])+35, int(particle[0][1])+35))

                if particle[2] <= 1:
                    self.left_particles.remove(particle)

        elif move_right:
            for i in range(2):
                self.right_particles.append([[self.rect.x, self.rect.y], [
                                random.randint(0, 15)/10, random.randint(0, 2)], random.randint(4, 8)])
            for particle in self.right_particles:
                particle[0][0] -= particle[1][0]
                particle[0][1] -= particle[1][1] * 0.08
                particle[2] -= 0.1
                particle[1][1] += 0.2

                tail = pygame.surface.Surface((particle[2],particle[2]))
                tail.fill(BLACK)
                screen.blit(tail,(int(particle[0][0]), int(particle[0][1])+35))

                if particle[2] <= 1:
                    self.right_particles.remove(particle)
        
        elif move_up:
            for i in range(2):
                self.jump_particles.append([[self.rect.x, self.rect.y], [
                                random.randint(0, 15)/10, random.randint(0, 2)], random.randint(4, 8)])
            for particle in self.jump_particles:
                particle[0][1] += particle[1][1]
                particle[2] -= 0.1
                particle[1][1] += 0.2

                tail = pygame.surface.Surface((particle[2],particle[2]))
                tail.fill(BLACK)
                screen.blit(tail,(int(particle[0][0])+18+random.randint(0, 6), int(particle[0][1])+35))

                if particle[2] <= 1:
                    self.jump_particles.remove(particle)
        else:
            self.jump_particles.clear()
            self.left_particles.clear()
            self.right_particles.clear()
        
    def ai(self):
        # for detect left right and stop scroll
        # leftaisurf = pygame.surface.Surface((25,10))
        # rightaisurf = pygame.surface.Surface((25,10))
        
        # leftaisurf_rect = leftaisurf.get_rect(topleft=(self.rect.x - 25,self.rect.y + 20 - 5))
        # rightaisurf_rect = rightaisurf.get_rect(topleft=(self.rect.x + 40,self.rect.y + 20 - 5))

        # screen.blit(leftaisurf,leftaisurf_rect)
        # screen.blit(rightaisurf,rightaisurf_rect)

        # for box in obs:
        #     if box.rect.colliderect(leftaisurf_rect) or box.rt_rect.colliderect(rightaisurf_rect.x+25,rightaisurf_rect.y,25,10):
        #         self.screen_scroll = 0
        #         break
        #         # print('collide')

        # for hide a player on corner
        lt = pygame.surface.Surface((5,5))
        lb = pygame.surface.Surface((5,5))
        rt = pygame.surface.Surface((5,5))
        rb = pygame.surface.Surface((5,5))

        lt.set_colorkey(BLACK)
        lb.set_colorkey(BLACK)
        rt.set_colorkey(BLACK)
        rb.set_colorkey(BLACK)

        lt_rect = lt.get_rect(topleft=(self.rect.x - 2,self.rect.y - 2))
        lb_rect = lb.get_rect(topleft=(self.rect.x - 2,self.rect.y + 38))
        rt_rect = rt.get_rect(topleft=(self.rect.x + 38,self.rect.y - 2))
        rb_rect = rb.get_rect(topleft=(self.rect.x + 38,self.rect.y + 38))


        screen.blit(lt,lt_rect)
        screen.blit(lb,lb_rect)
        screen.blit(rt,rt_rect)
        screen.blit(rb,rb_rect)
        #Check if no corner match then hide is false

        for box in obs:
            if box.rt_rect.colliderect(lt_rect)==False:
                # print('Left Top Collide')
                for box in obs:
                    if box.rt_rect.colliderect(rb_rect)==False:
                        # print('Right Bottom Collide')
                        for box in obs:
                            if box.rb_rect.colliderect(lb_rect)==False:
                                self.hide = False
                                break

        for box in obs:
            if box.lt_rect.colliderect(rt_rect)==False:
                # print('Left Top Collide')
                for box in obs:
                    if box.lt_rect.colliderect(lb_rect)==False:
                        # print('Right Bottom Collide')
                        for box in obs:
                            if box.lb_rect.colliderect(rb_rect)==False:
                                self.hide = False
                                break
        #check end 1
        #Check If corner Match then hide true
        for box in obs:
            if box.rt_rect.colliderect(lt_rect):
                # print('Left Top Collide')
                for box in obs:
                    if box.rt_rect.colliderect(rb_rect):
                        # print('Right Bottom Collide')
                        for box in obs:
                            if box.rb_rect.colliderect(lb_rect):
                                self.hide = True
                                # print('Left Corner Match')
                                # debug('Left Corner Match',200,25)
                                break

        for box in obs:
            if box.lt_rect.colliderect(rt_rect):
                # print('Left Top Collide')
                for box in obs:
                    if box.lt_rect.colliderect(lb_rect):
                        # print('Right Bottom Collide')
                        for box in obs:
                            if box.lb_rect.colliderect(rb_rect):
                                self.hide = True
                                # print('Right Corner Match')
                                # debug('Right Corner Match',300,25)
                                break
        #check end 2

    def update(self):
        self.ai()
        dy =0
        dx = 0

        if self.jump == True and self.in_air == False:
            self.val_y -= 16
            self.jump = False
            self.in_air = True
        if move_left:
            # if player.rect.x > 10:
            dx -= 2
            # self.screen_scroll = 2
        if move_right:
            # if player.rect.x < 305:
            dx += 2
            # self.screen_scroll = 2

        self.val_y += 0.75
        if self.val_y > 5:
            self.val_y = 2
        dy += self.val_y
        
        for box in obs:
            
            if box.rect.colliderect(self.rect.x + dx,self.rect.y,40,40):
                dx = 0
                self.screen_scroll = 0

            if box.rect.colliderect(self.rect.x,self.rect.y + dy,40,40):
                if self.val_y < 0:
                    dy = box.rect.bottom - self.rect.top
                elif self.val_y >= 0:
                    self.in_air = False
                    dy = box.rect.top - self.rect.bottom
            
        self.rect.x += dx
        self.rect.y += dy
        if (self.rect.right > 500 - 300)  or (self.rect.left < 300):
            self.rect.x -= dx
            self.screen_scroll = -dx

def debug(text,x,y):
    font = pygame.font.SysFont('arial',15,2)
    title = font.render(str(text), True,(0,0,0))
    screen.blit(title, (x,y))

class Box(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Box,self).__init__()
        self.image = pygame.surface.Surface((40,40))
        self.image.fill(BLACK)
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(topleft=(x,y))
        self.lt = pygame.surface.Surface((5,5))
        self.lb = pygame.surface.Surface((5,5))
        self.rt = pygame.surface.Surface((5,5))
        self.rb = pygame.surface.Surface((5,5))        
         
    def update(self):
        self.ai()
        self.rect.x += player.screen_scroll
    def ai(self):
        self.lt.set_colorkey(BLACK)
        self.rt.set_colorkey(BLACK)
        self.lb.set_colorkey(BLACK)
        self.rb.set_colorkey(BLACK)
        
        self.lt_rect = self.lt.get_rect(topleft=(self.rect.x - 2,self.rect.y - 2))
        self.rt_rect = self.rt.get_rect(topleft=(self.rect.x + 38,self.rect.y - 2))
        self.lb_rect = self.lb.get_rect(topleft=(self.rect.x - 2,self.rect.y + 38))
        self.rb_rect = self.rb.get_rect(topleft=(self.rect.x + 38,self.rect.y + 38))
        
        screen.blit(self.lt,self.lt_rect)
        screen.blit(self.rt,self.rt_rect)
        screen.blit(self.lb,self.lb_rect)
        screen.blit(self.rb,self.rb_rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Enemy,self).__init__()
        self.x = x
        self.y = y
        self.image = pygame.surface.Surface((40,40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(topleft=(x,y))
        self.enemy_particles = []
        self.obj = []
        self.left = False
        self.right = False
        self.initcount = 300
        self.count = 300
        self.poly_1 = [self.rect.x-30,self.rect.y+260]
        self.poly_2 = [self.rect.x+70,self.rect.y+260]
        self.length = int((abs(self.poly_1[0] - self.poly_2[0]) / 5)/2)
        self.l_angle = -10
        self.r_angle = 10
        self.detect = False
        self.cooldown = 100
        
    def update(self):
        self.rect.x += player.screen_scroll
        self.poly_1[0] += player.screen_scroll
        self.poly_2[0] += player.screen_scroll
        self.ai()
        self.detector()
        self.flames()
        self.eye()

    def eye(self):
        pygame.draw.circle(screen, WHITE,[self.rect.x + 18,self.rect.y + 18],12)
        if self.left:
            pygame.draw.circle(screen, DARKBLUE,[self.rect.x + 12,self.rect.y + 22],4)
        elif self.right:
            pygame.draw.circle(screen, DARKBLUE,[self.rect.x + 24,self.rect.y + 22],4)
        else:
            pygame.draw.circle(screen, DARKBLUE,[self.rect.x + 18,self.rect.y + 22],4)

    def flames(self):
        
        for i in range(2):
            self.enemy_particles.append([[self.rect.x-20+random.randint(1,60),self.rect.y-5+random.randint(1,30)], [
                                random.randint(5,20)/10, random.randint(0, 2)], random.randint(10,30)])
        for particle in self.enemy_particles:
            # particle[0][0] += particle[1][0]
            particle[0][1] -= particle[1][1] * 0.04
            particle[2] -= 0.4
            # particle[1][1] += 0.2

            tail = pygame.surface.Surface((particle[2],particle[2]))
            tail_rect = tail.get_rect(topleft=(int(particle[0][0]), int(particle[0][1]))) 
            tail.fill(BLACK)
            screen.blit(tail,tail_rect)

            if particle[2] <= 1:
                self.enemy_particles.remove(particle)
    def detector(self):
        # debug(self.detect,100,20)

        if self.l_surf_rect.colliderect(player.rect):
            if player.hide == False:
                self.detect = True
        else:
            self.detect = False
        
        if self.r_surf_rect.colliderect(player.rect):
            if player.hide == False:
                self.detect = True
        else:
            self.detect = False

        # self.fire()
        
        if self.detect:
            self.cooldown -= 1
            if self.cooldown <= 0:
                b = Bullet(self.rect.x+20,self.rect.y+20)
                bullet_group.add(b)
                self.cooldown = 300
            gape = self.rect.x - player.rect.x
            if gape != 0:
                if gape > 0:
                    self.rect.x -= 1
                if gape < 0:
                    self.rect.x += 1

    def ai(self):
        self.poly_1 = [self.rect.x-30,self.rect.y+300]
        self.poly_2 = [self.rect.x+70,self.rect.y+300]

        pygame.draw.polygon(screen,YELLOWGREY,[(self.rect.x+20,self.rect.y+20),self.poly_1,self.poly_2])

        self.l_surf = pygame.transform.rotate(pygame.surface.Surface((2,570)).convert_alpha(),(self.l_angle))
        self.l_surf_rect = self.l_surf.get_rect(center=(self.rect.x+20,self.rect.y+20))
        self.l_surf.set_colorkey(BLACK)
        screen.blit(self.l_surf,self.l_surf_rect)

        self.r_surf = pygame.transform.rotate(pygame.surface.Surface((2,570)).convert_alpha(),(self.r_angle))
        self.r_surf_rect = self.r_surf.get_rect(center=(self.rect.x+20,self.rect.y+20))
        self.r_surf.set_colorkey(BLACK)
        screen.blit(self.r_surf,self.r_surf_rect)

        # debug(self.l_angle,100,20)

        if self.initcount == 300:
            n = random.randint(0,2)
            if n == 0:
                self.left = True
                self.right = False
                self.initcount += 1
            if n == 1:
                self.left = False
                self.right = True
                self.initcount += 1

        if self.count == 0:
            self.right = True
            self.left = False

        if self.count == 600:
            self.left = True
            self.right = False

        if self.left:
            # self.poly_1[0] -= 2.4
            # self.poly_1[1] -= 0.8
            # self.poly_2[0] -= 2.4
            # self.poly_2[1] += 0.8
            self.rect.x -= 1
            self.count -= 1
            # self.l_angle -= 0.36
            # self.r_angle -= 0.36

        if self.right:
            # self.poly_1[0] += 2.4
            # self.poly_1[1] += 0.8
            # self.poly_2[0] += 2.4
            # self.poly_2[1] -= 0.8
            self.rect.x += 1
            self.count += 1
            # self.l_angle += 0.36
            # self.r_angle += 0.36

class Fire(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Fire,self).__init__()
        self.x = x
        self.y = y
        self.image = pygame.surface.Surface((40,20))
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(topleft=(x,y+20))
        self.fire_particles = []
    def update(self):
        self.rect.x += player.screen_scroll
        self.flame()
    def flame(self):
        for i in range(2):
            self.fire_particles.append([[self.rect.x-20+random.randint(1,60),self.rect.y-5+random.randint(1,30)], [
                                random.randint(5,20)/10, random.randint(0, 2)], random.randint(10,20),random.randint(60,200)])
        for particle in self.fire_particles:
            particle[0][0] -= particle[1][0] * 0.05
            particle[0][1] -= particle[1][1] * 0.8
            particle[2] -= 0.4
            particle[3] -= 2
            # particle[1][1] += 0.2

            f = pygame.surface.Surface((particle[2],particle[2]))
            f.set_alpha(particle[3])
            f_rect = f.get_rect(topleft=(int(particle[0][0]), int(particle[0][1]))) 
            f.fill(BLACK)
            screen.blit(f,f_rect)

            if particle[2] <= 1:
                self.fire_particles.remove(particle)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Bullet,self).__init__()
        self.x = x
        self.y = y
        self.image = pygame.surface.Surface((5,45))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(topleft=(x,y))
        self.bullet_particles = []
    def update(self):
        self.rect.x += player.screen_scroll
        self.rect.y += 8
        if self.rect.y > HEIGHT:
            self.kill()
        if self.rect.colliderect(player.rect):
            self.kill()
        self.flame()
    def flame(self):
        for i in range(2):
            self.bullet_particles.append([[self.rect.x-2+random.randint(0, 4),self.rect.y+random.randint(0, 40)], [
                                random.randint(5,20)/10, random.randint(0, 2)], random.randint(5,15)])
        for particle in self.bullet_particles:
            # particle[0][0] += particle[1][0]
            # particle[0][1] += particle[1][1]
            particle[2] -= 0.6
            particle[1][1] += 0.2

            tail = pygame.surface.Surface((particle[2],particle[2]))
            tail_rect = tail.get_rect(topleft=(int(particle[0][0]), int(particle[0][1]))) 
            tail.fill(RED)
            screen.blit(tail,tail_rect)

            if particle[2] <= 1:
                self.bullet_particles.remove(particle)
db = Dashboard()

box_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
fire_group = pygame.sprite.Group()
all_sprire = pygame.sprite.Group()

world = World()
player,obs = world.draw()

# Init RUN
run = True
# Main Loop
while run:
    clock.tick(FPS)

    if startgame == False and dashbord == True:
        screen.fill(BLACK)
        db.dashboard()

        #start button
        startbtn.msg(screen,'To Start Game','right')
        if startbtn.draw(screen):
            startgame = True

        #exit button
        exitbtn.msg(screen,'To Exit The Game','right')
        if exitbtn.draw(screen):
            run = False

    # setting section
    elif setting:
        db.setting()

    # game is started
    else:
        db.startgame()
        box_group.update()
        box_group.draw(screen)
        enemy_group.update()
        enemy_group.draw(screen)
        fire_group.update()
        fire_group.draw(screen)
        all_sprire.update()
        all_sprire.draw(screen)
        bullet_group.update()
        bullet_group.draw(screen)

        player.tail()
        if player.hide == False:
            player.eye()

        if backbtn.draw(screen):
            startgame = False
            dashbord = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_LEFT:
                move_left = True
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_UP:
                player.jump = True
                move_up = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_UP:
                player.jump = False
                move_up = False
                
    # update and flip our display
    pygame.display.update()
    pygame.display.flip()

pygame.quit()