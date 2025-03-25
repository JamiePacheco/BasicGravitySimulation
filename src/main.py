import pygame
import math

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

GRAV_CONST = 6.67430 * pow(10, -4)
MOON_MASS = 7.34 * pow(10, 22)
EARTH_MASS = 5.97 * pow(10, 24)

DISTANCE_EARTH_MOON = 3.84 * pow(10, 8)

TIMEFRAME = 60

class VectorLine:
    def __init__(self, x_start, y_start, vector : pygame.Vector2):
        self.line = self.update_line(x_start, y_start, vector)

    def update_line(self, x_start, y_start, vector : pygame.Vector2):
        try:
            n_vector = vector.normalize()
            x_comp = n_vector.x * 50
            y_comp = n_vector.y * 50
            return pygame.draw.line(screen, "white", (x_start, y_start), (x_start + x_comp, y_start + y_comp) , width=10)
        except ValueError:
            return

class Ball:
    def __init__(
            self, 
            pos : tuple, 
            svel : tuple = (0, 0), 
            saccel : tuple = (0.00, 0.00), 
            smass = 10,
            radius = 20, 
            color = "white",
            log = False,
            show_vectors = False
        ):
        self.pos : pygame.Vector2 = pygame.Vector2(pos[0], pos[1])
        self.xvel = svel[0]
        self.yvel = svel[1]
        self.xaccel = saccel[0]
        self.yaccel = saccel[1]
        self.mass = smass
        self.color = color
        self.radius = radius


        self.log = log
        self.show_vectors = show_vectors

        self.shape = pygame.draw.circle(screen, self.color, self.pos, self.radius)
        self.grav_force_vector = pygame.Vector2(0, 0)

        if show_vectors:
            self.grav_force_vector_line = VectorLine(self.pos.x, self.pos.y, self.grav_force_vector)
            self.velocity_vector_line = VectorLine(self.pos.x, self.pos.y, pygame.Vector2(self.xvel, self.yvel))

    def draw_ball(self, dt):
        self.update_ball_velocity(dt)
        self.update_ball(screen)
        self.shape = pygame.draw.circle(screen, self.color, self.pos,self.radius)

        if self.show_vectors:
            self.velocity_vector_line.update_line(self.pos.x, self.pos.y, pygame.Vector2(self.xvel, self.yvel))
            self.grav_force_vector_line.update_line(self.pos.x, self.pos.y, self.grav_force_vector)

    def update_ball(self, screen : pygame.Surface):
        new_x_pos = self.pos.x + (self.xvel / TIMEFRAME)
        new_y_pos = self.pos.y + (self.yvel / TIMEFRAME)
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

        if self.log:
            self.get_data()

    def update_ball_velocity(self, dt):
        self.xvel+=(self.xaccel) * dt
        self.yvel+= (self.yaccel) * dt

    def ball_collision(self, ydir = 1, xdir = 1):
        self.yvel *= ydir
        self.yaccel *= ydir
        self.xvel *= xdir
        self.xaccel *= xdir

    def get_data(self):
        print(f"x: {self.pos.x} y: {self.pos.y}")
        print(f"xvel: {self.xvel} yvel: {self.yvel}")
        print(f"xaccel: {self.xaccel} yaccel: {self.yaccel}")

    def calculate_grav_force(self, dt, bodies):
        net_force_x = 0
        net_force_y = 0
        for ball in bodies:
            if ball is self: continue
            dist = self.pos.distance_squared_to(ball.pos)
            dx = ball.pos.x - self.pos.x
            dy = ball.pos.y - self.pos.y
            d_angle = math.atan2(dy, dx)
            grav_accel = ((ball.mass * GRAV_CONST) / (dist))
            g_accel_x = math.cos(d_angle) * grav_accel
            g_accel_y = math.sin(d_angle) * grav_accel
            net_force_x += g_accel_x
            net_force_y += g_accel_y
            if self.log:
                print(f"angle: {d_angle}")
                print(f"distance: {dist}")
                print(f"fgrav: <{g_accel_x}, {g_accel_y}>")
        self.xaccel = net_force_x
        self.yaccel = net_force_y
        self.grav_force_vector.update(x=self.xaccel,y=self.yaccel)
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
    Ball((screen.get_width()/2, screen.get_height()/2 + 275), color="white", svel= (0, 0), radius=2, smass=1000, log = True, show_vectors=False),
    Ball((screen.get_width()/2, screen.get_height()/2 + 300), color = "blue", svel= (80,0), radius=15, smass = 100000, show_vectors=False),
    # Ball((screen.get_width()/2, screen.get_height()/2 + 325), color = "grey", svel=(25, 0), smass=10, radius = 5, log = False, show_vectors=False),
    Ball((screen.get_width()/2, screen.get_height()/2), color = "red", svel= (0,0), radius=20, smass = 10000000, show_vectors=False),
    # Ball((screen.get_width()/2, screen.get_height()/2 - 300), color = "red")
]

while running:

    SPEED_UP = 10
    

    dt = clock.tick(TIMEFRAME) * 0.001 * TIMEFRAME * SPEED_UP

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")

    for ball in balls:
        ball.calculate_grav_force(dt, balls)
        ball.draw_ball(dt)
    # colliding(balls)

    pygame.display.flip()


pygame.quit()