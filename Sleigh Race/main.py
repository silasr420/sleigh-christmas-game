# Import Libraries
import pygame
import random
import time
from pygame import mixer

#initialize pygame
pygame.init()
mixer.init()

#game window dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sleigh Race')


#set frame rate
clock = pygame.time.Clock()
FPS = 60

play_music = ("assets/play_music.mp3")
home_music = ("assets/home_music.mp3")
mixer.music.set_volume(0.5)



heart_img = pygame.image.load('assets/heart.png')
sleigh_img = pygame.image.load('assets/sleigh.png').convert_alpha()

play_bg = pygame.image.load('assets/playing_bg.png')
home_bg = pygame.image.load('assets/home_bg.png')

heart_img = pygame.transform.scale(heart_img, (48, 48))

play_bg = pygame.transform.scale(play_bg, (2000, 600))
home_bg = pygame.transform.scale(home_bg, (1000, 600))

score_font = pygame.font.SysFont('Britannic', 22)

delay = 0

sleigh_x = 280
sleigh_y = 280

sleigh_y_vel = 0

sleigh_width = 256
sleigh_height = 104
sleigh_img = pygame.transform.scale(sleigh_img, (sleigh_width, sleigh_height))

lives = 3
score = 0

bg_x = 0
bg_y = 0
bg_x_vel = 1

desired_music = home_music
current_music = None


obstacles = []
obstacle_types = []
OBSTACLE_SPAWN_DELAY = 75

heart_rect = heart_img.get_rect()
game_state = "home"


def get_sleigh_hitboxes(x, y):
    hitboxes = []

    main_hitbox = pygame.Rect(
        x + 10,   # offset from left
        y + 50,   # offset from top
        200,      # width
        38        # height
    )
    hitboxes.append(main_hitbox)

    deer_front = pygame.Rect(
        x + 220,
        y,
        30,
        90
    )
    hitboxes.append(deer_front)

    idk_what_its_called = pygame.Rect(
        x + 20,
        y + 85,
        120,
        20
    )
    hitboxes.append(idk_what_its_called)
    
    santa_head = pygame.Rect(
        x + 30,
        y + 20,
        53,
        30
    )
    hitboxes.append(santa_head)

    return hitboxes 

 



while True:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()
    if game_state == "playing":
        desired_music = play_music
        bg_x += bg_x_vel
        
        if bg_x >= 2000:
            bg_x = 0
        screen.blit(play_bg, (-bg_x, 0))
        screen.blit(play_bg, (-bg_x + 2000, 0))

        
        
        
        #screen.fill((40, 40, 255))
        
        sleigh_hitboxes = get_sleigh_hitboxes(sleigh_x, sleigh_y)
        
        #debugging hitboxes
        #for box in sleigh_hitboxes:
            #pygame.draw.rect(screen, (255, 0, 0), box, 2)
        
        
        
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            sleigh_y_vel = -4
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            sleigh_y_vel = 4    
        else:
            sleigh_y_vel = 0

        sleigh = screen.blit(sleigh_img, (sleigh_x, sleigh_y))
        
        sleigh_y += sleigh_y_vel
        if sleigh_y < 0:
            sleigh_y = 0
            
        if sleigh_y > SCREEN_HEIGHT - sleigh_height:
            sleigh_y = SCREEN_HEIGHT - sleigh_height
            
        
        if delay % OBSTACLE_SPAWN_DELAY == 0:
            ob_y = random.randint(0, SCREEN_HEIGHT - 75)
            if random.choice([True, False]):
                obstacle = pygame.Rect(SCREEN_WIDTH, ob_y, 75, 100)
            else:
                obstacle = pygame.Rect(SCREEN_WIDTH, ob_y, 75, 75)
            obstacles.append(obstacle)
            
        for obstacle in obstacles[:]:
            obstacle.x -= 5
            pygame.draw.rect(screen, (0, 255, 0), obstacle)
            
            for box in sleigh_hitboxes:
                if obstacle.colliderect(box):
                    if lives > 1:
                        lives -= 1
                        obstacles.remove(obstacle)
                    else:
                        game_state = "home"
                    
            if obstacle.right == sleigh_x + 250:
                score += 1
                

            if obstacle.right < 0:
                obstacles.remove(obstacle)
                
        
        if lives == 3:
            screen.blit(heart_img, (10, 10))
            screen.blit(heart_img, (68, 10))
            screen.blit(heart_img, (126, 10))
        elif lives == 2:
            screen.blit(heart_img, (10, 10))
            screen.blit(heart_img, (68, 10))
        elif lives == 1:
            screen.blit(heart_img, (10, 10))
            
        score_text = score_font.render("Score: " + str(score), True, (255, 255, 255))
        score_text_width = score_text.get_width()
        
        screen.blit(score_text, ((SCREEN_WIDTH - score_text_width) - 10, 10))
        
    
    elif game_state == "home":
        screen.blit(home_bg, (0, 0))
        desired_music = home_music
        
        space_text = score_font.render("Press space to play", True, (0, 0, 0))
        screen.blit(space_text,(400, 545))
        
        obstacles = []
        delay = 0
        lives = 3
        score = 0
        sleigh_x = 280
        sleigh_y = 280

        sleigh_y_vel = 0

        if keys[pygame.K_SPACE]:
            game_state = "playing"
        
    if desired_music != current_music:
        pygame.mixer.music.load(desired_music)
        pygame.mixer.music.play(-1)
        current_music = desired_music
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
    pygame.display.update()
    delay += 1
    print(game_state)
            
            
            