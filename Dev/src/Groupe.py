class Groupe:
    def __init__(self, id):
        self.identifiant = id
        self.utilisateurs = []

    def add_utilisateur(self, utilisateur):
        self.utilisateurs.append(utilisateur)

    def get_utilisateur(self, id):
        for utilisateur in self.utilisateurs:
            if utilisateur.identifiant == id:
                return utilisateur
        return None

    def nb_utilisateurs(self):
        return len(self.utilisateurs)

    def nb_criteres(self):
        cpt = 0
        for utilisateur in self.utilisateurs:
            cpt += utilisateur.nb_criteres
        return cpt

    def nb_liens_persos(self):
        cpt = 0
        for utilisateur in self.utilisateurs:
            cpt += utilisateur.nb_liens_persos
        return cpt

    def nb_liens_autres(self):
        cpt = 0
        for utilisateur in self.utilisateurs:
            cpt += utilisateur.nb_liens_autres
        return cpt
