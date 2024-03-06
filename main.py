# Example file showing a circle moving on screen
import dessin
from settings import Settings
from dessin import *
from vecteur import *

s = Settings()
config = s.wait()

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

print(config)
f = Figure(config['dp'], coords='float', tri=None)
f.open(config['path'])
figure = f.points
path = dessin.Dessin(screen, int(len(figure) * config['nbVect'] * config['']), figure)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    path.draw_figure(t)

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
