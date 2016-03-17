#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

import datetime

#locale.setlocale(locale.LC_TIME, "fr_FR.utf8")

import plotly.graph_objs as go


class GenerateurRapport:
    """
    A class to represent the report's generator
    """
    def __init__(self):
        """
        Initialize the generator
        """
        self.ratio_links_perso_collabo = True
        self.ratio_criterions_groups = True

    def generation(self, table):
        """
        Generate a report
        :param table: the table where to use informations
        """
        import plotly

        html_string = '''<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0 100; background:whitesmoke; }</style>
    </head>
    <body>
        <h1>Rapport d'activité du '''+datetime.datetime.now().strftime('%A %d %b')+'''</h1>'''

        if self.ratio_links_perso_collabo:
            id_user = []
            val_perso = []
            val_collabo = []
            colors = []
            colors2 = []
            for user in table.group.users:
                    colors.append('rgb(' + str(int(user.color[0] * 255)) + ',' + str(
                        int(user.color[1] * 255)) + ',' + str(int(user.color[2] * 255)) + ')')
                    colors2.append('rgb(' + str(int(user.color[0] * 125)) + ',' + str(
                        int(user.color[1] * 125)) + ',' + str(int(user.color[2] * 125)) + ')')


            for user in table.group.users:
                id_user.append(user.identifier)
                val_collabo.append(user.links_others)
                val_perso.append(user.links_persos)

            links_persos = go.Bar(
                x=id_user,
                y=val_perso,
                name='liens personnels',
                marker=dict(color=colors)
            )
            links_others = go.Bar(
                x=id_user,
                y=val_collabo,
                name='liens collaboratifs',
                marker=dict(color=colors2)
            )
            data = [links_others, links_persos]
            layout = go.Layout(
                barmode='stack'
            )
            fig = go.Figure(data=data, layout=layout)
            rapport = plotly.offline.plot(fig, filename="ratio_liens_collabo_persos.html",auto_open=False)
            html_string = html_string + '''<h2>Liens collaboratifs et personnels par utilisateur</h2>
            <iframe width="1000" height="550" frameborder="0" seamless="seamless" scrolling="no" src="''' + rapport + '''"></iframe>'''

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
                    "name": "Nombre de critères",
                    "hoverinfo": "label+percent+name",
                    "hole": .4,
                    "type": "pie"
                })

                fig = {
                    "data": [data[i]],
                    "layout": {
                        "title": "Nombre de critères par joueur en fonction du groupe : But " + str(i),

                    }
                }
                rapport = plotly.offline.plot(fig, filename='ratio_criterion_group_but_' + str(i) + ".html", auto_open=False)
                html_string = html_string + '''<h2>'''+fig["layout"]["title"]+'''</h2>
                <iframe width="1000" height="550" frameborder="0" seamless="seamless" scrolling="no" src="''' + rapport + '''"></iframe>'''

        html_string = html_string+'''</body></html>'''
        file_ = open('Rapport_'+datetime.datetime.now().strftime('%A_%d_%b')+'.html', 'w')
        file_.write(html_string)
        file_.close()

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
