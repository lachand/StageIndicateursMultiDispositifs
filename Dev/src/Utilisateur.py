class Utilisateur:
    def __init__(self, id, couleur, max_lvl):
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
        if self.critere.getitem(id_critere).size == 0:
            return False
        else:
            return True

    def add_link(self, id):
        if id != self.identifiant:
            self.liens_autres += 1
        else:
            self.liens_persos += 1

    def add_critere(self, id_critere):
        self.critere.append(id_critere)

    def add_critere_lvl(self, niveau):
        self.nb_criteres[niveau] += 1