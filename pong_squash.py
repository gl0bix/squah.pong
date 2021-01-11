import pygame

#vars

WIDTH = 1200
HEIGHT = 600
BORDER = 20
VELOCITY = 1

#classes
class Ball:
    
    RADIUS = 10

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def show(self, color):
        global screen
        pygame.draw.circle(screen, color, (self.x, self.y), self.RADIUS)

    def update(self, is_paddled):
        global bg_color, fg_color

        new_x = self.x + self.vx
        new_y = self.y + self.vy

        if new_x < BORDER + self.RADIUS:
            self.vx = -self.vx
        elif new_y < BORDER + self.RADIUS or new_y > HEIGHT - BORDER - self.RADIUS:
            self.vy = -self.vy
        elif is_paddled:
            self.vx = -self.vx
        else:
            self.show(bg_color)
            self.x += self.vx
            self.y += self.vy
            self.show(fg_color)

class Paddle:
    WIDTH = 20
    HEIGHT = 100

    def __init__(self, y):
        self.y = y

    def show(self, color):
        global screen
        pygame.draw.rect(screen, color, pygame.Rect((WIDTH-self.WIDTH, self.y - self.HEIGHT//2, self.WIDTH, self.HEIGHT)))

    def update(self):
        self.show(bg_color)
        self.y = pygame.mouse.get_pos()[1]
        self.show(fg_color)

#create objects
ball_start_x = WIDTH-Ball.RADIUS-100
ball_start_y = HEIGHT//2
ball_start_vx = -VELOCITY
ball_start_vy = VELOCITY
ball = Ball(ball_start_x, ball_start_y, ball_start_vx, ball_start_vy)
paddle = Paddle(HEIGHT//2)

#init
pygame.init()

lives_font = pygame.font.SysFont('helvetica', 14, True, False)
score_font = pygame.font.SysFont('helvetica', 12, False, False)
game_over_font = pygame.font.SysFont('helvetica', 30, True, False)

#screen
screen  = pygame.display.set_mode((WIDTH, HEIGHT))
bg_color = pygame.Color("black")
fg_color = pygame.Color("white")
hud_color = pygame.Color("yellow")
go_color = pygame.Color("red")

pygame.draw.rect(screen, fg_color, pygame.Rect((0, 0), (WIDTH, BORDER)))
pygame.draw.rect(screen, fg_color, pygame.Rect(0, 0, BORDER, HEIGHT))
pygame.draw.rect(screen, fg_color, pygame.Rect(0, HEIGHT - BORDER, WIDTH, BORDER))

ball.show(fg_color)
paddle.show(fg_color)
lives = 5
score = 0

game_over_text = game_over_font.render("GAME OVER", False, go_color)

game_runs = True
clock = pygame.time.Clock()

#global methods
def update_hud(lives, score):
    pygame.draw.rect(screen, bg_color, pygame.Rect((30,30), (100, 100)))

    if lives >= 0:
        lives_text = lives_font.render(f"Lives: {lives}", False, hud_color)
        screen.blit(lives_text, (30, 30))
    else:
        lives_text = lives_font.render(f"Lives: {0}", False, hud_color)
        screen.blit(lives_text, (30, 30))

    score_text = score_font.render(f"Score: {score}", False, hud_color)
    screen.blit(score_text, (30, 60))

#gameloop
while game_runs:
    is_collision = False
    old_ball_vx = ball.vx

    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        game_runs = False

    pygame.display.flip()

# update paddle and ball
    if ball.x > WIDTH - BORDER \
            and ball.x < WIDTH \
            and ball.y > paddle.y \
            and ball.y < (paddle.y + paddle.HEIGHT):
        ball.update(True)
    else:
        ball.update(False)
    paddle.update()

    if ball.x >= WIDTH:
        lives -= 1
        if lives > 0:
            ball = Ball(ball_start_x, ball_start_y, ball_start_vx, ball_start_vy)

    #show score
    if ball.vx < 0 and ball.vx != old_ball_vx:
        score += 1

    update_hud(lives, score)

    #gameover
    if lives <= 0:
        screen.blit(game_over_text, (WIDTH//2 -100, HEIGHT//2 - 100))

    #clock tick
    time_passed = clock.tick(1000)

pygame.quit()

