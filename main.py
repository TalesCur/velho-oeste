import pygame
from inimigo import Inimigo
from warning import Warning
from functions import lerp
import random

pygame.init()
pygame.mixer.init()
pygame.font.init()

_bg = pygame.image.load("background.png")
bg = pygame.transform.scale(_bg, (_bg.get_width()*1.1, _bg.get_height()*1.1))

gun = [pygame.image.load("images/gun_fire_frame2.png"), pygame.image.load("images/gun_fire_frame1.png")]
gun_frame = 0
font = pygame.font.SysFont("Comic Sans MS", 50)

# Initiating sounds
tema = pygame.mixer.Sound("sounds/main_theme.mp3")
tema.set_volume(1.0)
shot = pygame.mixer.Sound("sounds/shot.wav")
shot.set_volume(0.8)
ready_sound = pygame.mixer.Sound("sounds/ready_sound.wav")
ready_sound.set_volume(0.3)
nphase = pygame.mixer.Sound("sounds/nextphase.wav")
nphase.set_volume(0.3)
gun_fail = pygame.mixer.Sound("sounds/gun_fail.wav")

#Blood stuff
global blood_y
blood_y = -1280
blood_sprite = pygame.image.load("images/blood.png")
global blood_vspd
blood_vspd = 0

global _set
_set = False

global fail_cooldown
fail_cooldown = 0

global start
start = random.randint(60, 120)

game_over_reset_timer = 0

global start_start
start_start = start
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

fase = 1

# Estados do jogo: "game", "game_over", "won" 
global game_state
game_state = "game"

cam_x = 0
cam_y = 0
cam_zoom = 1
cam_zoom_targ = 1
shake = 0

dt = 1

img_break = pygame.image.load("images/break.png")

global inimigo
inimigo = Inimigo(640, 420, 1, 1)
inimigo.y = 1200

global inimigo_timer
inimigo_timer = random.randint(30, 60)
                                                     
global pontos
pontos = 0

global arma
arma = False

running = True

warning = None

won = False

global reset_timer
reset_timer = 120

tema.play()

def ini(f):

    global start
    start = round(random.randint(120, 180) / (1+f*.25))

    global arma
    arma = False

    global blood_y
    blood_y = -1280

    global blood_vspd
    blood_vspd = 0

    global start_start
    start_start = start

    global game_state
    game_state = "game"

    global _set
    _set = False
    dt = 1
    warning = None

    global inimigo
    inimigo.current_sprite = 0
    inimigo.y = 1200
    
    global reset_timer
    reset_timer = 120

    global inimigo_timer
    inimigo_timer = random.randint(60, 100) / (1+f*.15)

ini(pontos)

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    cam_zoom = lerp(cam_zoom, cam_zoom_targ, .1)
    gun_frame+=.1

    sprite_bg = pygame.transform.scale(bg, (bg.get_width()*cam_zoom, bg.get_height()*cam_zoom))
    screen.blit(sprite_bg, (round(640-sprite_bg.get_width()*.5+cam_x), round(288-sprite_bg.get_height()*.5+cam_y)))
    cam_x = random.uniform(-shake, shake)
    cam_y = random.uniform(-shake, shake)
    shake *= .9

    if not _set:
        

        if start == round(start_start/2):
            
            cam_zoom_targ += .1
            ready_sound.play()
            warning = Warning(0)
        elif start == 1:
            
            if random.randint(0, 1) == 1:
                
                cam_zoom_targ += .1
                ready_sound.play()
                warning = Warning(1)
                _set = True
                start = round(random.randint(50, 100) / (1+pontos*.1))

            else:
                
                ready_sound.play()
                warning = Warning(2)
                _set = False
    else:
        
        if start == 10:

            ready_sound.play()
            warning = Warning(2)


    keys = pygame.key.get_pressed()

    inimigo.update(dt)
    inimigo.draw(screen, cam_x, cam_y, cam_zoom)

    if warning != None:
        warning.update(dt)
        warning.draw(screen)
    
    pontos_text = font.render("Pontos: " + str( pontos), False, (255, 255, 255))
    screen.blit(pontos_text, (0, 0))
    if arma:
        screen.blit(gun[min(round(gun_frame), 1)], (900,405))
    if game_state == "game":

        if fail_cooldown > 0:
            fail_cooldown-=1
        else:
            arma = False
        
        if start <= 0:
            cam_zoom_targ = 1
            if keys[pygame.K_SPACE] and fail_cooldown <= 0:
                
                gun_frame = 0
                inimigo.die()
                game_state = "won"
                shake = 10
                pontos += 1
                shot.play()
                arma = True
            else:

                if inimigo_timer <= 0:
                    
    
                    inimigo.shoot()
                    game_state = "game_over"
                    game_over_reset_timer = 120
                    shake = 10
                    shot.play()
                    tema.stop()
                else:
                    inimigo_timer -= 1
        else:

            if keys[pygame.K_SPACE] and fail_cooldown <= 0:

                gun_frame = 1
                gun_fail.play()
                fail_cooldown = 100
                arma = True
    elif game_state == "game_over":

        vidro = pygame.transform.scale(img_break,(1280, 720))
        screen.blit(vidro, (-cam_x, -cam_y))

        if blood_y < 0:
            blood_y+=blood_vspd
            blood_vspd+=.2
        else:
            blood_y = 0
            blood_vspd = 0

        if game_over_reset_timer <= 0:
            
            if keys[pygame.K_SPACE]:
                
                arma = True
                pontos = 0
                ini(pontos)
                tema.play()
        else:
            game_over_reset_timer-=1

        screen.blit(blood_sprite, (0, blood_y))

    elif game_state == "won":
        if reset_timer > 0:
            reset_timer-=1
        else:
            fase+=1
            nphase.play()
            ini(pontos)
    pygame.display.flip()
    
    start-=1

    dt = clock.tick(60)
    dt = max(.001, min(dt, .1))
pygame.quit()