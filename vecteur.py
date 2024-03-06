import math
import pygame


def vecteur(screen, x, y, t, n, c):
    """
     Dessine un vecteur rotatif n et de paramètre c
    :param screen: support d'affichage
    :param x: origine x
    :param y: origine y
    :param t: temp
    :param n:
    :param c: coordonnée de départ
    :return x, y: fin du vecteur
    """

    origine = pygame.Vector2(x, y)
    radius = math.sqrt(c[0]**2+c[1]**2)
    xab = abs(c[0])
    if c[0] != 0:
        angle = math.acos((abs(c[0])*xab)/(xab*radius))
    else:
        if c[1] > 0:
            angle = 90
        elif c[1] < 0:
            angle = 270
        else:
            return 0, 0
    x += radius * math.cos(n * t * (math.pi * 2)+angle)
    y += radius * math.sin(n * t * (math.pi * 2)+angle)
    fin = pygame.Vector2(x, y)
    pygame.draw.line(screen, "black", to_pygame(origine), to_pygame(fin))
    return x, y


def to_pygame(pos):
    pos.x += 640
    pos.y = -1*pos.y + 360
    return pos


def from_pygame(pos):
    pos.x += 640
    pos.y = -1*pos.y + 360
    return pos


def to_pygame_vec(x, y):
    x += 640
    y = -1*y + 360
    return pygame.Vector2(x, y)


def point(screen, pos):
    pygame.draw.rect(screen, "black", [to_pygame(pos), pygame.Vector2(2, 2)])