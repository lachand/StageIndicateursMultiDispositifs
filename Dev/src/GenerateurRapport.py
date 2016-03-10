import plotly.plotly as py
import plotly.graph_objs as go
from IPython.display import HTML, display

class GenerateurRapport():

    def __init__(self):
        self.ratio_liens_perso_collabo = True
        self.ratio_criteres_groupes = True

    def generation(self, table):

        py.sign_in('lachand', 'sxtpaevi0x')

        if self.ratio_liens_perso_collabo == True :
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

        if self.ratio_criteres_groupes == True :
            values = {}
            labels = []
            data = []
            colors = []

            for i in range(1,len(table.getUtilisateurs())+1):
                labels.append(str(i))

            for i in range(0,len(table.ObjectifCriteres)):

                for utilisateur in table.getUtilisateurs():
                    values[i,utilisateur.getID()] = utilisateur.NbCriteres[i]
                    colors.append('rgb('+str(int(utilisateur.Couleur[0]*255))+','+str(int(utilisateur.Couleur[1]*255))+','+str(int(utilisateur.Couleur[2]*255))+')')

                data.append({
                    "values": self.getValues(values,i),
                    "labels": labels,
                    'marker': {'colors': colors},
                    "domain": {"x": [0,1]},
                    "name": "Nombre de criteres",
                    "hoverinfo":"label+percent+name",
                    "hole": .4,
                    "type": "pie"
                    })

                fig = {
                    "data": [data[i]],
                    "layout": {
                            "title":"Nombre de criteres par joueurs en fonction du groupe : But "+str(i),
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

                py.image.save_as(fig, filename='ratio_critere_groupe_but_'+str(i)+'.png')

    def getValues(self,values,i):
        reponse = []
        for it in values.items():
            if it[0][0] == i :
                reponse.insert(it[0][1]-1,it[1])
        return reponse