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
    utilisateur = []
    animaux = []
    criteres = []
    images_folder = []
    objectif_criteres = []
    current_lvl = 0
    colored_links = True
    colored_criteres = True
    avancement_objectif = []

    def initialisation(self, size):
        configuration = Configuration("../cfg/ConfigSimple.json")
        self.size = size.size
        self.groupe = Groupe(1)
        configuration.config_table(self)
        self.add_widget(Links(self.colored_links))

    def add_critere(self, critere):
        self.add_widget(critere)
        self.criteres.append(critere)

    def nouvelles_images(self, niveau):
        self.add_animal_lvl(niveau)
        return self.objectif_criteres[self.current_lvl]

    def add_animal_lvl(self, lvl):
        r1 = self.get_root_window().width - 200
        r2 = self.get_root_window().height - 200
        Images = glob.glob(self.images_folder[lvl])
        for images in Images:
            self.add_animal(len(self.animaux) + 1, images, [r1, r2])

    def add_animal(self, id, image, pos):
        animal = Animal(id, image, pos)
        self.animaux.append(id)
        self.add_widget(animal)

    def add_indicateur(self, indicateur):
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

    def get_utilisateur(self, id):
        return self.groupe.get_utilisateur(id)


class TableApp(App):
    def build(self):
        self.table = Table()
        Clock.schedule_interval(self.table.update, 1.0 / 60.0)
        return self.table

    def on_start(self):
        self.table.initialisation(self.root_window)

    def on_stop(self):
        configuration = Configuration("../cfg/ConfigSimple.json")
        generateur = GenerateurRapport()
        configuration.config_generateur(generateur)
        generateur.generation(self.table)


if __name__ == '__main__':
    TableApp().run()
