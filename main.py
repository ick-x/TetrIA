# Example file showing a circle moving on screen
import pygame
import tetris2 as t
def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    player_pos = pygame.Vector2(0, screen.get_height() / 2)

    left = False
    right = False
    down = False
    space = False
    keep = False
    rotate = False
    grid = t.Grid()
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(pygame.Color(155,155,155))
        grid.update(screen, 30)
        keys = pygame.key.get_pressed()

        #PRESS LEFT
        if keys[pygame.K_LEFT] and not left:
            grid.move_left()
            left = True
        if not keys[pygame.K_LEFT] and left:
            left = False

        #PRESS RIGHT
        if keys[pygame.K_RIGHT] and not right:
            grid.move_right()
            right = True
        if not keys[pygame.K_RIGHT] and right:
            right = False

        #HOLD DOWN
        if keys[pygame.K_DOWN]:
            grid.move_down()

        #PRESS SPACE
        if keys[pygame.K_SPACE] and not space:
            grid.move_instant()
            space = True
        if not keys[pygame.K_SPACE] and space:
            space = False

        #PRESS R
        if keys[pygame.K_r] and not rotate:
            rotate = True
            grid.rotate()
        if not keys[pygame.K_r] and rotate:
            rotate = False

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000
    pygame.quit()

main()