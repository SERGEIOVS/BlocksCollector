import pygame
from random import randrange as rnd
pygame.font.init()

RED = (255 , 0 , 0)

fontsize = 20

WIDTH, HEIGHT = 800 , 600

collected = 0

fps = 60

sc = pygame.display.set_mode((WIDTH , HEIGHT))

# paddle settings
paddle_w = WIDTH / 5
paddle_h = 50
paddle_speed = 15
paddle = pygame.draw.rect(sc , (0, 255 , 0) , (WIDTH / 5 , HEIGHT - 10 , 100 , paddle_h))


paddle2_w = WIDTH / 5
paddle2_h = 50
paddle2_speed = 15
paddle2 = pygame.draw.rect(sc , (0, 255 , 0) , (WIDTH / 5 , HEIGHT - 10 , 100 , paddle_h))

# ball settings
ball_radius = fontsize / 2
ball_speed = paddle_speed / 3
ball_rect = int(ball_radius * 2 ** 0.1)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect) , HEIGHT // 2 , ball_rect , ball_rect)

dx , dy = 1 , -1

pausegame = 0
paddles_num_horisontal = 1
paddles_num_vertical = 1

paddles_num_horisontal1 = 2
paddles_num_vertical1 = 1

level = 1

hearts = 5

music_state = '+'
main_font = 'Arial'
f1 = pygame.font.SysFont(main_font, fontsize)

text1 = f1.render('level : ' + str(level) + '  ' + 'hearts : ' + str(hearts) + ' ' + 'coins : ' + str(collected) + '   ' + '< a   d >   q - quit' , True,(RED))

PAUSE_TEXT = 'PAUSE'

pause = f1.render(PAUSE_TEXT, True,(RED))

musicstate = f1.render('MUSIC VOLUME ' + str(music_state) , True,(RED))

game_over = f1.render('pause' , True,(RED))

GameOver = 0
game_over_text = 'GAME OVER! PLAY? x - play'

# blocks settings

block_list  = [pygame.Rect(fontsize + 10 + 80  * i , fontsize + fontsize / 2 + 10 + 80 * j, WIDTH / fontsize, WIDTH  / fontsize ) for i in range(paddles_num_horisontal) for j in range(paddles_num_vertical)]
block_list1 = [pygame.Rect(fontsize + 10 + 80  * i , fontsize + fontsize / 2 + 10 + 80 * j, WIDTH / fontsize , WIDTH / fontsize ) for i in range(paddles_num_horisontal1) for j in range(paddles_num_vertical1)]

color_list = [(RED) for i in range(paddles_num_horisontal) for j in range(paddles_num_vertical)]

color_list1 = [(255 , 255 , 0) for i in range(paddles_num_horisontal1) for j in range(paddles_num_vertical1)]

pygame.init()

clock = pygame.time.Clock()

bgmusic = pygame.mixer.music.load('music/bensound-birthofahero.mp3')

music_volume = 0.1

pygame.mixer.music.set_volume(music_volume)
start_music = 1
if start_music == 1 and music_volume >= 0:
    pygame.mixer.music.play(-1)

sound1 = pygame.mixer.Sound('music/select1.wav')

# backgrund image
img = pygame.image.load('bg/1.jpg').convert()


sc.blit(text1, (10, 50))
if GameOver == 1:
    pausegame = 1
    
sc.blit(game_over, (WIDTH / 2 , HEIGHT / 2))
pygame.display.update()

