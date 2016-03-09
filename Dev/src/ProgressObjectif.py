from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.uix.button import Button

class ProgressObjectif(Widget):

    def __init__(self, objectif, position):
        Widget.__init__(self)
        self.Objectif = objectif
        self.Avancement = 0
        self.Niveau = 0
        btnNouvelleImage = Button(text='Nouvelles images',size=[200,50])
        btnNouvelleImage.pos=(position[0]- btnNouvelleImage.width / 2,position[1])
        btnNouvelleImage.bind(on_press=self.callback)
        self.pb = ProgressBar(max=self.Objectif, value=self.Avancement,size=[200,0])
        self.pb.pos=(position[0]-self.pb.width/2,position[1]+btnNouvelleImage.height)
        self.add_widget(btnNouvelleImage)
        self.add_widget(self.pb)

    def update(self,dt):
        self.Avancement = self.parent.getNbCriteres()
        self.pb.value = self.Avancement

    def callback(instance,niveau):
        if instance.Avancement == instance.Objectif :
            instance.Objectif = instance.parent.nouvellesImages(instance.Niveau)
            instance.pb.max = instance.Objectif
            instance.Niveau += 1