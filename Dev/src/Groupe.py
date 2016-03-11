class Groupe:
    """
    A class to represent a group
    """
    def __init__(self, id):
        """
        Initialize the groupe
        :param id: the identifiant of the group
        """
        self.identifiant = id
        self.utilisateurs = []

    def add_utilisateur(self, utilisateur):
        """
        Add an user to the groupe
        :param utilisateur: the user to add
        """
        self.utilisateurs.append(utilisateur)

    def get_utilisateur(self, id):
        """
        Get a specific user of the group
        :param id: the identifiant of the user
        """
        for utilisateur in self.utilisateurs:
            if utilisateur.identifiant == id:
                return utilisateur
        return None

    def nb_utilisateurs(self):
        """
        Get the number of users in the group
        :return: the number of users in the group
        """
        return len(self.utilisateurs)

    def nb_criteres(self):
        """
        Get the number of criterions in the group
        :return: the number of criterions in the group
        """
        cpt = 0
        for utilisateur in self.utilisateurs:
            cpt += utilisateur.nb_criteres
        return cpt

    def nb_liens_persos(self):
        """
        Get the number of personal links in the group
        :return: the number of personal links in the group
        """
        cpt = 0
        for utilisateur in self.utilisateurs:
            cpt += utilisateur.nb_liens_persos
        return cpt

    def nb_liens_autres(self):
        """
        Get the number of collaborative links in the group
        :return: the number of collaborative links in the group
        """
        cpt = 0
        for utilisateur in self.utilisateurs:
            cpt += utilisateur.nb_liens_autres
        return cpt
