import pygame
from pygame.locals import *

import random as rd

# constants

WIDTH = 1200
HEIGHT = 600
BORDER = 20
VELOCITY = 5

pygame.init()

# display
lives_font = pygame.font.SysFont('helvetica', 14, True, False)
score_font = pygame.font.SysFont('helvetica', 12, False, False)
game_over_font = pygame.font.SysFont('helvetica', 30, True, False)

# colors
bg_color = pygame.Color("black")
fg_color = pygame.Color("white")
hud_color = pygame.Color("yellow")
go_color = pygame.Color("red")
size = (WIDTH, HEIGHT)

# ball params
ball_start_x = WIDTH - 150
ball_start_y = lambda: rd.randint(0, HEIGHT)
ball_start_vx = -VELOCITY
ball_start_vy = VELOCITY

# other
miss_sound = pygame.mixer.Sound('sounds/scream.wav')
lives = 5
score = old_score = 0
score_points = 1

# screen
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Squash pong')


# entities
class Ball(pygame.sprite.Sprite):
    RADIUS = 10

    def __init__(self, x, y, vx, vy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/ball.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.sound = pygame.mixer.Sound('sounds/tock.mp3')

        self.rect.center = (x, y)
        self.vx = vx
        self.vy = vy

    def tock(self):
        self.sound.play()

    def hit(self, r):
        return self.rect.colliderect(r)

    def update(self):
        self.rect.center = (self.rect.centerx + self.vx, self.rect.centery + self.vy)

    def respawn(self):
        self.rect.center = (ball_start_x, ball_start_y())
        self.vx = -VELOCITY
        self.vy = VELOCITY


class Paddle(pygame.sprite.Sprite):
    WIDTH = 20
    HEIGHT = 150

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(fg_color)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH - self.WIDTH

    def update(self):
        self.rect.centery = pygame.mouse.get_pos()[1]


class TopBorder(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WIDTH, 20))
        self.image.fill(fg_color)
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.left = 0


class BottomBorder(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WIDTH, 20))
        self.image.fill(fg_color)
        self.rect = self.image.get_rect()
        self.rect.top = HEIGHT - 20
        self.rect.left = 0


class LeftBorder(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, HEIGHT))
        self.image.fill(fg_color)
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.left = 0


# create objects
ball = Ball(ball_start_x, ball_start_y(), ball_start_vx, ball_start_vy)
paddle = Paddle()
top_border = TopBorder()
bottom_border = BottomBorder()
left_border = LeftBorder()

bg = pygame.Surface(size=screen.get_size())
bg.fill(bg_color)

sprite_group_elements = pygame.sprite.Group()
sprite_group_elements.add(ball)
sprite_group_elements.add(paddle)

sprite_group_borders = pygame.sprite.Group()
sprite_group_borders.add(top_border)
sprite_group_borders.add(bottom_border)
sprite_group_borders.add(left_border)

pygame.draw.rect(screen, fg_color, pygame.Rect((0, 0), (WIDTH, BORDER)))
pygame.draw.rect(screen, fg_color, pygame.Rect(0, 0, BORDER, HEIGHT))
pygame.draw.rect(screen, fg_color, pygame.Rect(0, HEIGHT - BORDER, WIDTH, BORDER))

game_over_text = game_over_font.render("GAME OVER", False, go_color)

# action -> alter
game_runs = True
clock = pygame.time.Clock()
framerate = 200
pygame.time.set_timer(USEREVENT, 10)


# global methods
def update_hud():
    pygame.draw.rect(screen, bg_color, pygame.Rect((30, 30), (100, 100)))

    if lives >= 0:
        lives_text = lives_font.render(f"Lives: {lives}", False, hud_color)
        screen.blit(lives_text, (30, 30))
    else:
        lives_text = lives_font.render(f"Lives: {0}", False, hud_color)
        screen.blit(lives_text, (30, 30))

    score_text = score_font.render(f"Score: {score}", False, hud_color)
    screen.blit(score_text, (30, 60))


# gameloop
while game_runs:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_runs = False
        elif event.type == USEREVENT:
            if ball.hit(paddle):
                ball.tock()
                ball.vx = -ball.vx
                score += score_points
                if score >= old_score + 5:
                    old_score = score
                    score_points *= 2
                    ball.vx -= 2
                    ball.vy += 2
                ball.update()
            elif ball.hit(left_border):
                ball.tock()
                ball.vx = -ball.vx
                ball.update()
            elif ball.hit(top_border):
                ball.tock()
                ball.vy = -ball.vy
                ball.update()
            elif ball.hit(bottom_border):
                ball.tock()
                ball.vy = -ball.vy
                ball.update()
            else:
                screen.blit(bg, (0, 0))
                sprite_group_elements.update()
                sprite_group_elements.draw(screen)
                sprite_group_borders.draw(screen)
                pygame.time.set_timer(USEREVENT, 10)
                update_hud()

            # score and gameover
            if ball.rect.centerx > WIDTH:
                lives -= 1
                if lives > 0:
                    ball.respawn()
                    miss_sound.play()
                    score_points = 1
                elif lives <= 0:
                    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 100))
                    ball.kill()

    # clock tick
    clock.tick(framerate)
    pygame.display.flip()

pygame.quit()
