from kivy.uix.scatter import Scatter
from kivy.uix.textinput import TextInput
from Utilisateur import Utilisateur
from Critere import Critere


class Clavier(Scatter):
    def __init__(self, utilisateur, couleur, position, angle):
        Scatter.__init__(self)
        self.Utilisateur = utilisateur
        self.ID = self.Utilisateur.getid()
        self.couleur = couleur
        self.pos = position
        self.rotation = angle
        ti = TextInput(size_hint=(None, None), backgroud_color=self.couleur, multiline=False, size=(100, 30))
        ti.bind(on_text_validate=self.validate)
        self.do_rotation = False
        self.do_scale = False
        self.do_translation = False
        self.add_widget(ti)

    def validate(self, value):
        if len(value.text) != 0:
            critere = Critere(0, value.text, self.Utilisateur, self.pos, self.parent.getColoredCriteres())
            self.Utilisateur.addCritereLvl(self.parent.CurrentLvl)
            self.parent.addCritere(critere)
        self.parent.remove_widget(self)
