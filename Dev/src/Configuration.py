#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

import json as json2
import os
import urllib

import demjson as json

from IndicateurCritere import IndicateurCritere
from IndicateurVote import IndicateurVote
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
        # """
        # self.backend = BackendWeb(
        #     url="http://www.museotouch.fr/api/interface_v2/",
        #     data_url="http://www.museotouch.fr/api/interface_v2/",
        #     decode=False)
        self.config_file = config_file

    def config_table(self, table, id):
        """
        Configure the table
        :param id:
        :param table: the table to configure
        """

        from Utilisateur import Utilisateur

        if not os.path.exists("../Activities/"+str(id)):
            os.makedirs("../Activities/"+str(id))

        if table.has_internet:
            from backend.backendweb import BackendWeb
            self.backend = BackendWeb(
             url="http://museotouch.fr/api/interface_v2/",
             data_url="http://museotouch.fr/api/interface_v2/",
             decode=False)

        table.remove_widget(table.layout)

        with open(self.config_file) as json_data:
            data = json.decode(json_data.read())
        # Creation of users
        cpt_users = 1
        for user in data["Utilisateurs"]:
            r = float(user["Couleur"]["r"]) / 255.
            g = float(user["Couleur"]["g"]) / 255.
            b = float(user["Couleur"]["b"]) / 255.
            table.group.add_user(Utilisateur(cpt_users, [r, g, b], 3,
                                             [int(user["Position"]["x"]) * table.size[0] / 100,
                                              int(user["Position"]["y"]) * table.size[1] / 100]))
            cpt_users += 1

        for indicateur in data["Indicateurs"]:
            # Indicator : personnal zone
            if indicateur["Nom"] == "ZoneUtilisateur":
                zone = ZoneUtilisateur(table.get_user(int(indicateur["Source"])),
                                       [int(indicateur["Position"]["x"]) * table.size[0] / 100,
                                        int(indicateur["Position"]["y"]) * table.size[1] / 100])
                table.add_indicateur(zone)
                table.user_zones.append(zone)
            # Indicator : vote zone
            if indicateur["Nom"] == "ZoneVote":
                print "ajout zone vote"
                table.add_indicateur(ZoneVote(table.get_user(int(indicateur["Source"])),
                                              [int(indicateur["Position"]["x"]) * table.size[0] / 100,
                                               int(indicateur["Position"]["y"]) * table.size[1] / 100],
                                              int(indicateur["Angle"])))

        # Download all informations about the activity
        if table.has_internet:
            # Download all informations about the activity
            self.backend.get_expos(uid=id)

            result = self.backend.req.result
            with open("../Activities/"+str(id)+"/config.json", 'w') as fd:
                from json import dump
                dump(result, fd)
                fd.close()


        ##### Load activity without internet
        with open("../Activities/"+str(id)+"/config.json", "r") as fd:
            json_data = fd.read()
            data = json2.loads(json_data)

        # Association between indicator's mode and id
        print data
        for elmt in data["keywords"]:
            if elmt["fieldId"] == "Indicateur-nombre-de-criteres":
                for choix in elmt["choices"]:
                    if choix["label"] == "Integre":
                        crit_integre = choix["choiceId"]
                    elif choix["label"] == "Ajoute":
                        crit_ajoute = choix["choiceId"]

            elif elmt["fieldId"] == "Indicateur-votes":
                for choix in elmt["choices"]:
                    if choix["label"] == "Integre":
                        vote_integre = choix["choiceId"]
                    elif choix["label"] == "Ajoute":
                        vote_ajoute = choix["choiceId"]

            elif elmt["fieldId"] == "Indicateur-nombre-de-liens":
                for choix in elmt["choices"]:
                    if choix["label"] == "Integre":
                        lien_integre = choix["choiceId"]
                    elif choix["label"] == "Ajoute":
                        lien_ajoute = choix["choiceId"]

            elif elmt["fieldId"] == "Indicateur-progres-objectifs":
                for choix in elmt["choices"]:
                    if choix["label"] == "Integre":
                        prog_integre = choix["choiceId"]
                    elif choix["label"] == "Ajoute":
                        prog_ajoute = choix["choiceId"]

        # Creation of objectives
        for elmt in data["items"]:
            for struct in data["structures"]:
                if struct["structureConstId"] == "Objectifs":
                    if elmt["structureId"] == struct["structureId"]:
                        lvl = int(elmt["fields"]["Niveau"])
                        objectif = int(elmt["fields"]["Objectif"])
                        table.objective_criterions.insert(lvl, objectif)

        # Configuration of indicators
        for elmt in data["items"]:

            for struct in data["structures"]:
                if struct["structureConstId"] == "Parametres-application-indicateurs":
                    print struct["structureId"], struct
                    if elmt["structureId"] == struct["structureId"]:

                        max_lvl = elmt["fields"]["Nombre-de-niveaux"]
                        url = "http://" + elmt["mainMedia"]["url"].replace("%2F", "/")

                        for i in range(0, int(max_lvl)):
                            table.images_folder.append([])

                        if elmt["fields"]["Indicateur-nombre-de-criteres"] == [crit_integre]:
                            table.integrated_criterions = True
                        elif elmt["fields"]["Indicateur-nombre-de-criteres"] == [crit_ajoute]:
                            table.integrated_criterions = False
                            print "ajout indicateur critere"
                            indicateur_critere = IndicateurCritere()
                            table.add_widget(indicateur_critere)
                            indicateur_critere.add_label()
                        else:
                            table.integrated_criterions = False

                        if elmt["fields"]["Indicateur-votes"] == [vote_integre]:
                            table.vote_integrated = True
                            vote = IndicateurVote(table.vote_integrated)
                            table.add_widget(vote, index=100000)
                            vote.initialisation()
                        elif elmt["fields"]["Indicateur-votes"] == [vote_ajoute]:
                            table.vote_integrated = False
                            vote = IndicateurVote(table.vote_integrated)
                            table.add_widget(vote)
                            vote.initialisation()
                        else:
                            table.vote_integrated = False

                        if elmt["fields"]["Indicateur-nombre-de-liens"] == [lien_integre]:
                            table.integrated_links = True

                        elif elmt["fields"]["Indicateur-nombre-de-liens"] == [lien_ajoute]:
                            table.integrated_links = False
                        else:
                            table.integrated_links = None

                        if elmt["fields"]["Indicateur-progres-objectifs"] == [prog_integre]:
                            table.add_indicateur(ProgressObjectif(table.objective_criterions[0],
                                                                  [50. * table.size[0] / 100.,
                                                                   0. * table.size[1] / 100.],
                                                                  int(max_lvl), True, url))
                        elif elmt["fields"]["Indicateur-progres-objectifs"] == [prog_ajoute]:
                            table.add_indicateur(ProgressObjectif(table.objective_criterions[0],
                                                                  [50. * table.size[0] / 100.,
                                                                   0. * table.size[1] / 100.],
                                                                  int(max_lvl), False))

            # Adding images to the activity
            for struct in data["structures"]:

                if struct["structureConstId"] == "Element":
                    if elmt["structureId"] == struct["structureId"]:
                        if not os.path.exists("../Activities/"+str(id)+"/lvl"+str(elmt["fields"]["Niveau"])):
                            os.makedirs("../Activities/"+str(id)+"/lvl"+str(elmt["fields"]["Niveau"]))
                        url = "http://" + elmt["mainMedia"]["url"].replace("%2F", "/")
                        image_str =url.rsplit('/', 1)
                        if not os.path.exists("../Activities/"+str(id)+"/lvl"+str(elmt["fields"]["Niveau"])+"/"+image_str[1]):
                            urllib.urlretrieve (url, "../Activities/"+str(id)+"/lvl"+str(elmt["fields"]["Niveau"])+"/"+image_str[1])
                        table.images_folder[int(elmt["fields"]["Niveau"]) - 1].append("../Activities/"+str(id)+"/lvl"+str(elmt["fields"]["Niveau"])+"/"+image_str[1])

        table.add_animal_lvl(0)
        table.add_animal_lvl(1)
