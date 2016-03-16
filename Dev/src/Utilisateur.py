class Utilisateur:
    """
    A class representing a user of the application
    """
    def __init__(self, id, color, max_lvl):
        """
        Initialize an user
        :param id: the identifier of the user
        :param color: the color of the user
        :param max_lvl: the max_lvl for objectives
        """
        self.identifier = id
        self.color = color
        self.validate = False
        self.criterion = []
        self.nb_criterions = [0, 0, 0, 0]
        self.current_image = None
        self.links_persos = 0
        self.links_others = 0
        self.max_lvl = max_lvl

        for i in range(0, max_lvl):
            self.nb_criterions.append(0)

    def has_criterion(self, id_criterion):
        """
        Return if the user is the creator of a specified criterion
        :param id_criterion: the identifier of the criterion
        :return: true if hte user is the creator, else false
        """
        if self.criterion.getitem(id_criterion).size == 0:
            return False
        else:
            return True

    def add_link(self, id):
        """
        add a link to statistics
        :param id: the identifier of the link
        """
        if id != self.identifier:
            self.links_others += 1
        else:
            self.links_persos += 1

    def add_criterion(self, id_criterion):
        """
        add a criterion to statistics
        :param id: the identifier of the criterion
        """
        self.criterion.append(id_criterion)

    def add_criterion_lvl(self, level):
        """
        add a criterion to statistics
        :param level : the current level of the game
        """
        self.nb_criterions[level] += 1