from Animal import Animal
from Utilisateur import Utilisateur
from Critere import Critere
from ZoneUtilisateur import ZoneUtilisateur
from Links import Links
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.colorpicker import Color
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.graphics import Line, Ellipse
from kivy.properties import ListProperty
from kivy.config import Config
from importlib import import_module
from kivy.lang import Builder

Builder.load_file('template.kv')

Config.set('kivy', 'keyboard_mode','multi')
Config.set('kivy', 'keyboard_layout','keyboard.json')
Config.set('graphics','fullscreen','auto')



class Table(Widget):

    Utilisateur = []
    Animaux = []
    Criteres = []

    def initialisation(self, size):
        self.size = size.size
        ##
        self.addUser(1,[float(255/255.), float(189/255.), float(1/255.)])
        self.addUser(2,[float(0/255.), float(25/255.), float(255/255.)])
        self.addUser(3,[float(12/255.), float(127/255.), float(0/255.)])
        self.addUser(4,[float(204/255.), float(8/255.), float(0/255.)])
        ##
        r1 = self.get_root_window().width-200
        r2 = self.get_root_window().height-200
        ##
        self.addAnimal(1,"Images/2084.jpg",[r1,r2])
        self.addAnimal(2,"Images/2085.jpg",[r1,r2])
        self.addAnimal(3,"Images/2086.jpg",[r1,r2])
        self.addAnimal(4,"Images/2087.jpg",[r1,r2])
        self.addAnimal(5,"Images/2088.jpg",[r1,r2])
        self.addAnimal(6,"Images/2089.jpg",[r1,r2])
        self.addAnimal(7,"Images/2090.jpg",[r1,r2])
        self.addAnimal(8,"Images/2091.jpg",[r1,r2])
        self.addAnimal(9,"Images/2092.jpg",[r1,r2])
        self.addAnimal(10,"Images/2094.jpg",[r1,r2])
        ##
        self.addIndicateur(ZoneUtilisateur(self.Utilisateur[0],[self.width,0]))
        self.addIndicateur(ZoneUtilisateur(self.Utilisateur[1],[self.width,self.height]))
        self.addIndicateur(ZoneUtilisateur(self.Utilisateur[2],[0,self.height]))
        self.addIndicateur(ZoneUtilisateur(self.Utilisateur[3],[0,0]))
        self.add_widget(Links())

    def addUser(self, id, couleur):
        self.Utilisateur.append(Utilisateur(id, couleur))

    def addCritere(self, id, texte, createur, position):
        critere = Critere(id, texte, createur, position)
        self.Criteres.append(id)
        self.add_widget(critere)

    def addAnimal(self, id, image, pos):
        animal = Animal(id, image, pos)
        self.Animaux.append(id)
        self.add_widget(animal)

    def addIndicateur(self, indicateur):
        self.add_widget(indicateur)

    def update(self, dt):
        for child in self.children:
            if child.__class__ == Critere :
                child.update(dt)
            elif child.__class__ == Animal :
                child.update(dt)
            elif child.__class__ == Links :
                child.update(dt)

    def getUtilisateur(self, id):
        for utilisateur in self.Utilisateur :
            if utilisateur.getID() == id :
                return utilisateur
        return None

class TableApp(App):
    def build(self):
        self.table = Table()
        Clock.schedule_interval(self.table.update, 1.0/60.0)
        return self.table

    def on_start(self):
        self.table.initialisation(self.root_window)

if __name__ == '__main__':
    TableApp().run()