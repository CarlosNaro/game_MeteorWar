# importacion de lalibreria 

import pygame, random

# definimos la propiedades del campo de juego 
WIDTH = 800
HEIGHT = 600 
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255, 0) 

pygame.init() #inicializamos el pygame
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT)) #DIMENCION DE LA PANTALLA DE JUEGO 
pygame.display.set_caption("la guerrita") #titulo del juego 
clock = pygame.time.Clock()

#función que dibuje  el texto 

def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)

def draw_shield_bar(surface, x, y, percentage ):
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGHT
    border = pygame.Rect(x, y,BAR_LENGHT, BAR_HEIGHT)
    fill = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill )
    pygame.draw.rect(surface, WHITE,border ,2)


#definimos la clase jugador 

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert()
        self.image.set_colorkey(BLACK) #eliminar el borde de la imagen exportada 
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH //2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.shield = 100 #variable que ayudará en la vida del jugador 
    
    def update(self):
        #definimos el control del juego 
        self.speed_x = 0 # chequemos que la velocidad sea igual a cero 
        #metodo que trae lista de todas las teclas presionadas 
        keystate = pygame.key.get_pressed() # chequemos si alguna tecla esta precionado 
        #logica para mover la nave 
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        #logica para no salirnos del campo de juego 
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    #función shoot para disparar 
    def shoot(self):
        bullet = Bullet( self.rect.centerx, self.rect.top) # instacia para crear bala 
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play()
        

class Meteor(pygame.sprite.Sprite):
    def __init__(self): #inicializar la clase 
        super().__init__() #iniciallizamos la superclase 
        self.image = random.choice(meteor_images)
        #quitamos el color negro 
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/laser1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y 
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0: # con esto se verifca e elimina la instacia del objeto que ejecutamos 
            self.kill() 
      

class Explosion( pygame.sprite.Sprite ):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50 # VELOCIDAD 
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now 
            self.frame +=1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center 
                


def show_go_screen():
    screen.blit(background, [0,0]) # dar fondo a la pantalla de inicio 
    draw_text(screen, "SHOOTER", 65, WIDTH // 2 , HEIGHT //4)
    draw_text(screen, "Iquitos Technology", 27, WIDTH // 2 , HEIGHT //2)
    draw_text(screen, "Press Key",20 ,WIDTH //2 , HEIGHT * 3/4 )
    pygame.display.flip()
    Waiting = True
    while Waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              pygame.quit()
        
            if event.type == pygame.KEYUP:
                Waiting = False
         
         


meteor_images = []
meteor_list = [
"assets/meteorGrey_big1.png",
"assets/meteorGrey_big2.png",
"assets/meteorGrey_big3.png",
"assets/meteorGrey_big4.png",
"assets/meteorGrey_med1.png",
"assets/meteorGrey_med2.png",
"assets/meteorGrey_small1.png",
"assets/meteorGrey_small2.png",
"assets/meteorGrey_tiny1.png",
"assets/meteorGrey_tiny2.png",
]

for item in meteor_list:
    meteor_images.append(pygame.image.load(item).convert())
 
 #---------------- EXPLOSION IMAGENES--------
explosion_anim =[]
for item in range(9):
    file = "assets/regularExplosion0{}.png".format(item)
    img = pygame.image.load(file).convert()
    img.set_colorkey(BLACK)
    img_scale = pygame.transform.scale(img, (70,70))
    explosion_anim.append(img_scale)

#cargar imagen de fondo 
background= pygame.image.load("assets/background.png").convert() 

#cargar sonidos 
laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.set_volume(0.2)

# all_sprites = pygame.sprite.Group()
# meteor_list = pygame.sprite.Group()
# bullets = pygame.sprite.Group()

# player = Player()
# all_sprites.add(player) # agregamos el

# for i in range(8):
#   meteor = Meteor()
#   all_sprites.add(meteor)
#   meteor_list.add(meteor)

# #variable que llevara la cuenta de muertes 
# score = 0

#---GAME OVER---

game_over = True

pygame.mixer.music.play(loops=-1)

runnig = True

while runnig:
    if game_over:

        show_go_screen() 
        
        game_over = False
        all_sprites = pygame.sprite.Group()
        meteor_list = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player) # agregamos el

        for i in range(8):
            meteor = Meteor()
            all_sprites.add(meteor)
            meteor_list.add(meteor)

        #variable que llevara la cuenta de muertes 
        score = 0 

    clock.tick(60) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            runnig = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
  
    all_sprites.update()
    
    #COLISIONES - METEORO - LASER
    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
    for item in hits:
        score +=1
        explosion_sound.play()
        explosion = Explosion(item.rect.center)
        all_sprites.add(explosion)
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)
     
    # DETECTAR LAS COLISIONES - JUGADOR - METEORO 
    hits = pygame.sprite.spritecollide(player, meteor_list, True)

    for item in hits:
        player.shield -= 25
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)
        if player.shield <= 0:
            game_over = True
            # runnig=False 
    
    screen.blit(background,[0,0])
    all_sprites.draw(screen) # dibujamos en pantalla 
    
    #marcador 
    draw_text(screen, str(score), 25, WIDTH // 2, 10)
    #escudo 
    draw_shield_bar(screen, 5,5, player.shield)

    pygame.display.flip()
    
pygame.quit()



   

