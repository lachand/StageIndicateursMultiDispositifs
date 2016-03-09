from kivy.uix.widget import Widget

class Utilisateur():

    def __init__(self, id, couleur):
        self.ID = id
        self.Couleur = couleur
        self.validate=False
        self.Critere=[]
        self.CurrentImage=None

    def getID(self):
        return self.ID

    def getCouleur(self):
        return self.Couleur

    def hasCritere(self, idCritere):
        if self.Critere.getitem(idCritere).size == 0:
            return False
        else :
            return True

    def addCritere(self, idCritere):
        self.Critere.append(idCritere)

    def setCurrentImage(self,idImage):
        self.CurrentImage = idImage

    def Validate(self):
        self.validate = True

    def Unvalidate(self):
        self.validate = False

    def getValidate(self):
        return self.validate
