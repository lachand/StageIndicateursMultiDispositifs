import demjson as json
from pprint import pprint

class Configuration():

    def setConfig(self,configFile,table):
        from Utilisateur import Utilisateur

        ## Gestion des Images
        with open("..\cfg\ConfigSimple.json") as json_data:
            data = json.decode(json_data.read())
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