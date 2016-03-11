import plotly.graph_objs as go
import plotly.plotly as py
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot


class GenerateurRapport:
    """
    A class to represent the repport's generator
    """
    def __init__(self):
        """
        Initialize the generator
        """
        self.ratio_liens_perso_collabo = True
        self.ratio_criteres_groupes = True

    def generation(self, table):
        """
        Generate a repport
        :param table: the table where to use informations
        """
        py.sign_in('lachand', 'sxtpaevi0x')

        if self.ratio_liens_perso_collabo:
            id_utilisateur = []
            val_perso = []
            val_collabo = []
            for utilisateur in table.groupe.utilisateurs:
                id_utilisateur.append(utilisateur.identifiant)
                val_collabo.append(utilisateur.liens_autres)
                val_perso.append(utilisateur.liens_persos)

            liens_persos = go.Bar(
                x=id_utilisateur,
                y=val_perso,
                name='Liens personnels'
            )
            liens_autres = go.Bar(
                x=id_utilisateur,
                y=val_collabo,
                name='Liens collaboratifs'
            )
            data = [liens_autres, liens_persos]
            layout = go.Layout(
                barmode='stack'
            )
            fig = go.Figure(data=data, layout=layout)
            print data
            py.image.save_as(fig, filename='ratio_liens_persos_collabo.png')

        if self.ratio_criteres_groupes:
            values = {}
            labels = []
            data = []
            colors = []

            for i in range(1, len(table.groupe.utilisateurs) + 1):
                labels.append(str(i))

            for i in range(0, len(table.objectif_criteres)):

                for utilisateur in table.groupe.utilisateurs:
                    values[i, utilisateur.identifiant] = utilisateur.nb_criteres[i]
                    colors.append('rgb(' + str(int(utilisateur.couleur[0] * 255)) + ',' + str(
                        int(utilisateur.couleur[1] * 255)) + ',' + str(int(utilisateur.couleur[2] * 255)) + ')')

                data.append({
                    "values": self.get_values(values, i),
                    "labels": labels,
                    'marker': {'colors': colors},
                    "domain": {"x": [0, 1]},
                    "name": "Nombre de criteres",
                    "hoverinfo": "label+percent+name",
                    "hole": .4,
                    "type": "pie"
                })

                fig = {
                    "data": [data[i]],
                    "layout": {
                        "title": "Nombre de criteres par joueurs en fonction du groupe : But " + str(i),
                        "annotations":
                            {
                                "font": {
                                    "size": 20
                                },
                                "showarrow": False,
                                "text": "But 1 : ",
                                "x": 0.15,
                                "y": 0.5
                            }
                    }
                }

                py.image.save_as(fig, filename='ratio_critere_groupe_but_' + str(i) + '.png')

    def get_values(self, values, i):
        """
        Get values with a part of a key in a dictionnary
        :param values: the dictionnary
        :param i: the part of the key
        :return a table with eahc values having i as a part of their key
        """
        reponse = []
        for it in values.items():
            if it[0][0] == i:
                reponse.insert(it[0][1] - 1, it[1])
        return reponse
