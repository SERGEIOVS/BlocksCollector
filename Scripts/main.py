import pygame
from random import randrange as rnd
pygame.font.init()

WIDTH, HEIGHT = 800, 600
fps = 60

# paddle settings
paddle_w = WIDTH/3
paddle_h = HEIGHT/20
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)

# ball settings
ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.1)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1

paddles_num_horisontal = 1
paddles_num_vertical = 1

level = 1

f1 = pygame.font.Font(None, 36)

text1 = f1.render('level : ' + str(level), True,(180, 0, 0))

# blocks settings
block_list = [pygame.Rect(50 + 80 * i, 50 + 80 * j, 50, 50) for i in range(paddles_num_horisontal) for j in range(paddles_num_vertical)]
color_list = [(255,0,0) for i in range(paddles_num_horisontal) for j in range(paddles_num_vertical)]

pygame.init()

sc = pygame.display.set_mode((WIDTH, HEIGHT))


clock = pygame.time.Clock()

bgmusic = pygame.mixer.music.load('music/bensound-birthofahero.mp3')

pygame.mixer.music.set_volume(0.1)

pygame.mixer.music.play()

sound1 = pygame.mixer.Sound('music/select1.wav')

# backgrund image
img = pygame.image.load('bg/1.jpg').convert()


sc.blit(text1, (10, 50))


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
    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(sc, pygame.Color('yellow'), paddle)
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)

    pygame.draw.rect(sc, (255, 255, 255),(0,0,400, 20))

    sc.blit(text1, (0, 0))

    # ball movement
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy

    # collision left right
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx

    # collision top
    if ball.centery < ball_radius:
        dy = -dy

    # collision paddle
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)

        # if dx > 0:
        #     dx, dy = (-dx, -dy) if ball.centerx < paddle.centerx else (dx, -dy)
        # else:
        #     dx, dy = (-dx, -dy) if ball.centerx >= paddle.centerx else (dx, -dy)

    # collision blocks
    hit_index = ball.collidelist(block_list)

    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)
        sound1.play()

        # special effect
        hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
        pygame.draw.rect(sc, hit_color, hit_rect)
        fps += 2

    # win, game over
    if ball.bottom > HEIGHT:
        print('GAME OVER!')
        exit()



    elif not len(block_list):

        print('WIN!!!')

        sound1.play()

        level +=1

        text1 = f1.render('level : '+str(level), True,(180, 0, 0))


        paddles_num_horisontal += 1

        block_list = [pygame.Rect(10 + 80 * i, 10 + 80 * j, 50, 50) for i in range(paddles_num_horisontal) for j in range(paddles_num_vertical)]

        color_list = [(255, 0, 0) for i in range(paddles_num_horisontal) for j in range(paddles_num_vertical)]

        #[pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]



    # control
    key = pygame.key.get_pressed()
    if key[pygame.K_a] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_d] and paddle.right < WIDTH:
        paddle.right += paddle_speed
    if key[pygame.K_q]:
        quit()

    # update screen
    pygame.display.update()
    clock.tick(fps)
