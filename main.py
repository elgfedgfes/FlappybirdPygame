import pygame
import sys
import random

#Functions
def draw_floor():
    screen.blit(floor,(floor_x_pos,900))
    screen.blit(floor,(floor_x_pos + 576,900))
    
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 250))
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
    return top_pipe,bottom_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if (pipe.bottom >= 1024):
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe ,pipe)
            
def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird_box.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False
            
    if bird_box.top <= -100 or bird_box.bottom >= 900:
        can_score = True
        return False
    
    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_box = new_bird.get_rect(center = (100, bird_box.centery))
    return new_bird,new_bird_box

def score_display(game_state):
    
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
        
        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288,850))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
#Score
def pipe_score_check():
    global score, can_score
    
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True

#pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)

pygame.init()
#initialization screen clock
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',50)

#Game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True



#Initialization Background
backgruound = pygame.image.load('assets/background-day.png').convert()
backgruound = pygame.transform.scale2x(backgruound)

#initialization floor
floor = pygame.image.load('assets/base.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

#initialization pipe
pipe_surface = pygame.image.load('assets/pipe-red.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
#var event
SPAWNPIPE = pygame.USEREVENT
#tmer(milisconds)
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [400,600,800]


#initialization bird & animation
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_box = bird_surface.get_rect(center = (100,512))
#Timer animation
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)
#Game over display
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,512))
#Sounds
flap_sound = pygame.mixer.Sound('sound/wing.wav')
death_sound = pygame.mixer.Sound('sound/hit.wav')
score_sound = pygame.mixer.Sound('sound/point.wav')

#loop
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #Actions
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()
                
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                bird_movement = 0
                bird_movement -= 8
                pipe_list.clear()
                bird_box.center = (100,512)
                score = 0
                     
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            
            bird_surface, bird_box = bird_animation()
    
    #draw background
    screen.blit(backgruound,(0,0))
    
    if game_active:
        #move bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_box.centery += bird_movement
        #draw bird
        screen.blit(rotated_bird,bird_box)
        #colission bird
        game_active = check_collision(pipe_list)
        #draw pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        #Score
        pipe_score_check()
        score_display('main_game')
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')

    #draw floor
    draw_floor()
    #move floor
    floor_x_pos -= 1
    #animation floor
    if (floor_x_pos <= -576):
        floor_x_pos = 0
    
    pygame.display.update()
    
    #Frame rate update
    clock.tick(60)