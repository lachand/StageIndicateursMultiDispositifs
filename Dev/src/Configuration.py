#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

import demjson as json

from ProgressObjectif import ProgressObjectif
from ZoneUtilisateur import ZoneUtilisateur
from ZoneVote import ZoneVote

class Configuration:
    """
    A class in order to dynamically configure the session
    """
    def __init__(self, config_file):
        """
        Initialize the configuration
        :param config_file: the configuration file
        """
        self.config_file = config_file

    def config_table(self, table):
        """
        Configure the table
        :param table: the table to configure
        """
        from Utilisateur import Utilisateur

        # Gestion des Images
        with open(self.config_file) as json_data:
            data = json.decode(json_data.read())

        max_lvl = int(data["Images"]["MaxLvl"])
        for lvl in data["Images"]["Src"]:
            table.images_folder.insert(int(lvl["Lvl"]), lvl["Src"])
            table.objective_criterions.insert(int(lvl["Lvl"]), int(lvl["Objectif"]))
        table.add_animal_lvl(0)

        # Gestion des users
        cpt_users = 1
        for user in data["Utilisateurs"]:
            r = float(user["Couleur"]["r"]) / 255.
            g = float(user["Couleur"]["g"]) / 255.
            b = float(user["Couleur"]["b"]) / 255.
            table.group.add_user(Utilisateur(cpt_users, [r, g, b], max_lvl))
            cpt_users += 1

        # Gestion des Indicateurs
        for indicateur in data["Indicateurs"]:
            # Indicateur : Zone personnelle
            if indicateur["Nom"] == "ZoneUtilisateur":
                table.add_indicateur(ZoneUtilisateur(table.get_user(int(indicateur["Source"])),
                                                     [int(indicateur["Position"]["x"]) * table.size[0] / 100,
                                                     int(indicateur["Position"]["y"]) * table.size[1] / 100]))
            # Indicateur : Zone de vote
            if indicateur["Nom"] == "ZoneVote":
                table.add_indicateur(ZoneVote(table.get_user(int(indicateur["Source"])),
                                                     [int(indicateur["Position"]["x"]) * table.size[0] / 100,
                                                     int(indicateur["Position"]["y"]) * table.size[1] / 100],
                                                     int(indicateur["Angle"])))
            # Indicateur : Progres de l'objective
            elif indicateur["Nom"] == "ProgressObjectif":
                table.add_indicateur(ProgressObjectif(table.objective_criterions[int(indicateur["Lvl"])],
                                                      [int(indicateur["Position"]["x"]) * table.size[0] / 100,
                                                      int(indicateur["Position"]["y"]) * table.size[1] / 100],
                                                      max_lvl))
            # Indicateurs : links colored
            elif indicateur["Nom"] == "Links":
                if indicateur["Colored"] == "True":
                    table.colored_links = True
                else:
                    table.colored_links = False

            # Indicateurs : criterions colored
            elif indicateur["Nom"] == "criterions":
                if indicateur["Colored"] == "True":
                    table.colored_criterions = True
                else:
                    table.colored_criterions = False

    def config_generateur(self, generateur):
        """
        Configure the indicator's generator
        :param generateur: the generator to configure
        """
        with open(self.config_file) as json_data:
            data = json.decode(json_data.read())
