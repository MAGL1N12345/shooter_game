from pygame import *
from random import randint

score = 0
goal = 10
lost = 0
max_lost = 3
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN', True, (255, 255, 255))
lose = font1.render('YOU LOSE', True, (180, 0, 0))
front2 = font.SysFont('Arial', 40) 
class GameSprite(sprite.Sprite):
    def __init__(self, plaer_speed, plaer_image, plaer_x, plaer_y, wigth, height):
        super().__init__()
        self.image = transform.scale(image.load(plaer_image), (wigth, height))
        self.speed = plaer_speed
        self.rect = self.image.get_rect()
        self.rect.x = plaer_x
        self.rect.y = plaer_y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_passed = key.get_pressed()

        if keys_passed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys_passed[K_d] and self.rect.x < 650:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(5, 'bullet.png', self.rect.centerx, self.rect.top,  10, 17)
        bullets.add(bullet)


class Enemy(GameSprite):
   
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(5,620)
            lost += 1




class Bullet(GameSprite):
   
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()






win_widht = 700
win_height = 500
finish = False
game = True



window = display.set_mode((win_widht, win_height))
display.set_caption('динамический шутер с увлекающим геймплеем')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
hero = Player(5, 'rocket.png', 100, 400, 50, 65)
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")
cyborgs = sprite.Group()
bullets = sprite.Group()
for i in range(5):
    cyborg = Enemy(randint(3, 7), 'ufo.png',randint(5, 620), 0, 65, 50)
    cyborgs.add(cyborg)
game = True
clock = time.Clock()
FPS = 60
speed = 10
font.init()
font = font.Font(None, 30)
killed, lost = 0, 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                hero.fire()
        collides = sprite.groupcollide(cyborgs, bullets, True, True)     
        for c in collides:
            score = score + 1
            cyborg = Enemy('ufo.png', randint(80, win_widht - 80), -40, 80, 50, randint(1, 5))
            cyborgs.add(cyborg)
        
        if sprite.spritecollide(hero, cyborgs, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))



    if not finish:
        window.blit(background,(0, 0))
        win = font.render(
            "kills:"+ str(killed), True, (255, 255, 255)
        )
        window.blit(win, (10, 10))
        lose = font.render(
            "missed:"+ str(lost), True, (255, 255, 255)
        )
        window.blit(lose, (10, 50))



        if sprite.groupcollide(cyborgs, bullets, True, True):
            killed += 1
            
        #if sprite.spritecollide(hero, cyborgs, False):
            #finish = True
            #window.blit(lose, (200, 200))
        


        hero.update()
        hero.reset()
        cyborgs.update()
        cyborgs.draw(window)
        bullets.update()
        bullets.draw(window)
        display.update()
        clock.tick(FPS)



