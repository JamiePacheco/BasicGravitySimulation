import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

class Ball:
    def __init__(self, pos : tuple, svel : tuple = (2, 2), saccel : tuple = (0.0001, 0.0001), smass = 10, color = "white"):
        self.pos : pygame.Vector2 = pygame.Vector2(pos[0], pos[1])
        self.xvel = svel[0]
        self.yvel = svel[1]
        self.xaccel = saccel[0]
        self.yaccel = saccel[1]
        self.mass = smass
        self.color = color
        self.shape = pygame.draw.circle(screen, self.color, self.pos, 20)

        
    def draw_ball(self):
        self.update_ball_velocity()
        self.update_ball(screen)
        self.shape = pygame.draw.circle(screen, self.color, self.pos, 20)

    def update_ball(self, screen : pygame.Surface):
        new_x_pos = self.pos.x + self.xvel
        new_y_pos = self.pos.y + self.yvel
        if  new_y_pos - 20 <= 0 or new_y_pos + 20 >= screen.get_height():
            self.yvel *= -1
            self.yaccel *= -1
            new_y_pos = self.pos.y + self.yvel

        if new_x_pos - 20 <= 0 or new_x_pos + 20 >= screen.get_width():
            self.xvel *= -1
            self.xaccel *= -1
            new_x_pos = self.pos.x + self.xvel

        self.pos.x = new_x_pos
        self.pos.y = new_y_pos

        self.get_pos()

    def update_ball_velocity(self):
        self.xvel+=self.xaccel
        self.yaccel+=self.yaccel

    def ball_collision(self, ydir = 1, xdir = 1):
        self.yvel *= ydir
        self.yaccel *= ydir
        self.xvel *= xdir
        self.xaccel *= xdir

    def get_pos(self):
        print(f"x: {self.pos.x} y: {self.pos.y}")

def colliding(balls : list[Ball]):

    balls_to_compare = balls.copy()

    while len(balls_to_compare) > 1:
        currball = balls_to_compare.pop(0)
        for ball in balls_to_compare:
            if currball.shape.colliderect(ball.shape):
                pos_xvel = (currball.xvel > 0 and ball.xvel > 0)
                neg_xvel =  (currball.xvel < 0 and ball.xvel < 0)

                pos_yvel = (currball.yvel > 0 and ball.yvel > 0)
                neg_yvel = (currball.yvel < 0 and ball.yvel < 0)

                samex =  pos_xvel or neg_xvel
                samey = pos_yvel or neg_yvel

            
                if samey and samex:
                    if (currball.pos.x < ball.pos.x and pos_xvel) or (currball.pos.x > ball.pos.x and neg_xvel):
                        currball.ball_collision(1, -1)
                    elif (ball.pos.x < currball.pos.x and pos_xvel) or (ball.pos.x > currball.pos.x and neg_xvel):
                        ball.ball_collision(1, -1)
                    if (currball.pos.y < ball.pos.y and pos_yvel) or (currball.pos.y > ball.pos.y and neg_yvel):
                        currball.ball_collision(-1, 1)
                    elif (ball.pos.y < currball.pos.y and pos_yvel) or (ball.pos.y > currball.pos.y and neg_yvel):
                        ball.ball_collision(-1, 1)
                    continue

                currball.ball_collision(-1 if not samey else 1, -1 if not samex else 1)
                ball.ball_collision(-1 if not samey else 1, -1 if not samex else 1)


balls = [
    Ball((screen.get_width()/2 - 100, screen.get_height()/2), color="white"),
    Ball((screen.get_width()/2 + 100, screen.get_height()/2), color = "green"),
    Ball((screen.get_width()/2, screen.get_height()/2 + 300), color = "blue"),
    Ball((screen.get_width()/2, screen.get_height()/2 - 300), color = "red")
]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")

    for ball in balls:
        ball.draw_ball()
    colliding(balls)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()