def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sc.blit(img, (0, 0))

    # drawing world
    [pygame.draw.rect(sc, color_list[color] , block) for color, block in enumerate(block_list)]

    [pygame.draw.rect(sc, color_list1[color1] , block1) for color1, block1 in enumerate(block_list1)]

    pygame.draw.rect(sc, pygame.Color((0,255,0)) , paddle , 0 , 5)

    pygame.draw.circle(sc, pygame.Color('white') , ball.center , ball_radius)

    pygame.draw.rect(sc, (255, 255, 255) , (0,0,int(WIDTH),fontsize + fontsize / 2))

    sc.blit(text1, (0 , 0))

    if pausegame == 1 :
        ball_speed = 0
        paddle_speed = 0
        pause = f1.render(PAUSE_TEXT , True,(RED))
        sc.blit(pause, (WIDTH / 2 , HEIGHT / 2))

    # ball movement
    if pausegame == 0 and hearts >= 1:
        ball.x += ball_speed * dx
        ball.y += ball_speed * dy

    # collision left right
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius * 2 :
        dx = -dx

    # collision top
    if ball.centery < ball_radius + 30:
        dy = -dy

    # collision paddle
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx , dy , ball , paddle)


        # if dx > 0:
        #     dx, dy = (-dx, -dy) if ball.centerx < paddle.centerx else (dx, -dy)
        # else:
        #     dx, dy = (-dx, -dy) if ball.centerx >= paddle.centerx else (dx, -dy)

    # collision blocks

    hit_index = ball.collidelist(block_list)
    hit_index1 = ball.collidelist(block_list1)

    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx , dy = detect_collision(dx, dy, ball, hit_rect)
        sound1.play()

    if hit_index1 != -1:
        hit_rect = block_list1.pop(hit_index1)
        hit_color1 = color_list1.pop(hit_index1)
        dx, dy = detect_collision(dx , dy , ball , hit_rect)
        sound1.play()
        collected += 1
        text1 = f1.render('level : ' + str(level) + '  ' + 'hearts : ' + str(hearts) + ' ' + 'coins : ' + str(collected) + '   ' + '< a   d >   q - quit' , True,(RED))

    # win, game over
    if ball.bottom > HEIGHT and hearts >= 0:
        hearts -= 1
        ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
        text1 = f1.render('level : ' + str(level) + '  ' + 'hearts : ' + str(hearts) + ' ' + 'coins : ' + str(collected) + '   ' + '< a   d >   q - quit' , True,(RED))

    elif not len(block_list1):
        
        sound1.play()
        
        level +=1
        
        text1 = f1.render('level : ' + str(level) + '  ' + 'hearts : ' + str(hearts) + ' ' + 'coins : ' + str(collected) + '   ' + '< a   d >   q - quit' , True,(RED))
        
        paddles_num_vertical1 += 1
        
        block_list  = [pygame.Rect(fontsize + 10 + 80  * i , fontsize + fontsize / 2 + 10 * level  + 80 * j, WIDTH / fontsize, WIDTH  / fontsize ) for i in range(paddles_num_horisontal) for j in range(paddles_num_vertical)]
        block_list1 = [pygame.Rect(fontsize + 10 + 80  * i , fontsize + fontsize / 2  + 10 * level + 80 * j, WIDTH / fontsize , WIDTH / fontsize ) for i in range(paddles_num_horisontal1) for j in range(paddles_num_vertical1)]
        
        color_list = [(255,0,0) for i in range(paddles_num_horisontal) for j in range(paddles_num_vertical)]
        color_list1 = [(255,255,0) for i in range(paddles_num_horisontal1) for j in range(paddles_num_vertical1)]

    # control
    key = pygame.key.get_pressed()
    if pausegame == 0  and hearts >= 1:
        if key[pygame.K_a] and paddle.left > 0:
            paddle.left -= paddle_speed

        if key[pygame.K_d] and paddle.right < WIDTH and hearts >= 1:
            paddle.right += paddle_speed
    
    if pausegame == 1:
        pause = f1.render(PAUSE_TEXT , True,(RED))
        sc.blit(pause, (WIDTH / 2 , HEIGHT / 2))

    if hearts <= 1:
        pause = f1.render( str(game_over_text), True,(RED))
        sc.blit(pause, (WIDTH / 2 - int(len(main_font) / 2) , HEIGHT / 2))

    if key[pygame.K_q]:
        quit()
    
    if key[pygame.K_DOWN]:
        music_state = '-'
        music_volume -= 0.01
        pygame.mixer.music.set_volume(music_volume)
        
        musicstate = f1.render('MUSIC VOLUME ' + str(music_state) , True,(RED))
        
        sc.blit(musicstate , (WIDTH / 2 , HEIGHT / 2))

    if key[pygame.K_UP]:
        music_state = '+'
        music_volume += 0.01
        pygame.mixer.music.set_volume(music_volume)
        
        musicstate = f1.render('MUSIC VOLUME ' + str(music_state) , True,(RED))
        
        sc.blit(musicstate, (WIDTH / 2 , HEIGHT / 2))
    
    if key[pygame.K_f]:
        pygame.display.toggle_fullscreen()
    
    if key[pygame.K_ESCAPE]:
        pausegame    = 1
        paddle_speed = 0
        ball_speed   = 0

    if key[pygame.K_p]:
        pausegame    = 0
        paddle_speed = 15
        ball_speed   = paddle_speed / 3

    if key[pygame.K_x]:
        pausegame = 0
        hearts = 5
        ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect) , HEIGHT // 2 , ball_rect , ball_rect)
        paddle_speed = 15
        ball_speed   = paddle_speed / 3

    



    # update screen
    pygame.display.update()
    clock.tick(fps) 