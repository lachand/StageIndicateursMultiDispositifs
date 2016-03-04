from kivy.clock import Clock
from kivy.app import App
from kivy.uix.colorpicker import Color
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.graphics import Line, Ellipse
from kivy.properties import ListProperty
import random
from kivy.config import Config
Config.set('kivy', 'keyboard_mode','multi')
Config.set('kivy', 'keyboard_layout','keyboard.json')
Config.set('graphics','fullscreen','auto')
from kivy.gesture import Gesture, GestureDatabase
from gesture_circle import circle
from kivy.uix.textinput import TextInput

def simplegesture(name, point_list):
    g = Gesture()
    g.add_stroke(point_list)
    g.normalize()
    g.name = name
    return g

class Bouton(Widget):

    def __init__(self, id, couleur, position):
        self.ID = id
        self.Couleur = couleur
        self.Position = position
        Widget.__init__(self)

class Clavier(Scatter):

    def __init__(self, id, couleur, position, angle):
        Scatter.__init__(self)
        self.ID = id
        self.couleur = couleur
        self.pos = position
        self.rotation = angle
        ti = TextInput(size_hint=(None, None),backgroud_color=self.couleur,multiline=False)
        ti.bind(on_text_validate=self.validate)
        ti.bind(on_double_tap=self.delete)
        self.do_rotation = False
        self.do_scale = False
        self.do_translation = False
        self.add_widget(ti)

    def validate(self, value):
        if len(value.text)!=0:
            couleur = 0,0,0
            for fils in self.parent.children :
                if fils.__class__ == User and fils.ID == self.ID:
                    couleur = fils.Couleur
            concept = Concept(0,value.text, self.id, couleur, self.pos)
            self.parent.add_widget(concept)
        self.parent.remove_widget(self)

    def delete(self,value):
        self.parent.remove_widget(self)

class User(Widget):

    def __init__(self, id, pos):
        self.Nb_Idees = 0
        self.ID = id
        if self.ID == 1 :
            self.Couleur = [float(255/255.), float(189/255.), float(1/255.)]
        elif self.ID == 2 :
            self.Couleur = [float(0/255.), float(25/255.), float(255/255.)]
        elif self.ID == 3 :
            self.Couleur = [float(12/255.), float(127/255.), float(0/255.)]
        else:
            self.Couleur = [float(204/255.), float(8/255.), float(0/255.)]

        self.Taille = [500,500]
        self.Position = pos[0]-self.Taille[0]/2,pos[1]-self.Taille[1]/2
        self.validate=False
        Widget.__init__(self)

    def on_touch_down(self, touch):
        if touch.is_double_tap and self.collide_point(touch.x,touch.y):
            if self.ID == 1:
                position = self.get_root_window().width/2,200
                rotation = 0
            elif self.ID == 2:
                position = self.get_root_window().width-(300),self.get_root_window().height/2
                rotation = 90
            elif self.ID == 3:
                position = self.get_root_window().width/2,self.get_root_window().height-(300)
                rotation = 180
            elif self.ID == 4:
                position = 200,self.get_root_window().height/2
                rotation = -90
            print self.Couleur
            clav = Clavier(self.ID,self.Couleur,position,rotation)
            self.parent.add_widget(clav)
        elif self.collide_point(touch.x,touch.y):
            self.validate=True
            self.h = 0.5
            print self.validate

    def on_touch_up(self, touch):
        if self.collide_point(touch.x,touch.y):
            self.validate=False
            print self.validate

    def setPosition(self, pos):
        self.center = pos

    def getID(self):
        return self.ID

    def getCouleur(self):
        return self.col

    def setTaille(self, taille):
        self.size = taille

class Concept(Scatter):

    def __init__(self, id, texte, createur, couleur, position):
        print couleur
        Scatter.__init__(self)
        self.pos = position
        self.Nb_Liaisons = 0
        self.ID = id
        self.Texte = texte
        self.Createur = createur
        self.couleur = couleur
        self.Links = []
        self.size = len(texte)*10,50
        print self.pos
        print self.center
        with self.canvas:
            Color(self.couleur[0],self.couleur[1],self.couleur[2])
            Ellipse(size=(self.size))
            Label(text=self.Texte,halign='left',size=self.size)

    def addLink(self, id_img, id_usr):
        estDedans = False
        for lien in self.Links :
            if id_img == lien[0]:
                estDedans = True
                if id_usr == lien[1]:
                    self.Links.remove([id_img,id_usr])
        if estDedans == False :
            self.Links.append([id_img, id_usr])

    def fuseConcept(self,concept):
        for lien in concept.Links:
            self.addLink(lien[0],lien[1])
        for fils in self.parent.children:
            if fils.__class__ == Concept and fils.collide_widget(self) and fils != self:
                self.parent.remove_widget(fils)

    def update(self, dt):
        cpt = 0
        for child in self.parent.children :
            if child.__class__ == Animal and child.collide_point(self.center[0],self.center[1]) and child.current_user != 0:
                self.addLink(child.ID, child.current_user)
                child.current_user = 0
                child.remove_bouton_joueur()
            if child.__class__ == User and child.validate == True:
                cpt += 1
        if cpt == 4 :
            for child in self.parent.children :
                if child.__class__ == Concept and child.collide_point(self.center[0],self.center[1]) and child != self:
                    self.fuseConcept(child)

