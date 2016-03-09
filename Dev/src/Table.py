from Animal import Animal
from Utilisateur import Utilisateur
from Critere import Critere
from ZoneUtilisateur import ZoneUtilisateur
from Links import Links
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.lang import Builder
from Groupe import Groupe
from ProgressObjectif import ProgressObjectif
from Configuration import Configuration
import glob

Builder.load_file('template.kv')

Config.set('kivy', 'keyboard_mode', 'multi')
Config.set('kivy', 'keyboard_layout', 'keyboard.json')
Config.set('graphics', 'fullscreen', 'auto')

class Table(Widget):
    Utilisateur = []
    Animaux = []
    Criteres = []
    ImagesFolder = []
    ObjectifCriteres = []
    CurrentLvl = 0

    def initialisation(self, size):
        configuration = Configuration()
        self.size = size.size
        self.groupe = Groupe(1)
        self.groupe.addUtilisateur(Utilisateur(1, [float(255/255.), float(189/255.), float(1/255.)]))
        self.groupe.addUtilisateur(Utilisateur(2, [float(0/255.), float(25/255.), float(255/255.)]))
        self.groupe.addUtilisateur(Utilisateur(3, [float(12/255.), float(127/255.), float(0/255.)]))
        self.groupe.addUtilisateur(Utilisateur(4, [float(204/255.), float(8/255.), float(0/255.)]))
        ##
        r1 = self.get_root_window().width-200
        r2 = self.get_root_window().height-200
        ##
        #self.addAnimal(1, "Images/2084.jpg", [r1, r2])
        #self.addAnimal(2, "Images/2085.jpg", [r1, r2])
        #self.addAnimal(3, "Images/2086.jpg", [r1, r2])
        #self.addAnimal(4, "Images/2087.jpg", [r1, r2])
        #self.addAnimal(5, "Images/2088.jpg", [r1, r2])
        #self.addAnimal(6, "Images/2089.jpg", [r1, r2])
        ##
        self.addIndicateur(ZoneUtilisateur(self.getUtilisateur(1), [self.width ,0]))
        self.addIndicateur(ZoneUtilisateur(self.getUtilisateur(2), [self.width, self.height]))
        self.addIndicateur(ZoneUtilisateur(self.getUtilisateur(3), [0, self.height]))
        self.addIndicateur(ZoneUtilisateur(self.getUtilisateur(4), [0, 0]))
        self.add_widget(Links())

        configuration.setConfig("..\cfg\ConfigSimple.json",self)

        self.pb = ProgressObjectif(self.ObjectifCriteres[self.CurrentLvl],[self.width/2, 0])
        self.add_widget(self.pb)

    def addUser(self, id, couleur):
        self.Utilisateur.append(Utilisateur(id, couleur))

    def addCritere(self, critere):
        self.add_widget(critere)
        self.Criteres.append(critere)

    def nouvellesImages(self,niveau):
        self.addAnimalLvl(niveau)
        self.CurrentLvl += 1
        return self.ObjectifCriteres[self.CurrentLvl]

    def addAnimalLvl(self,lvl):
        r1 = self.get_root_window().width-200
        r2 = self.get_root_window().height-200
        Images = glob.glob(self.ImagesFolder[lvl])
        print self.ImagesFolder[lvl]
        for images in Images:
            self.addAnimal(len(self.Animaux)+1,images,[r1,r2])


    def addAnimal(self, id, image, pos):
        animal = Animal(id, image, pos)
        self.Animaux.append(id)
        self.add_widget(animal)

    def addIndicateur(self, indicateur):
        self.add_widget(indicateur)

    def update(self, dt):
        for child in self.children:
            if child.__class__ == Critere:
                child.update(dt)
            elif child.__class__ == Animal:
                child.update(dt)
            elif child.__class__ == Links:
                child.update(dt)
            elif child.__class__ == ProgressObjectif:
                child.update(dt)

    def getUtilisateur(self, id):
        return self.groupe.getUtilisateur(id)

    def getUtilisateurs(self):
        return self.groupe.getUtilisateurs()

    def getNbCriteres(self):
        return len(self.Criteres)

class TableApp(App):
    def build(self):
        self.table = Table()
        Clock.schedule_interval(self.table.update, 1.0/60.0)
        return self.table

    def on_start(self):
        self.table.initialisation(self.root_window)

if __name__ == '__main__':
    TableApp().run()