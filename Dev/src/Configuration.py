import demjson as json
from ZoneUtilisateur import ZoneUtilisateur
from ProgressObjectif import ProgressObjectif
from Links import Links

class Configuration():

    def setConfigTable(self,configFile,table):
        from Utilisateur import Utilisateur

        ## Gestion des Images
        with open(configFile) as json_data:
            data = json.decode(json_data.read())

        maxLvl = int(data["Images"]["MaxLvl"])
        for lvl in data["Images"]["Src"]:
            table.ImagesFolder.insert(int(lvl["Lvl"]),lvl["Src"])
            table.ObjectifCriteres.insert(int(lvl["Lvl"]),int(lvl["Objectif"]))
        table.addAnimalLvl(0)

        ## Gestion des Utilisateurs
        cptUtilisateurs = 1
        for utilisateur in data["Utilisateurs"]:
            r = float(utilisateur["Couleur"]["r"])
            g = float(utilisateur["Couleur"]["g"])
            b = float(utilisateur["Couleur"]["b"])
            table.groupe.addUtilisateur(Utilisateur(cptUtilisateurs,[r,g,b]))
            cptUtilisateurs += 1

        ## Gestion des Indicateurs
        for indicateur in data["Indicateurs"]:
            ## Indicateur : Zone personnelle
            if indicateur["Nom"] == "ZoneUtilisateur":
                table.addIndicateur(ZoneUtilisateur(table.getUtilisateur(int(indicateur["Source"])),
                                                    [int(indicateur["Position"]["x"])*table.size[0]/100,
                                                     int(indicateur["Position"]["y"])*table.size[1]/100]))
            ## Indicateur : Progres de l'objectif
            elif indicateur["Nom"] == "ProgressObjectif":
                table.addIndicateur(ProgressObjectif(table.getObjectifCriteres(int(indicateur["Lvl"])),
                                                     [int(indicateur["Position"]["x"])*table.size[0]/100,
                                                      int(indicateur["Position"]["y"])*table.size[1]/100],
                                                     maxLvl))
            ## Indicateurs : Liens colores
            elif indicateur["Nom"] == "Links":
                if indicateur["Colored"] == "True":
                    table.setColoredLinks(True)
                else:
                    table.setColoredLinks(False)

            ## Indicateurs : criteres colores
            elif indicateur["Nom"] == "Criteres":
                if indicateur["Colored"] == "True":
                    table.setColoredCriteres(True)
                else:
                    table.setColoredCriteres(False)

    def setConfigGenerateur(self,configFile,generateur):
        with open(configFile) as json_data:
            data = json.decode(json_data.read())