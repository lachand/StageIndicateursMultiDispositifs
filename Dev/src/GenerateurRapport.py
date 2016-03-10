import plotly.plotly as py
import plotly.graph_objs as go

class GenerateurRapport():

    def __init__(self):
        self.ratio_liens_perso_collabo = False
        self.ratio_criteres_groupes = False

    def generation(self, table):

        py.sign_in('lachand', 'sxtpaevi0x')

        id_utilisateur = []
        val_perso = []
        val_collabo=[]
        for utilisateur in table.getUtilisateurs():
            id_utilisateur.append(utilisateur.getID())
            val_collabo.append(utilisateur.nbLiensAutres())
            val_perso.append(utilisateur.nbLiensPersos())

        liensPersos = go.Bar(
            x=id_utilisateur,
            y=val_perso,
            name='Liens personnels'
        )
        liensAutres = go.Bar(
            x=id_utilisateur,
            y=val_collabo,
            name='Liens collaboratifs'
        )
        data = [liensAutres,liensPersos]
        layout = go.Layout(
            barmode='stack'
        )
        fig = go.Figure(data=data, layout=layout)
        py.image.save_as(fig, filename='ratio_liens_persos_collabo.png')