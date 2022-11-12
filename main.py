#import des classes
#classes import
import screens, Tools_Android
import csv
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivymd.app import MDApp

#initialization of child classes
class Engine():

    def init(self, username=False, genre=False, weight=False, permis=False, database=False):
        if not database:
            self.loginUser = Tools_Android.NewUser(username, genre, weight, permis)
            self.loginConso = Tools_Android.Consommation()
            self.loginTaux = Tools_Android.TauxAlc(self.getUser().getElim(), self.getUser().getLimit())
        if database:
            self.database = Tools_Android.DataBase()

    def getUser(self):
        return self.loginUser

    def getDataBase(self):
        return self.database

    def getConso(self):
        return self.loginConso

    def getTaux(self):
        return self.loginTaux

#GUI Builder
class AlcoolTracker(MDApp, App, Widget):
    def build(self):
        self.theme_cls.theme_style= "Dark"
        self.theme_cls.primary_palette= "BlueGray"
        # Window.size=360, 780
        # Window.size= GetSystemMetrics(0),GetSystemMetrics(1)
        Window.fullscreen='auto'
        return Builder.load_file("AlcoolTracker.kv")

#Main Program
if __name__ == "__main__":
     #check that all users are offline
    records=[]
    with open('users.csv', 'r') as f:
        reader = csv.reader(f , delimiter=';')
        for row in reader:
            if not row==[]:
                if row[4]==True:
                    row[4]=False
                records.append(row)

    with open('users.csv','w',newline='', encoding='utf-8') as fichiercsv:
        writer=csv.writer(fichiercsv, delimiter=';')
        for k in records:
            writer.writerow(k)

    #App Launching
    screens.App()
    AlcoolTracker().run()



