from kivy.app import App
from kivy.clock import Clock
import threading

class TableApp(App):
    def __init__(self, **kwargs):
        from Table import Table
        super(TableApp, self).__init__(**kwargs)
        self.table = Table()

    def build(self):
        Clock.schedule_interval(self.table.update, 1.0 / 60.0)
        return self.table

    def on_start(self):
        self.table.initialisation(self.root_window)
        t1 = threading.Thread(target=self.table.server.run_server)
        t1.daemon = True
        t1.start()

    def on_quit(self):
        if self.table.menu_mode :
            exit()
        else:
            self.table.menu()

    def on_stop(self):
        # from GenerateurRapport import GenerateurRapport
        # configuration = Configuration(PATH)
        # generateur = GenerateurRapport()
        # configuration.config_generateur(generateur)
        # generateur.generation(self.table)
        self.table.logger.close()