class Utilisateur:
    """
    A class representing a user of the application
    """
    def __init__(self, id, couleur, max_lvl):
        """
        Initialize an user
        :param id: the identifier of the user
        :param couleur: the color of the user
        :param max_lvl: the max_lvl for objectives
        """
        self.identifiant = id
        self.couleur = couleur
        self.validate = False
        self.critere = []
        self.nb_criteres = [0, 0, 0, 0]
        self.current_image = None
        self.liens_persos = 0
        self.liens_autres = 0
        self.max_lvl = max_lvl

        for i in range(0, max_lvl):
            self.nb_criteres.append(0)

    def has_critere(self, id_critere):
        """
        Return if the user is the creator of a specified criterion
        :param id_critere: the identifier of the criterion
        :return: true if hte user is the creator, else false
        """
        if self.critere.getitem(id_critere).size == 0:
            return False
        else:
            return True

    def add_link(self, id):
        """
        add a link to statistics
        :param id: the identifier of the link
        """
        if id != self.identifiant:
            self.liens_autres += 1
        else:
            self.liens_persos += 1

    def add_critere(self, id_critere):
        """
        add a criterion to statistics
        :param id: the identifier of the criterion
        """
        self.critere.append(id_critere)

    def add_critere_lvl(self, niveau):
        """
        add a criterion to statistics
        :param niveau : the current level of the game
        """
        self.nb_criteres[niveau] += 1