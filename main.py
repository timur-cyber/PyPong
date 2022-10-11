import pygame
from game_objects import BLACK, Game, Button

# Initialize game
pygame.init()

# Screen Settings
SCREEN_RESOLUTION = (720, 480)
screen = pygame.display.set_mode(SCREEN_RESOLUTION)
screen_color_rgb = BLACK

# Title and Icon
pygame.display.set_caption("PyPong")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Setting game
game = Game(screen)
game.set_game()

start_btn = Button('Start game', (250, 200), game)

running = True
while running:
    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
            running = False
        if key[pygame.K_SPACE]:
            start_btn.visible = False
            game.started = True
        start_btn.on_event(event)

    start_btn.show(screen)
    if game.started:
        game.start_game()

    # Screen refresh
    pygame.display.update()
    screen.fill(screen_color_rgb)
