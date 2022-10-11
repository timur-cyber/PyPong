import random
import time

import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Button(object):
    visible = True

    def __init__(self, text, pos, game, font_family="Arial", font_size=50):
        self.game = game
        self.x, self.y = pos
        self.font = pygame.font.SysFont(font_family, font_size)
        self.text = self.font.render(text, True, BLACK)
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(WHITE)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def on_event(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.visible = False
                    self.game.started = True

    def show(self, screen):
        if self.visible:
            screen.blit(self.surface, (self.x, self.y))


class Counter(object):
    def __init__(self, text, pos, font_family="Arial", font_size=50):
        self.x, self.y = pos
        self.font = pygame.font.SysFont(font_family, font_size)
        self.text = self.font.render(text, True, WHITE)
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(BLACK)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def change_text(self, text):
        self.text = self.font.render(text, True, WHITE)
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(BLACK)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])


class Player(object):
    default_v = 7

    def __init__(self, x, y, h=25, w=100):
        self.rect = pygame.rect.Rect(x, y, h, w)
        self.points = 0

    def handle_keys(self):
        key = pygame.key.get_pressed()
        dist = self.default_v
        if key[pygame.K_UP] or key[pygame.K_w]:
            if not self.rect.y <= 0:
                self.rect.move_ip(0, -dist)
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            if not self.rect.y >= 380:
                self.rect.move_ip(0, +dist)

    def act(self):
        self.handle_keys()

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)


class Bot(Player):
    default_v = 4

    def __init__(self, x, y, ball):
        super().__init__(x, y)
        self.ball = ball

    def ai_movement(self, ball):
        dist = self.default_v
        if abs(ball.circle.y - self.rect.y) > dist + 5:
            if ball.circle.y >= self.rect.y:
                if not self.rect.y >= 380:
                    self.rect.move_ip(0, +dist)
            elif ball.circle.y <= self.rect.y:
                self.rect.move_ip(0, -dist)

    def act(self):
        self.ai_movement(self.ball)


class Ball(object):
    default_v = 2
    acceleration = 0.25
    balling = False
    timer = None
    acceleration_timer = None

    def __init__(self, surface):
        self.surface = surface
        screen_res = surface.get_size()
        self.CENTER = (screen_res[0] // 2, screen_res[1] // 2)
        self.circle = pygame.draw.circle(surface, WHITE, self.CENTER, 10)
        self.velocity = self.default_v
        self.movement_x = self.velocity
        self.movement_y = self.velocity

    def acceleration_behaviour(self):
        if not self.acceleration_timer:
            self.acceleration_timer = time.time()
        else:
            current = time.time()
            if (current - self.acceleration_timer) >= 1:
                self.velocity += self.acceleration
                self.acceleration_timer = None

    def ball_restarter(self):
        if not self.balling:
            if not self.timer:
                self.timer = time.time()
            else:
                current = time.time()
                if (current - self.timer) >= 0.75:
                    self.balling = True
                    self.timer = None
                    self.acceleration_timer = None
            return

    def motion(self, player1, player2, scoreboard):
        pygame.draw.circle(self.surface, WHITE, self.circle.center, 10)

        self.acceleration_behaviour()
        diff = random.randint(0, 2)
        if self.circle.x <= 0:
            player1.points += 1
            self.movement_x = self.velocity
            self.movement_y += diff
            self.circle.center = self.CENTER
            self.balling = False
            scoreboard.count_player1(player1.points)
        if self.circle.x >= 700:
            player2.points += 1
            self.movement_x = -self.velocity
            self.movement_y += diff
            self.circle.center = self.CENTER
            self.balling = False
            scoreboard.count_player2(player2.points)
        if self.circle.y <= 0:
            self.movement_y = self.velocity
            self.movement_y += diff
        if self.circle.y >= 460:
            self.movement_y = -self.velocity
            self.movement_y += diff
        if self.circle.colliderect(player1):
            self.movement_x = -self.velocity
            self.movement_y += diff
        if self.circle.colliderect(player2):
            self.movement_x = self.velocity
            self.movement_y += diff

        if not self.balling:
            self.velocity = 2
            self.acceleration_timer = None
            self.movement_x = self.velocity if random.randint(0, 1) == 1 else -self.velocity
            if not self.timer:
                self.timer = time.time()
            else:
                current = time.time()
                if (current - self.timer) >= 0.75:
                    self.balling = True
                    self.timer = None
            return

        self.circle.center = (self.circle.center[0] + self.movement_x, self.circle.center[1] + self.movement_y)
        pygame.draw.circle(self.surface, WHITE, self.circle.center, 10)

    def player1_scored(self):
        if self.circle.x <= 0:
            return True
        else:
            return False

    def player2_scored(self):
        if self.circle.x >= 700:
            return True
        else:
            return False

    def draw(self):
        pygame.draw.circle(self.surface, WHITE, self.circle.center, 10)


class ScoreBoard(object):
    left_pos = (240, 50)
    right_pos = (450, 50)

    def __init__(self):
        self.counter_left = Counter('0', self.left_pos)
        self.counter_right = Counter('0', self.right_pos)

    def count_player1(self, points):
        self.counter_right.change_text(str(points))

    def count_player2(self, points):
        self.counter_left.change_text(str(points))

    def draw(self, surface):
        surface.blit(self.counter_left.surface, self.left_pos)
        surface.blit(self.counter_right.surface, self.right_pos)


class Game(object):
    started = False

    def __init__(self, surface):
        self.surface = surface
        self.ball = Ball(self.surface)
        self.scoreboard = ScoreBoard()
        self.player1 = None
        self.player2 = None

    def set_game(self):
        self.player1 = Player(600, 250)
        self.player2 = Bot(100, 250, self.ball)

    def set_p2p_game(self):
        self.player1 = Player(600, 250)
        self.player2 = Player(100, 250)

    def start_game(self):
        self.scoreboard.draw(self.surface)
        self.player1.draw(self.surface)
        self.player1.act()
        self.player2.draw(self.surface)
        self.player2.act()
        self.ball.motion(self.player1, self.player2, self.scoreboard)
        self.ball.draw()
