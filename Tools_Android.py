# AlcooTest

import time, csv
from datetime import datetime
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

class TauxAlc():
    
    def __init__(self, coeff, limit):
        self.taux= 0.0
        self.coeff = coeff
        self.limit = limit

    #Alcohol Level getter
    def getTaux(self, username, hor=False):
        if not hor:
            hor=time.mktime(time.strptime(str(time.strftime("%b %d %H:%M %Y", time.localtime())),"%b %d %H:%M %Y"))

        records=[]
        with open('drink.csv', 'r') as f:
            reader = csv.reader(f , delimiter=';')
            for row in reader:
                if not row ==[]:
                    if row[6]==username:
                        records.append(row)
        records.sort()
        if records==[]:
            self.taux=0.0

        else:
            date=int(records[-1][0])
            horMaximum=int(records[-1][4])
            tauxMaximum=float(records[-1][5])

            if hor>horMaximum:
                self.taux=tauxMaximum - self.coeff *(hor-horMaximum)/60
                if self.taux<0:
                    self.taux=0.0

            elif hor<horMaximum:
                self.taux = tauxMaximum-((horMaximum-hor)*tauxMaximum/(horMaximum-date))
                if self.taux<0:
                    self.taux=0.0

            elif hor==horMaximum:
                self.taux = tauxMaximum
        return round(self.taux, 2)

    
    def getSymptomes(self, username):
        sympt = ""
        symptomes = {(0.0, 0.09): "Aucun effet",
                     (0.1, 0.3): "Décontracté",
                     (0.3, 0.5): "Réactivité altérée",
                     (0.3, 0.6): "Légère Euphorie",
                     (0.3, 0.8): "Baisse de l'Attention, Vision affaiblie",
                     (0.6, 1.0): "Extraversion",
                     (0.6, 2.5): "Sensation de chaleur",
                     (0.6, 3.0): "Reduction de la douleur",
                     (0.8, 3.0): "Vision Etroite, Manque de Concentration",
                     (1.0, 2.0): "Vomissement probable",
                     (1.0, 2.5): "Variations d'humeurs",
                     (1.5, 3.0): "Difficultés Prononcées à Parler, Titubations",
                     (1.8, float("inf")): "Pertes de Mémoire",
                     (2.0, float("inf")): "Vomissements",
                     (3.0, float("inf")): "Respiration Difficile et Faible, Perte de Conscience",
                     (3.5, float("inf")): "Danger de Mort, Intoxication élevée, Coma Ethylique"}
        taux = self.getTaux(username)
        for k in symptomes:
            if k[0] <= taux <= k[1]:
                for n in symptomes[k]:
                    sympt += n
                sympt += ", "
        return sympt[:-2]

    #Get sobriety date
    def taux0(self, username, aff=True):

        records=[]
        with open('drink.csv', 'r') as f:
            reader = csv.reader(f , delimiter=';')
            for row in reader:
                if not row==[]:
                    if row[6]==username:
                        records.append(row)
        records.sort()
        if records == []:
            return "Sobre"
        else:
            horMaximum = int(records[-1][4])
            tauxMaximum = float(records[-1][5])
            tps=int(tauxMaximum/(self.coeff/60))
            horZero = horMaximum + tps
        if aff:
            if horZero > time.mktime(time.strptime(str(time.strftime("%b %d %H:%M %Y", time.localtime())),"%b %d %H:%M %Y")):
                phr= "Sobre à la date: "+ str(datetime.fromtimestamp(horZero))[:-3]
            else:
                phr= "Sobre"
            return phr
        else:
            return horZero

    #Legal Driving date
    def tauxcond(self, username):
        records=[]
        with open('drink.csv', 'r') as f:
            reader = csv.reader(f , delimiter=';')
            for row in reader:
                if not row==[]:
                    if row[6]==username:
                        records.append(row)
        records.sort()
        horMaximum = int(records[-1][4])
        tauxMaximum =float(records[-1][5])
        tps=int((tauxMaximum-self.limit)/(self.coeff/60))
        horCond=str(datetime.fromtimestamp(horMaximum+tps))[:-3]
        phr= "Vous pourrez conduire à la date: "+horCond
        return phr

    #Check if Legal Driving date
    def conduiteaut(self, username):
        records=[]
        with open('drink.csv', 'r') as f:
            reader = csv.reader(f , delimiter=';')
            for row in reader:
                if not row==[]:
                    if row[6]==username:
                        records.append(row)
        records.sort()
        if records==[]:
            phr= "Vous pouvez conduire"
            return phr
        else:
            horaire=time.mktime(time.strptime(str(time.strftime("%b %d %H:%M %Y", time.localtime())),"%b %d %H:%M %Y"))
            horMaxi=int(records[-1][4])
            taux = self.getTaux(username, horaire)
            if horaire<horMaxi and taux <= self.limit:
                phr = "Vous pouvez conduire mais vous n'avez PAS ENCORE atteint votre pic d'alcoolémie ({str(datetime.fromtimestamp(horMaxi))[11:-3]})!"
                return phr

            elif taux <= self.limit:
                phr= "Vous pouvez conduire"
                return phr

            return self.tauxcond(username)

