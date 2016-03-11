import demjson as json

from ProgressObjectif import ProgressObjectif
from ZoneUtilisateur import ZoneUtilisateur


class Configuration:
    def __init__(self, config_file):
        self.config_file = config_file

    def config_table(self, table):
        from Utilisateur import Utilisateur

        # Gestion des Images
        with open(self.config_file) as json_data:
            data = json.decode(json_data.read())

        max_lvl = int(data["Images"]["MaxLvl"])
        for lvl in data["Images"]["Src"]:
            table.images_folder.insert(int(lvl["Lvl"]), lvl["Src"])
            table.objectif_criteres.insert(int(lvl["Lvl"]), int(lvl["Objectif"]))
        table.add_animal_lvl(0)

        # Gestion des Utilisateurs
        cpt_utilisateurs = 1
        for utilisateur in data["Utilisateurs"]:
            r = float(utilisateur["Couleur"]["r"]) / 255.
            g = float(utilisateur["Couleur"]["g"]) / 255.
            b = float(utilisateur["Couleur"]["b"]) / 255.
            table.groupe.add_utilisateur(Utilisateur(cpt_utilisateurs, [r, g, b], max_lvl))
            cpt_utilisateurs += 1

        # Gestion des Indicateurs
        for indicateur in data["Indicateurs"]:
            # Indicateur : Zone personnelle
            if indicateur["Nom"] == "ZoneUtilisateur":
                table.add_indicateur(ZoneUtilisateur(table.get_utilisateur(int(indicateur["Source"])),
                                                    [int(indicateur["Position"]["x"]) * table.size[0] / 100,
                                                     int(indicateur["Position"]["y"]) * table.size[1] / 100]))
            # Indicateur : Progres de l'objectif
            elif indicateur["Nom"] == "ProgressObjectif":
                table.add_indicateur(ProgressObjectif(table.objectif_criteres[int(indicateur["Lvl"])],
                                                     [int(indicateur["Position"]["x"]) * table.size[0] / 100,
                                                      int(indicateur["Position"]["y"]) * table.size[1] / 100],
                                                     max_lvl))
            # Indicateurs : Liens colores
            elif indicateur["Nom"] == "Links":
                if indicateur["Colored"] == "True":
                    table.colored_links = True
                else:
                    table.colored_links = False

            # Indicateurs : criteres colores
            elif indicateur["Nom"] == "Criteres":
                if indicateur["Colored"] == "True":
                    table.colored_criteres = True
                else:
                    table.colored_criteres = False

    def config_generateur(self, generateur):
        with open(self.config_file) as json_data:
            data = json.decode(json_data.read())
