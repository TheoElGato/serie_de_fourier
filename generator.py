from tkinter import *
from xml.dom import minidom
from math import *
from time import sleep

####################################
## Erreur et mise en forme        ##
####################################

class UnknownFileFormat(Exception):
    def __init__(self, message):
        super().__init__(message)

def size(s):
    s = s.replace('pt', '')
    s = s.replace('cm', '')
    s = s.replace('mm', '')
    s = s.replace(' ', '')
    s = int(s)
    return s


class Figure:
    #####################################
    ## Attributs de base de la classe  ##
    #####################################

    def __init__(self, dt, coords = 'int', tri = None):
        self.dt = dt # Paramètre dt pour la distance (en unité svg, soit pixel) entre deux points
        assert coords in ('int', 'float')
        self.coords = coords # Type de rendu des coordonées des points (int ou float)
        assert tri in ('nsoe', None)
        self.trimode = tri # Type de tri
        
    def __getitem__(self, index):
        return self.points[index] # Renvoie le point adressé

    def __len__(self):
        return len(self.points) # Nombre de points

    ######################################
    ## Traitement de fichier            ##
    ######################################

    def open(self, file): ## Pour l'ouverture d'un fichier
        if file[-4:] == '.svg': # Si image
            self.filepath = file
            self.doc = minidom.parse(self.filepath)
            svg_meta = self.doc.getElementsByTagName("svg")[0]
            self.width = size(svg_meta.getAttribute('width'))
            self.height = size(svg_meta.getAttribute('height'))
            self.ComputePoints()

        elif file[-4:] == '.pts': # Si ensemble de points
            self.filepath = file
            self.open_ptsfile()

        else: # En cas de non reconnaissance du format du fichier
            n = len(file) - 1
            try:
                while file[n] != '.':
                    n -= 1
                raise UnknownFileFormat('With extension ' + file[n:])
            except IndexError:
                raise UnknownFileFormat('Without any extension')

    def open_ptsfile(self): ## Ouverture du fichier et traitement des points
        f = open(self.filepath, 'r', encoding = 'utf-8')
        r = f.read()
        f.close()
        if 'int\n' in r:
            self.coords = 'int'
            r = r.replace('int\n', '')
        elif 'float\n' in r:
            self.coords = 'float'
            r = r.replace('float\n', '')

        self.points = []
        r = r.replace('\n', '')
        for pt in r.split('], '):
            if not pt:
                continue

            pt = pt.replace('[', '')
            pt = pt.split(',')
            if self.coords == 'int':
                pt[0], pt[1] = int(pt[0]), int(pt[1])
            else:
                pt[0], pt[1] = float(pt[0]), float(pt[1])

            self.points.append(pt)

    def saveas(self, filename): ## Enregistrement sous forme de fichier texte contenant l'ensemble des points
        if filename[-4:] != '.pts':
            filename += '.pts'

        f = open(filename, 'w', encoding = 'utf-8')
        i = 0
        f.write(self.coords + '\n')
        for p in self.points:
            i += 1
            x, y = p
            f.write('[' + str(x) + ',' + str(y) + '], ')
            if i % 200 == 0:
                f.write('\n')

        f.write('\n')
        f.close()

    #####################################
    ## Décomposition en lignes         ##
    #####################################

    def ComputePoints(self):
        self.points = [] ## Liste contenant tous les points
        self.lines = [] ## Liste contenant toutes les lignes

        # On récupère touts les cercles de l'image svg
        elements = self.doc.getElementsByTagName("circle")
        for i in elements:
            x, y = float(i.getAttribute('cx')), float(i.getAttribute('cy'))
            r = float(i.getAttribute('r'))
            self.points += self.GenerateAccuracyCircle(r, (x, y)) # Ajoute les points des cercles directement

        # On récupère toutes les ellipses de l'image svg
        elements = self.doc.getElementsByTagName("ellipse")
        for i in elements:
            x, y = float(i.getAttribute('cx')), float(i.getAttribute('cy'))
            rx, ry = float(i.getAttribute('rx')), float(i.getAttribute('ry'))
            self.points += self.GenerateAccuracyEllipse(rx, ry, (x, y)) # Ajoute les points des cercles directement

        # On récupère toutes les lignes de l'image svg
        elements = self.doc.getElementsByTagName("line")
        for i in elements:
            x1, y1 = float(i.getAttribute('x1')), float(i.getAttribute('y1'))
            x2, y2 = float(i.getAttribute('x2')), float(i.getAttribute('y2'))
            self.lines.append([[x1, y1], [x2, y2]]) # Enregistrement du segment

        # On récupère toutes les polyline, à savoir, un ensemble de ligne
        elements = self.doc.getElementsByTagName("polyline")
        for i in elements:
            pts = i.getAttribute('points').split(' ')
            for p in range(len(pts)):
                pts[p] = [float(pts[p].split(',')[0]),
                          float(pts[p].split(',')[1])] # On détermine mes coordonées des self.points

            for p in range(len(pts) - 1):
                self.lines.append([pts[p], pts[p+1]]) # Enregistrement du segment

        # On récupère les polygones
        elements = self.doc.getElementsByTagName("polygon")
        for i in elements:
            pts = i.getAttribute('points').split(' ')
            for p in range(len(pts)):
                pts[p] = [float(pts[p].split(',')[0]),
                          float(pts[p].split(',')[1])]

            for p in range(len(pts) - 1):
                self.lines.append([pts[p], pts[p+1]]) # Enregistrement des segments
            self.lines.append([pts[-1], pts[0]]) # Instruction pour la fermeture de la forme

        # On récupère tous les rectangles
        elements = self.doc.getElementsByTagName("rect")
        for i in elements:
            x = float(i.getAttribute('x'))
            y = float(i.getAttribute('y'))
            w = float(i.getAttribute('width'))
            h = float(i.getAttribute('height')) # On récupère les dimensions du rectangle et son point d'application
            ln = [[x, y], # Lignes ainsi crées
                  [x, y+h],
                  [x+w, y+h],
                  [x+w, y]]

            for p in range(len(ln) - 1): # Ajout à la liste
                self.lines.append([ln[p], ln[p+1]]) # Enregistrement des segments
            self.lines.append([ln[-1], ln[0]]) # Fermeture de la forme

        for line in self.lines: ## A la fin de la récupération des segments, on calcule l'ensemble des points
            self.points += self.GenerateAccuracyLine(line)

        self.PointsOptim() # On libère les points en dehors de la zone
        if self.trimode == 'nsoe':
            self.PointsSort() # On tri les points

    #####################################
    ## Décomposition en points         ##
    #####################################

    def GenerateAccuracyLine(self, line):
        points = []
        segw, segh = line[1][0] - line[0][0], line[1][1] - line[0][1] # Calcul la largeur projecté sur l'axe x et y du segment
        length = sqrt((segw**2) + (segh**2)) # Longueur du segment
        n = int(length/self.dt) # Détermine le nombre de points intermédiaires en fonction de la longueur du segment et de la précision voulu (delta T)
        for i in range(0, n+2): # Du premier au dernier élément (avec en plus le point final)
            n_dt = self.dt*i

            x = line[0][0] + ((segw*n_dt)/length) # calcule des coordonées du point suivant
            y = line[0][1] + ((segh*n_dt)/length)
            if self.coords == 'int':
                points.append([int(x), int(y)]) # Ajout du point (int)
            else:
                points.append([x, y]) # Ajout du point (float)

        return points # Renvoie une liste de tous les points du segment (pour une ligne uniquement)

    def GenerateAccuracyCircle(self, radius, O):
        Ox, Oy = O # Origine du cercke
        d = 2 * radius
        r = radius
        ox, oy = Ox-r, Oy # Premier point
        offsetx, offsety = Ox - r, Oy - r # Décalage de l'origine
        pts = []
        inter = (2*pi*self.dt) / (pi * d) # Angle d'intervalle entre deux points
        alpha = 0 # Angle
        for i in range(int((pi * d)/self.dt)):
            alpha += inter # On incrémente l'angle
            x = Ox - (r * cos(alpha)) # On calcule le point en question
            y = Oy - (r * sin(alpha))
            if self.coords == 'int':
                pts.append([int(x), int(y)]) # Ajout du point (int)
            else:
                pts.append([x, y]) # Ajout du point (float)
            ox, oy = x, y

        return pts.copy() # Renvoie la liste de points ainsi crée

    def GenerateAccuracyEllipse(self, rx, ry, O):
        if rx > ry:
            r = rx
        else:
            r = ry

        a, b = rx, ry
        d = 2 * r
        Ox, Oy = O # Origine de l'ellipse
        ox, oy = Ox-r, Oy # Premier point
        offsetx, offsety = Ox - r, Oy - r # Décalage de l'origine
        pts = []
        inter = (2*pi*self.dt) / (pi * d) # Angle d'intervalle entre deux points (pour un cercle de rayon le demi grand axe)
        alpha = 0 # Angle
        for i in range(int((pi * d)/self.dt)):
            alpha += inter # On incrémente l'angle
            x = Ox - ((a * b * cos(alpha))/sqrt((b**2 * cos(alpha) ** 2) + (a**2 * sin(alpha) ** 2))) # On calcule le point en question
            y = Oy - ((a * b * sin(alpha))/sqrt((b**2 * cos(alpha) ** 2) + (a**2 * sin(alpha) ** 2)))
            if self.coords == 'int':
                pts.append([int(x), int(y)]) # Ajout du point (int)
            else:
                pts.append([x, y]) # Ajout du point (float)
            ox, oy = x, y

        return pts.copy() # Renvoie la liste de points ainsi crée

    def PointsOptim(self):
        i = 0
        for pt in self.points:
            x, y = self.points[i]
            if x > self.width or y > self.height: # Regarde si on est en dehors de la zone de dessin
                self.points.pop(i)
                continue
            i += 1

    def PointsSort(self):
        self.points = sorted(self.points, key=lambda pt: pt[0]) # Tri d'abord la liste par abscisses
        self.points = sorted(self.points, key=lambda pt: pt[1]) # Puis tri par les ordonées

    #####################################
    ## Tracage du dessin avec points   ##
    #####################################

    def TraceShape(self, pause = 1, color = 'black'):
        tk = Tk() # Crée la fenêtre
        tk.title('Tracé des points')
        tk.resizable(False, False)
        c = Canvas(tk, width = 500, height = 500) # Zone de dessin
        c.pack()

        xmax, ymax = 0, 0 # On cherche la valeur x ou y la plus grande
        for i in self.points:
            x, y = i
            if x > xmax:
                xmax = x
            if y > ymax:
                ymax = y

        coefx = 500/xmax # Calcule du coeficient pour remplir la fenêtre en largeur
        coefy = 500/ymax #     "    "      "       "     "     "    "    "  hauteur
        if coefx < coefy: # Dans le cas ou c'est la largeur qui prime, on adapte la hauteur
            coefy = coefx
            c.config(height = ymax * coefy)
        else: # et vice versa
            coefx = coefy
            c.config(width = xmax * coefx)

        for p in self.points: # On trace les points
            x, y = p # Récupère les coordonées
            c.create_line(x*coefx, y*coefy, x*coefx+1, y*coefy+1, fill = color) # Dessine le point en noir
            if pause:
                tk.update() # Mise à jour
                sleep(pause * (10 ** -3)) # Attente de mise à jour (pour bien voir)

        tk.mainloop() # Démarrage de la fenêtre


#####################################
## Fonction de test                ##
#####################################

def htest(): # Fonction de test automatique
    print('Appel de la class')
    f = Figure(1, coords = 'float', tri = None)
    print('Partie n°1 : Depuis une image svg')
    f.open('img_01.svg')
    print(len(f), 'points calculés')
    f.saveas('export_points.pts')
    print('\nPartie n°2 : Depuis un fichier de points')
    f.open('export_points.pts')
    print(len(f), 'points lus')
    print('\nFin du test !')
    f.TraceShape(pause = 1, color = 'red')


if __name__ == '__main__':
    htest()