class Consommation:
    def __init__(self):
        self.alcohol_dialog=None
    
    #Alcohol Name Error Pop-Up
    def alcohol_alert(self):
        if not self.alcohol_dialog:
            self.alcohol_dialog = MDDialog(
                text="Nom d'alcool inconnu, verifiez que vous l'avez ajoute",
                buttons=[
                    MDFlatButton(
                        text="Modifier",
                        on_release = self.alcohol_alert_close,
                        ),
                ],
            )
        self.alcohol_dialog.open()
    
    def alcohol_alert_close(self, obj):
        self.alcohol_dialog.dismiss()

    #Add a Drink in the DataBase
    def addDrink(self, name, dosebar, date, duration, quantite, repas, taux, weight, coeff, elim, username):

        with open('drink.csv', 'r') as f:
            compteur=0
            reader = csv.reader(f , delimiter=';')
            for k in reader:
                compteur+=1

        if compteur==50:
            records=[]
            with open('drink.csv', 'r') as f:
                reader = csv.reader(f , delimiter=';')
                for row in reader:
                    records.append(row)
                records.sort()
                del records[0]
            with open('drink.csv','w',newline='', encoding='utf-8') as fichiercsv:
                writer=csv.writer(fichiercsv, delimiter=';')
                for k in records:
                    writer.writerow(k)
        
        with open('alcohol_list.csv', 'r') as f:
            reader = csv.reader(f , delimiter=';')
            exist=False
            for row in reader:
                    if not row==[]:
                        if row[0]==name:
                            exist=True
        if type(name)!=float and not exist:
            self.alcohol_alert()
        else:
            with open('alcohol_list.csv', 'r') as f:
                reader = csv.reader(f , delimiter=';')
                for row in reader:
                        if not row==[]:
                            if row[0]==name:
                                concentration=row[1]
            if concentration!='':
                deg = concentration
        
            if dosebar == False:
                quant = float(deg)*0.8*float(quantite)/100
            else:
                quant = 11

            #horMaximum, round(tauxMaximum, 2)

            repas=(int(repas[:-1]))/20
            date = date + 900 * repas

            horMaximum = date + int(duration)*60
            tauxMaximum = taux + (quant / (weight * coeff)) - elim * ((horMaximum - date)/60)
            values =[int(date), name, duration, quant, int(horMaximum), round(tauxMaximum, 2), username]
            with open('drink.csv','a',newline='', encoding='utf-8') as fichiercsv:
                writer=csv.writer(fichiercsv, delimiter= ';')
                writer.writerow(values)
            return True
        
class NewUser:
    #Set parameters to new user
    def __init__(self, username, genre, weight, permis):
        self.username = username
        self.gender = genre
        self.weight = weight
        self.permis = permis
        self.coeff, self.elim = self.setCoeff(self.gender)
        self.limit = self.setLimit(self.permis)

    def getWeight(self):
        return self.weight

    def getElim(self):
        return self.elim

    def getCoeff(self):
        return self.coeff

    def getLimit(self):
        return self.limit
    
    def getUsername(self):
        return self.username
    
    @staticmethod
    def setLimit(permis):
        if permis == 'True':
            return 0.2
        else:
            return 0.5

    @staticmethod
    def setCoeff(gender):
        if gender == "Homme":
            coeff = 0.7
            elim = round(0.13 / 60, 4)
        elif gender == "Femme":
            coeff = 0.6
            elim = round(0.0950 / 60, 4)
        return coeff, elim

