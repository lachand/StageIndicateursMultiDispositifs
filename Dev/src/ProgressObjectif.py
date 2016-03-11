from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget


class ProgressObjectif(Widget):
    """
    A class to represent the indicator representing the progress comparing to objectives
    """
    def __init__(self, objectif, position, niveau_max):
        """
        Initialize the indicator
        :param objectif: a table of differents objectives
        :param position: the position of the indicator
        :param niveau_max: the max number of objectives
        """
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
        """
        Update the indicator when criterions are created
        """
        self.avancement = len(self.parent.criteres)
        self.pb.value = self.avancement

    def callback(instance, value):
        """
        Add new animals to the table if the current objective is done
        """
        if instance.avancement >= instance.objectif and instance.niveau < instance.niveau_max:
            table = instance.parent
            table.current_lvl += 1
            instance.niveau += 1
            instance.objectif = instance.parent.nouvelles_images(instance.niveau)
            instance.pb.max = instance.objectif
