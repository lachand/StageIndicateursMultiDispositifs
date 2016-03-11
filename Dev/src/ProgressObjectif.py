from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget


class ProgressObjectif(Widget):
    def __init__(self, objectif, position, niveau_max):
        Widget.__init__(self)
        self.objectif = objectif
        self.avancement = 0
        self.niveau = 0
        self.niveau_max = niveau_max

        btn_nouvelle_image = Button(text='Nouvelles images', size=[200, 50])
        btn_nouvelle_image.pos = (position[0] - btn_nouvelle_image.width / 2, position[1])
        btn_nouvelle_image.bind(on_press=self.callback)

        self.pb = ProgressBar(max=self.objectif, value=self.avancement, size=[200, 0])
        self.pb.pos = (position[0] - self.pb.width / 2, position[1] + btn_nouvelle_image.height)
        self.add_widget(btn_nouvelle_image)
        self.add_widget(self.pb)

    def update(self, dt):
        self.avancement = len(self.parent.criteres)
        self.pb.value = self.avancement

    def callback(instance, value):
        if instance.avancement >= instance.objectif and instance.niveau < instance.niveau_max:
            table = instance.parent
            table.current_lvl += 1
            instance.niveau += 1
            instance.objectif = instance.parent.nouvelles_images(instance.niveau)
            instance.pb.max = instance.objectif
