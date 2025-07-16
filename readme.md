Utilisation du module de configuration tkinter :
```py
from settings import Settings

s = Settings()
config = s.wait()
## Format de config :
## {'path': Chemin absolu vers le fichier à ouvrir, pret pour le programme d'import d'une image
##  'dp': Distance entre deux points (float) en pixel, pret pour le programme d'import d'une image
##  'nbVect': Quantité de vecteur, [0; 1],
##  'coefVect': Coeficient (par défaut 7/4=1.75) pour le nombre de vecteurs maximum selon le nombre de points}
```
Utilisation du générateur de points :
```py
from generator import Figure

f = Figure(dt, coords = 'int', tri = None) # coords : ('int', 'float') et tri : (None-> ordre des traits, 'nsoe'-> ordre haut en bas)
f.open('image.svg') # Ouvre l'image en svg, calcule les points et les met en accès par la méthode suivante :
l = len(f) # Longueur de la liste de points
first = f[0] # Premier point ou f[n], n < len(f)
f.saveas('file.pts') # Enregistre la liste des points sous le fichier indiqué (enregistre aussi si mode float ou int)
f.open('file.pts') # même ligne que pour ouvrir une image, mais sans calcules, récupère la liste de points, écrase les précédents et les mets en accès libre
f.TraceShape(pause = 1.0(ms), color = 'white') # Affiche sur une fenêtre tkinter les points, dans l'ordre généré. Couleur et intervalle de rafraichissement configurables
```
Exemple d'utilisation mixée des deux programmes (sans description du contenu des variables) :
```py
form settings import Settings
from generator import Figure

s = Settings()
config = s.wait()

f = Figure(config['dp'], coords = 'float', tri = None) # On ne met pas de tri, et les coordonées en flotant pour plus de précision
f.open(config['path']) # On ouvre le fichier, peu importe si c'est une liste de points ou une images svg
print('Il y a', len(f), 'points') # Affichage du nombre de points
print("Premiers points :")
for i in range(5):
    print("Point", i+1, ': ', f[i])

f.TraceShape(pause = 0.1, color = 'orange') # Ouvre une petite fenêtre tkinter pour voir l'ordre de tracé !
```
