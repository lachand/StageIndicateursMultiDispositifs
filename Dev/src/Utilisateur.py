class Utilisateur():

    def __init__(self, id, couleur,maxLvl):
        self.ID = id
        self.Couleur = couleur
        self.validate=False
        self.Critere=[]
        self.NbCriteres=[0,0,0,0]
        self.CurrentImage=None
        self.LiensPersos=0
        self.LiensAutres=0
        self.MaxLvl = maxLvl

        for i in range(0,maxLvl):
            self.NbCriteres.append(0)

    def getID(self):
        return self.ID

    def getCouleur(self):
        return self.Couleur

    def hasCritere(self, idCritere):
        if self.Critere.getitem(idCritere).size == 0:
            return False
        else :
            return True

    def addLink(self, id):
        if id != self.ID:
            self.LiensAutres += 1
        else:
            self.LiensPersos += 1

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

    def nbCriteres(self):
        return len(self.Critere)

    def nbLiensPersos(self):
        return self.LiensPersos

    def addCritereLvl(self,niveau):
        self.NbCriteres[niveau] += 1

    def nbLiensAutres(self):
        return self.LiensAutres