from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import tkinter as tk

class ToolTip(object):
    id = None
    tw = None

    def __init__(self, widget, text='', color = '#FFFFEA', waittime = 500, wraplength = 270, relief = 'solid', borderwidth = 1, justify = 'left'):
        self.relief = relief
        self.borderwidth = borderwidth
        self.justify = justify
        self.color = color
        self.widget = widget
        self.text = text
        self.waittime = waittime
        self.wraplength = wraplength
        self.ln = self.text.split('\n')
        self.mode_dbl = True if len(self.ln) >= 2 else False

        font = {'family': 'Segoe UI', 'size': 9}

        self.font_text = (font['family'], font['size'])

        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        f = tk.Frame(self.tw, relief = self.relief, background = self.color, borderwidth = self.borderwidth)
        f.pack(ipadx=1)

        label = tk.Label(f,
                         text = self.text,
                         justify = self.justify,
                         background = self.color,
                         relief = None,
                         font = self.font_text,
                         wraplength = self.wraplength)

        label.grid(padx = 1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()


class Settings:
    def __init__(self):
        self.data = True

        self.master = Tk()
        self.master.title('Configuration')
        self.master.resizable(False, False)
        self.master.protocol('WM_DELETE_WINDOW', self.Quitter)

        self.style = ttk.Style()
        self.style.configure("TLabel", foreground="black", font = ('Consolas', 11))
        self.style.configure("TButton", foreground = "black", font = ('Consolas', 11))

        self.step_down = [False, False]

        self.file = StringVar()
        self.coef = StringVar(value = '7/4')
        self.step0()

    def step0(self):
        if self.step_down[0]:
            return

        self.step_down[0] = True
        self.label_file = ttk.Label(self.master, text = 'Fichier à ouvrir :')
        self.label_file.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 10, sticky = 'w')

        self.entry_file = ttk.Entry(self.master, textvariable = self.file, font = ('Consolas', 11))
        self.entry_file.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'we')
        self.entry_file.bind('<KeyRelease>', self.Open)

        self.bt_file = ttk.Button(self.master, text = '...', command = self.Open, width = 3)
        self.bt_file.grid(row = 1, column = 1, padx = 10, pady = 5)

    def step1(self):
        if self.step_down[1]:
            return

        self.step_down[1] = True
        self.label_dp = ttk.Label(self.master, text = 'Intervalle entre les points :')
        self.label_dp.grid(row = 2, column = 0, columnspan = 2, padx = 10, pady = 10, sticky = 'w')

        self.dp = ttk.Spinbox(self.master, from_ = 1, to_ = 99999, font = ('Consolas', 11))
        self.dp.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = 'we')
        self.dp.set(1000)
        ToolTip(self.dp, """Choix du nombre de points pour la décomposition de la figure. Plus le nombre indiqué sera faible, plus il y aura de points générés.""")

        self.label_unit = ttk.Label(self.master, text = 'milli px')
        self.label_unit.grid(row = 3, column = 1, padx = 10, pady = 5)
        ToolTip(self.label_unit, """Entrez ici l'intervalle entre deux points. L'unité est le pixel. Pour plus de précision dans les calculs des cercles et des ellipses, vous pouvez changer au millième de picel près. Plus le nombre indiqué est petit, plus le nombre de points sera grand, et donc, plus la forme sera précise. (Des points trop près entraineront un temps de calcul bien supérieur. Nous recommandons de mettre 1000 comme valeur par défaut)""")

        self.label_qty = ttk.Label(self.master, text = 'Quantité de vecteurs :')
        self.label_qty.grid(row = 4, column = 0, columnspan = 2, padx = 10, pady = 10, sticky = 'w')

        self.scale = ttk.Scale(self.master, from_ = 0, to = 1)
        self.scale.grid(row = 5, column = 0, padx = 10, pady = 5, sticky = 'we')
        self.scale.set(1)
        ToolTip(self.scale, """Quantité de vecteur à utiliser pour reproduire la forme. Nombre appartenant à [0; 1]. A 0, un simple vecteur, immobile : aucune précision. A 1, la quantité de vecteurs est optimisée en fonction de la précision voulu dans le champ au dessus.""")

        self.entry_coef = ttk.Entry(self.master, textvariable = self.coef, width = 5, font = ('Consolas', 11))
        self.entry_coef.grid(row = 5, column = 1, padx = 10, pady = 5)
        ToolTip(self.entry_coef, """Le coeficient ici permet de calculer le nombre de vecteurs maximum calculable en fonction de la dimension des points. Il doit impérativement être exprimé sous forme de fraction !""")

        self.start = ttk.Button(self.master, text = 'LANCER LA SIMULATION', command = self.launch)
        self.start.grid(row = 6, column = 0, columnspan = 2, padx = 10, pady = 10, sticky = 'we')
        ToolTip(self.start, """Ferme cette fenêtre de paramétrage puis lance la procédure de calcul des points. Une fois les points calculés, une autre fenêtre s'ouvrira pour afficher la zone vectorielle.""")

    def hide1(self):
        try:
            self.step_down[1] = False
            self.label_dp.destroy()
            self.dp.destroy()
            self.label_unit.destroy()
            self.label_qty.destroy()
            self.scale.destroy()
            self.entry_coef.destroy()
            self.start.destroy()
        except AttributeError:
            pass

    def convertFraction(self, string):
        string = string.replace(' ', '')
        string = string.replace(':', '/')
        string = string.replace('\\', '/')
        div, did = string.split('/')
        div, did = int(div), int(did)
        return div / did

    def launch(self):
        self.data = {'path': self.file.get(),
                     'dp': int(self.dp.get()) / 1000,
                     'nbVect': self.scale.get(),
                     'coefVect': self.convertFraction(self.coef.get())}

        self.master.destroy()

    def Open(self, evt = None):
        if evt == None:
            file = askopenfilename(title = 'Ouvrir', initialdir = '.', filetypes = [('Images SVG', '*.svg'), ('Liste de points', '*.pts'), ('Tous les fichiers', '*.*')])
        else:
            file = self.file.get()

        if file:
            self.file.set(value = file)
            self.step1()
        else:
            self.hide1()
            self.hide2()

    def Quitter(self):
        self.data = None
        self.master.destroy()

    def wait(self):
        self.master.wait_window()
        return self.data

def htest():
    s = Settings()
    config = s.wait()
    ## Format de config :
    ## {'path': Chemin absolu vers le fichier à ouvrir, pret pour le programme d'import d'une image
    ##  'dp': Distance entre deux points (float) en pixel, pret pour le programme d'import d'une image
    ##  'nbVect': Quantité de vecteur, [0; 1],
    ##  'coefVect': Coeficient (par défaut 7/4=1.75) pour le nombre de vecteurs maximum selon le nombre de points}

if __name__ == '__main__':
    htest()
