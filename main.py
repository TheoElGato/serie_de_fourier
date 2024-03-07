from fourier import *
import pygame
from generator import Figure
from settings import *

USER = 0
FOURIER = 1
TWO_PI = pi * 2

x = []
fourierX = []
time = 0
path = []
drawing = []
state = -1


def init(drawing):
    for i in range(len(drawing)):
        x.insert(0, Complex(drawing[i][0], drawing[i][1]))

    fourierX = dft(x)
    debut = fourierX[:int(len(fourierX)/2)]
    fin = fourierX[int(len(fourierX)/2):]
    temp = []
    for i in range(min(len(debut), len(fin))):
        temp.append(debut[i])
        temp.append(fin[-i])

    fourierX = temp
    return fourierX

def epicycles(screen, x, y, rotation, fourier, nbvec):
  for i in range(nbvec):
    prevx = x
    prevy = y
    freq = fourier[i][2]
    radius = fourier[i][3]
    phase = fourier[i][4]
    x += radius * cos(freq * time + phase + rotation)
    y += radius * sin(freq * time + phase + rotation)

    # desiner la ligne
    pygame.draw.line(screen, [0, 0, 0], [x, y], [prevx, prevy] )

  return x, y


s = Settings()
config = s.wait()


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
time = 0


figure = Figure(config['dp'], 'int', None)
figure.open(config['path'])

fourierX = init(figure.points)
nbvec = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill([255, 255, 255])

    # render
    x, y = epicycles(screen, 0, 0, 0, fourierX, nbvec)
    path.append([x, y])
    for i in path:
        pygame.draw.rect(screen, [0, 0, 0], [i[0], i[1], 1, 1])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and nbvec < len(fourierX):
        nbvec += 1
    if keys[pygame.K_s] and nbvec > 0:
        nbvec -= 1




    dt = TWO_PI / len(fourierX)
    time += dt
    if time > TWO_PI:
      time = 0
      path = []


    pygame.display.flip()
    clock.tick(60)

pygame.quit()




