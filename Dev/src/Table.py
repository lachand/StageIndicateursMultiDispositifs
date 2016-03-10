import glob

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.widget import Widget

from Animal import Animal
from Configuration import Configuration
from Critere import Critere
from GenerateurRapport import GenerateurRapport
from Groupe import Groupe
from Links import Links
from ProgressObjectif import ProgressObjectif

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
    ColoredLinks = True
    ColoredCriteres = True
    AvancementObjectif = []

    def initialisation(self, size):
        configuration = Configuration()
        self.size = size.size
        self.groupe = Groupe(1)
        configuration.setConfigTable("..\cfg\ConfigSimple.json", self)
        self.add_widget(Links(self.ColoredLinks))

    def addCritere(self, critere):
        self.add_widget(critere)
        self.Criteres.append(critere)

    def nouvellesImages(self, niveau):
        self.addAnimalLvl(niveau)
        return self.ObjectifCriteres[self.CurrentLvl]

    def addAnimalLvl(self, lvl):
        r1 = self.get_root_window().width - 200
        r2 = self.get_root_window().height - 200
        Images = glob.glob(self.ImagesFolder[lvl])
        print self.ImagesFolder[lvl]
        for images in Images:
            self.addAnimal(len(self.Animaux) + 1, images, [r1, r2])

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

    def getCriteres(self):
        return self.Criteres

    def getColoredCriteres(self):
        return self.ColoredCriteres

    def setColoredLinks(self, colored):
        self.ColoredLinks = colored

    def setColoredCriteres(self, colored):
        self.ColoredCriteres = colored

    def getUtilisateur(self, id):
        return self.groupe.getUtilisateur(id)

    def getUtilisateurs(self):
        return self.groupe.getUtilisateurs()

    def getNbCriteres(self):
        return len(self.Criteres)

    def getObjectifCriteres(self, lvl):
        return self.ObjectifCriteres[lvl]


class TableApp(App):
    def build(self):
        self.table = Table()
        Clock.schedule_interval(self.table.update, 1.0 / 60.0)
        return self.table

    def on_start(self):
        self.table.initialisation(self.root_window)

    def on_stop(self):
        configuration = Configuration()
        generateur = GenerateurRapport()
        configuration.setConfigGenerateur("..\cfg\ConfigSimple.json", generateur)
        generateur.generation(self.table)


if __name__ == '__main__':
    TableApp().run()