class Links(Widget):

    def update(self, dt):
        self.canvas.clear()
        for child in self.parent.children:
            if child.__class__ == Concept :
                for lien in child.Links:
                    for child2 in self.parent.children:
                        if child2.__class__ == Animal and lien[0] == child2.ID :
                            for user in self.parent.children:
                                if user.__class__ == User and user.ID == lien[1]:
                                    with self.canvas:
                                        Color(user.Couleur[0],user.Couleur[1],user.Couleur[2])
                                        Line(points=[child.center[0],child.center[1],child2.center[0],child2.center[1]],width=2)

class Animal(Scatter):

    def __init__(self, id, image, r1,r2):
        Scatter.__init__(self)
        self.size = [100,100]
        self.center = [random.randint(200,r1), random.randint(200,r2)]
        self.Image = image
        self.ID = id
        img = Image(source=self.Image)
        self.add_widget(img)
        self.nb_boutons = 0
        self.current_user = 0

    def add_bouton_joueur(self,id, Couleur):
        if id == 1 :
            bouton = Bouton(id,Couleur,[-10,-10])
        elif id == 2:
            bouton = Bouton(id,Couleur,[90,-10])
        elif id == 3 :
            bouton = Bouton(id,Couleur,[90,90])
        else :
            bouton = Bouton(id,Couleur,[-10,90])
        self.add_widget(bouton)
        self.nb_boutons += 1

    def remove_bouton_joueur(self):#,id):
        for element in self.children:
            if element.__class__ == Bouton :# and element.ID == id:
                self.nb_boutons -= 1
                self.remove_widget(element)

    def update(self, dt):
        for child in self.parent.children :
            if child.__class__ == User and child.collide_point(self.center[0],self.center[1]):
                if self.current_user == 0 :
                    self.current_user = child.ID
                    self.add_bouton_joueur(child.ID, child.Couleur)


class Demo(Widget):
    Users = ListProperty([])
    Images = ListProperty([])
    Concepts = ListProperty([])

    def initialisation(self, size):
        self.add_widget(Links())
        self.size = size.size
        self.addUser(1,[self.width,0])
        self.addUser(2,[self.width,self.height])
        self.addUser(3,[0,self.height])
        self.addUser(4,[0,0])
        r1 = self.get_root_window().width-200
        r2 = self.get_root_window().height-200
        self.addAnimal(1,"Images/2084.jpg",r1,r2)
        self.addAnimal(2,"Images/2085.jpg",r1,r2)
        self.addAnimal(3,"Images/2086.jpg",r1,r2)
        self.addAnimal(4,"Images/2087.jpg",r1,r2)
        self.addAnimal(5,"Images/2088.jpg",r1,r2)
        self.addAnimal(6,"Images/2089.jpg",r1,r2)
        self.addAnimal(7,"Images/2090.jpg",r1,r2)
        self.addAnimal(8,"Images/2091.jpg",r1,r2)
        self.addAnimal(9,"Images/2092.jpg",r1,r2)
        self.addAnimal(10,"Images/2094.jpg",r1,r2)
        #self.addConcept(1,"Poils",2)
        #self.addConcept(2,"Pattes",3)
        #self.addConcept(3,"Marin",1)
        self.gdb = GestureDatabase()
        self.gdb.add_gesture(circle)

    def update(self, dt):
        for child in self.children:
            if child.__class__ == Concept :
                child.update(dt)
            elif child.__class__ == Animal :
                child.update(dt)
            elif child.__class__ == Links :
                child.update(dt)



    def addUser(self, id, pos):
        user = User(id, pos)
        self.add_widget(user)
        #self.Users.add(id)

    def addConcept(self, id, texte, createur):
        concept = Concept(id, texte, createur)
        self.add_widget(concept)
        #self.Concepts.add(id)

    def addAnimal(self, id, image, r1, r2):
        animal = Animal(id, image, r1, r2)
        self.add_widget(animal)
        #self.Animals.add(id)

    # def on_touch_down(self, touch):
    #     touche = False
    #     for child in self.children :
    #         if child.collide_point(touch.x,touch.y) and child.__class__ == User and touche == False:
    #             child.on_touch_down(touch)
    #             touche = True
    #         if child.__class__ == Animal and touche == False:
    #             child.on_touch_down(touch)
    #             touche = True
    #         if child.__class__ == Concept and touche == False:
    #             touche = True
    #             child.on_touch_down(touch)
    #
    # def on_touch_up(self, touch):
    #     for child in self.children :
    #         if child.collide_point(touch.x,touch.y) and child.__class__ == User:
    #             child.on_touch_up(touch)
    #         if child.__class__ == Animal :
    #             child.on_touch_up(touch)
    #         if child.__class__ == Concept :
    #             child.on_touch_up(touch)
    # def on_touch_down(self, touch):
    #      for child in self.children :
    #          if child.collide_point(touch.x,touch.y) and child.__class__ == User:
    #              child.on_touch_down(touch)
    #          if child.__class__ == Animal and child.collide_point(touch.x,touch.y):
    #              child.on_touch_down(touch)
    #              break
    #          if child.__class__ == Concept and child.collide_point(touch.x,touch.y):
    #              child.on_touch_down(touch)
    #              break
             #if child.__class__ == TextInput and child.collide_point(touch.x,touch.y):
             #    child.on_touch_down(touch)
             #    break

class DemoApp(App):
    def build(self):
        self.demo = Demo()
        Clock.schedule_interval(self.demo.update, 1.0/60.0)
        return self.demo

    def on_start(self):
        self.demo.initialisation(self.root_window)

if __name__ == '__main__':
    DemoApp().run()