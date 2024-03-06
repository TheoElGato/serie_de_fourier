# Example file showing a circle moving on screen

from dessin import *
from vecteur import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
t = 0

presition = 500
k = 0
draw = []


para = []
n = 0
for i in range(presition):
    para.append(parametre(n))
    n = n + (-1) ** i * (i + 1)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    x, y = 0, 0
    n = 0
    for i in range(presition):
        oldx, oldy = x, y
        x, y = vecteur(screen, oldx, oldy, t, n, para[i])
        n = n + ((-1) ** i) * (i + 1)

    draw.append([x, y])
    for i in draw:
        point(screen, pygame.Vector2(i[0], i[1]))
    if len(draw) > 600:
        draw.pop(0)

    # for i in range(len(figure)):
    #    point(screen, pygame.Vector2(path(i)))


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    t += 0.002
    if t >= 1:
        t = 0

pygame.quit()
