import math


class Link:
    """
    A class representing a link between an animal and a criterion
    """
    def __init__(self, id_img, id_usr):
        """

        :param id_img:
        :param id_usr:
        :return:
        """
        self.id_img = id_img
        self.id_usr = id_usr
        self.distance = 0
        self.angle = 0

    def linked_to(self, id_img, id_usr):
        """

        :param id_img:
        :return:
        """
        return self.id_img == id_img and self.id_usr == id_usr

    def linked_to_animal(self, id_img):
        """

        :param id_img:
        :return:
        """
        return self.id_img == id_img

    def linked_to_user(self, id_usr):
        """

        :param id_img:
        :return:
        """
        return self.id_usr == id_usr

    def update(self, center_animal, center_critere):
        dx = center_critere[0] - center_animal[0]
        dy = center_critere[1] - center_animal[1]

        self.distance = math.hypot(dx, dy)
        self.angle = math.atan2(-dy, dx)