class DataBase:
    def getDataUpdate(self):
        with open('users.csv', 'r') as f:
            reader = csv.reader(f , delimiter=';')
            for row in reader:
                if row[4]=='True':
                    return row
    
    def SignIn(self, username, weight, driving, gender):
        with open('users.csv','a',newline='', encoding='utf-8') as fichiercsv:
            writer=csv.writer(fichiercsv, delimiter=";")
            writer.writerow([username, weight, int(driving), gender, 'True'])

    def logout(self):
        records=[]
        with open('users.csv', 'r') as f:
            reader = csv.reader(f , delimiter=';')
            for row in reader:
                if row[4]=='True':
                    row[4]='False'
                records.append(row)

        with open('users.csv','w',newline='', encoding='utf-8') as fichiercsv:
            writer=csv.writer(fichiercsv, delimiter=';')
            for k in records:
                writer.writerow(k)
    
    def online(self, username):
        records=[]
        with open('users.csv', 'r') as f:
            reader = csv.reader(f , delimiter=';')
            for row in reader:
                if row[0]==username:
                    row[4]='True'
                records.append(row)

        with open('users.csv','w',newline='', encoding='utf-8') as fichiercsv:
            writer=csv.writer(fichiercsv, delimiter=';')
            for k in records:
                writer.writerow(k)
    
    def UserExist(self, username):
        with open('users.csv', 'r') as f:
            reader = csv.reader(f , delimiter=';')
            for k in reader:
                if k[0]==username:
                    return True
            return False
    
    def AlcExist(self, alcname):
        with open('alcohol_list.csv', 'r') as f:
            reader = csv.reader(f , delimiter=';')
            for k in reader:
                if not k==[]:
                    if k[0]==alcname:
                        return True
            return False
    
    def noSpeCaracters(self, name):
        error=False
        for k in name:
                if k in "_-.,;:!?@&§~^`¨°|()\{\}[]/\<\">#€$¤£²*+=%µ\'":
                    error=True
        return error
    
    def deleteAlcohol(self, alcohol):
        records=[]
        with open('alcohol_list.csv', 'r') as f:
            reader = csv.reader(f , delimiter=';')
            for k in reader:
                if not k==[]:
                    if k[0]!=alcohol:
                        records.append(k)

        with open('alcohol_list.csv','w',newline='', encoding='utf-8') as fichiercsv:
            writer=csv.writer(fichiercsv, delimiter=';')
            for k in records:
                writer.writerow(k)
    
    def deleteDrink(self, date):
        records=[]
        with open('drink.csv', 'r') as f:
            reader = csv.reader(f , delimiter=';')
            for row in reader:
                if not row==[]:
                    if not (row[0]==str(date)):
                        records.append(row)

        with open('drink.csv','w',newline='', encoding='utf-8') as fichiercsv:
            writer=csv.writer(fichiercsv, delimiter=';')
            for k in records:
                writer.writerow(k)
    
    def deleteUser(self):
        records=[]
        username=self.getUsernameOnline()
        with open('users.csv', 'r') as f:
            reader = csv.reader(f , delimiter=';')
            for row in reader:
                if not (row[0]==username):
                    records.append(row)

        with open('users.csv','w',newline='', encoding='utf-8') as fichiercsv:
            writer=csv.writer(fichiercsv, delimiter=';')
            for k in records:
                writer.writerow(k)
        
        drink_records=[]
        with open('drink.csv', 'r') as f:
            reader = csv.reader(f , delimiter=';')
            for row in reader:
                if not row==[]:
                    if not (row[6]==username):
                        drink_records.append(row)

        with open('drink.csv','w',newline='', encoding='utf-8') as fichiercsv:
            writer=csv.writer(fichiercsv, delimiter=';')
            for k in drink_records:
                writer.writerow(k)
        
    
    def LengthAlcList(self):
        with open('alcohol_list.csv', 'r') as f:
            compteur=0
            reader = csv.reader(f , delimiter=';')
            for k in reader:
                if not k==[]:
                    compteur+=1
            return compteur

    def AlcList(self):
        liste=[]
        with open('alcohol_list.csv', 'r') as f:
            data=csv.reader(f , delimiter=';')
            for k in data:
                if not k==[]:
                    liste.append(k)
            return liste
    
    def LengthDrinkList(self):
        compteur=0
        username=self.getUsernameOnline()
        with open('drink.csv', 'r') as f:
            reader = csv.reader(f , delimiter=';')
            for k in reader:
                if not k==[]:
                    if k[6]==username:
                        compteur+=1
        return compteur
    
    def DrinkList(self):
        username=self.getUsernameOnline()
        liste=[]
        with open('drink.csv', 'r') as f:
            reader = csv.reader(f , delimiter=';')
            for row in reader:
                if not row==[]:
                    if row[6]==username:
                        liste.append((row[0], row[1], row[2], row[4], row[5]))
        liste.sort()
        liste.reverse()
        return liste
    
    def AddAlcohol(self, alcname, strength):
        with open('alcohol_list.csv','a',newline='', encoding='utf-8') as fichiercsv:
            writer=csv.writer(fichiercsv, delimiter=";")
            writer.writerow([alcname, strength])
    
    def getUsernameOnline(self):
        with open('users.csv', 'r') as f:
            reader = csv.reader(f , delimiter=';')
            for row in reader:
                if row[4]=='True':
                    return row[0]
    
    def UpdateUserData(self, username, weight, driving, gender):
        records=[]
        with open('users.csv', 'r') as f:
            reader = csv.reader(f , delimiter=';')
            for row in reader:
                if row[4]=='True':
                    row[0]=username
                    row[1]=weight
                    row[2]=driving
                    row[3]=gender
                records.append(row)

        with open('users.csv','w',newline='', encoding='utf-8') as fichiercsv:
            writer=csv.writer(fichiercsv, delimiter=';')
            for k in records:
                writer.writerow(k)


        