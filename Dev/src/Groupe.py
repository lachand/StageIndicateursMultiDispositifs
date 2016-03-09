class Groupe():

    def __init__(self,id):
        self.ID = id
        self.Utilisateurs=[]

    def getID(self):
        return self.ID

    def addUtilisateur(self,utilisateur):
        self.Utilisateurs.append(utilisateur)

    def getUtilisateur(self,id):
        for utilisateur in self.Utilisateurs :
            if utilisateur.getID() == id :
                return utilisateur
        return None

    def getUtilisateurs(self):
        return self.Utilisateurs

    def nbUtilisateurs(self):
        return len(self.Utilisateurs)

    def nbCriteres(self):
        cpt = 0
        for utilisateurs in self.Utilisateurs:
            cpt += utilisateurs.nbCriteres
        return cpt

    def nbLiensPersos(self):
        cpt = 0
        for utilisateurs in self.Utilisateurs:
            cpt += utilisateurs.nbLiensPersos
        return cpt

    def nbLiensAutres(self):
        cpt = 0
        for utilisateurs in self.Utilisateurs:
            cpt += utilisateurs.nbLiensAutres
        return cpt