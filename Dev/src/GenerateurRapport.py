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
        self.ratio_links_perso_collabo = True
        self.ratio_criterions_groups = True

    def generation(self, table):
        """
        Generate a repport
        :param table: the table where to use informations
        """
        py.sign_in('lachand', 'sxtpaevi0x')

        if self.ratio_links_perso_collabo:
            id_user = []
            val_perso = []
            val_collabo = []
            for user in table.group.users:
                id_user.append(user.identifier)
                val_collabo.append(user.links_others)
                val_perso.append(user.links_persos)

            links_persos = go.Bar(
                x=id_user,
                y=val_perso,
                name='links personnels'
            )
            links_others = go.Bar(
                x=id_user,
                y=val_collabo,
                name='links collaboratifs'
            )
            data = [links_others, links_persos]
            layout = go.Layout(
                barmode='stack'
            )
            fig = go.Figure(data=data, layout=layout)
            print data
            py.image.save_as(fig, filename='ratio_links_persos_collabo.png')

        if self.ratio_criterions_groups:
            values = {}
            labels = []
            data = []
            colors = []

            for i in range(1, len(table.group.users) + 1):
                labels.append(str(i))

            for i in range(0, len(table.objective_criterions)):

                for user in table.group.users:
                    values[i, user.identifier] = user.nb_criterions[i]
                    colors.append('rgb(' + str(int(user.color[0] * 255)) + ',' + str(
                        int(user.color[1] * 255)) + ',' + str(int(user.color[2] * 255)) + ')')

                data.append({
                    "values": self.get_values(values, i),
                    "labels": labels,
                    'marker': {'colors': colors},
                    "domain": {"x": [0, 1]},
                    "name": "Nombre de criterions",
                    "hoverinfo": "label+percent+name",
                    "hole": .4,
                    "type": "pie"
                })

                fig = {
                    "data": [data[i]],
                    "layout": {
                        "title": "Nombre de criterions par joueurs en fonction du group : But " + str(i),
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

                py.image.save_as(fig, filename='ratio_criterion_group_but_' + str(i) + '.png')

    def get_values(self, values, i):
        """
        Get values with a part of a key in a dictionary
        :param values: the dictionary
        :param i: the part of the key
        :return a table with each values having i as a part of their key
        """
        answer = []
        for it in values.items():
            if it[0][0] == i:
                answer.insert(it[0][1] - 1, it[1])
        return answer
