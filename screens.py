#classes import
import time
from datetime import datetime
import main
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.pickers import MDTimePicker, MDDatePicker

#initialization of all app screens
class App():
    def __init__(self):
        HomePage()
        LoginWindow()
        SigninWindow()
        MyAlcoholsPage()
        Drinks()
        AddDrink()
        AddAlcohol()
        SettingPage()
        WindowManager()

#Home Screen
class HomePage(main.Engine, Screen, Widget):

    #User inputs getter
    username=ObjectProperty(None)
    alcoolemie=ObjectProperty(None)
    symptomes=ObjectProperty(None)
    info=ObjectProperty(None)

    #Update all infos on the Main Screen
    def update(self):

        super().init(database=True)
        data=super().getDataBase().getDataUpdate()
        if data[2]=='False': valuePermis=False
        else: valuePermis=True
        self.valueUsername, self.valueWeight, self.valueGenre=data[0],data[1],data[3]

        #Update Text Displays
        super().init(self.valueUsername, self.valueGenre, self.valueWeight, valuePermis)
        self.ids.username.text=super().getUser().getUsername()
        self.ids.alcoolemie.text=str(super().getTaux().getTaux(self.ids.username.text))+"g/L"
        self.ids.symptomes.text=super().getTaux().getSymptomes(self.ids.username.text)
        self.ids.info.text=str(super().getTaux().taux0(self.ids.username.text))+"\n"+str(super().getTaux().conduiteaut(self.ids.username.text))

    #Update the Online Status on the DataBase
    def logout(self):
        super().init(database=True)
        super().getDataBase().logout()
        self.ids.username.text=""
        self.ids.alcoolemie.text=""
        self.ids.symptomes.text=""
        self.ids.info.text=""

#Login Screen
class LoginWindow(main.Engine, Screen):

    user= ObjectProperty(None)
    username_dialog=None

    #Delete the user input
    def clear(self):
        self.user.text = ""

    #Alert Pop-Up if username input is incorrect
    def username_alert(self):
        if not self.username_dialog:
            
            self.username_dialog = MDDialog(
                text="Nom d'utilisateur inconnu",
                buttons=[
                    MDFlatButton(
                        text="Modifier",
                        on_release = self.username_alert_close,
                        ),
                ],
            )
        self.username_dialog.open()
    
     #Close Alert Pop-Up
    def username_alert_close(self, obj):
        self.username_dialog.dismiss()

    #Update the Online Status on the DataBase
    def login(self):
        username=self.ids.user.text

        #Username Validity Check
        super().init(database=True)
        error=super().getDataBase().noSpeCaracters(username)
        if error:
            self.username_alert()
            self.clear()
        else:
            exist=super().getDataBase().UserExist(username)
            if not exist:
                self.username_alert()
                self.clear()
            else:
                super().init(database=True)
                super().getDataBase().online(username)
                self.clear()
                self.manager.current='home'

#Signin Screen
class SigninWindow(main.Engine, Screen):
    #Retrieving Data of the new user
    username = ObjectProperty(None)
    weight = ObjectProperty(None)

    checkbox_homme = ObjectProperty(None)
    checkbox_femme = ObjectProperty(None)
    checkbox_permis = ObjectProperty(None)    
    
    permis= False
    homme= False
    femme= False

    username_dialog=None
    genre_dialog=None

    #Pop-Up Alert if the username is incorrect 
    def username_alert(self):
        if not self.username_dialog:
            
            self.username_dialog = MDDialog(
                text="Nom d'utilisateur invalide ou deja utilise",
                buttons=[
                    MDFlatButton(
                        text="Modifier",
                        on_release = self.username_alert_close,
                        ),
                ],
            )
        self.username_dialog.open()
    
    def username_alert_close(self, obj):
        self.username_dialog.dismiss()

    #Pop-Up Alert if the gender is unknown
    def genre_alert(self):
        if not self.genre_dialog:
            
            self.genre_dialog = MDDialog(
                text="Veuillez renseigner votre sexe",
                buttons=[
                    MDFlatButton(
                        text="Modifier",
                        on_release = self.genre_alert_close,
                        ),
                ],
            )
        self.genre_dialog.open()

    def genre_alert_close(self, obj):
        self.genre_dialog.dismiss()

    #Updating variables based on user input
    def slide_it(self, *args):
        self.weight.text= str(int(args[1]))

    def homme_click(self, instance, value):
        self.homme=value
    
    def femme_click(self, instance, value):
        self.femme=value

    def permis_click(self, instance, value):
        self.permis=value

    def disable_button(self):
        if self.ids.checkbox_homme.active == True:
            self.ids.checkbox_femme.disabled = True
        elif self.ids.checkbox_femme.active == True:
            self.ids.checkbox_homme.disabled = True
    
    def enable_button(self):
        if self.ids.checkbox_femme.active == False:
            self.ids.checkbox_homme.disabled = False
        if self.ids.checkbox_homme.active == False:
            self.ids.checkbox_femme.disabled = False
    

    def press(self):

        #Updating variables based on user input
        username = self.username.text
        weight = self.weight.text
        genre=None

        if self.homme==False and self.femme==False:
            self.genre_alert()

        else:
            super().init(database=True)

            #Check no special characters in username or multiples user 
            error=super().getDataBase().noSpeCaracters(username)
            if error:
                self.username_alert()
                self.ids.username.text=""
            else:
                exist=super().getDataBase().UserExist(username)
                if exist:
                    self.username_alert()
                    self.ids.username.text=""
                else:
                    if self.homme:
                        genre="Homme"
                    elif self.femme:
                        genre="Femme"           

                    #Calling the method to register the user
                    self.submit(username.lower(), weight, self.permis, genre)

                    #Clear the Input boxes
                    self.username.text = ""
                    self.weight.text = ""
                    if self.ids.checkbox_femme.active == True:
                        self.ids.checkbox_femme.active = False
                    if self.ids.checkbox_homme.active == True:
                        self.ids.checkbox_homme.active = False
                    if self.ids.checkbox_permis.active == True:
                        self.ids.checkbox_permis.active = False
                    self.ids.slider.value=0

    #Register the User
    def submit(self, username, weight, driving, gender):
        
        #Register the New User
        super().init(database=True)
        super().getDataBase().SignIn(username, weight, driving, gender)

        self.manager.current='home'

#Alcohols Inventory Screen
class MyAlcoholsPage(main.Engine, Screen):

    container=ObjectProperty(None)

    #Delete the Pressed Alcohol
    def delete(self, alcohol):
        super().init(database=True)
        super().getDataBase().deleteAlcohol(alcohol)
        self.update_list()

    def update_list(self):
        super().init(database=True)
        
        #Creating an Empty Container
        self.ids.container.clear_widgets()

        #Check the number of alcohols added
        count=super().getDataBase().LengthAlcList()
        #Stores all alcohols and their concentration
        records=super().getDataBase().AlcList()
        for i in range(count):
            if not records[i]==[]:
                alcohol=records[i][0]
                strength=records[i][1]
                #We create a new element in our container/Alcohol List
                self.ids.container.add_widget(
                    TwoLineListItem(text=str(alcohol),  secondary_text= str(strength)+"°", on_press=lambda x: self.delete(x.text))
                    )

#Alcohols Consumptions Screen
class Drinks(main.Engine, Screen):
    container=ObjectProperty(None)

    #Delete the Pressed Drink
    def delete(self, date):
        super().init(database=True)

        #Convert Date to TimeStamp
        date=int(time.mktime(time.strptime(str(date),"%Y-%m-%d %H:%M")))

        super().getDataBase().deleteDrink(date)
        self.on_start()

    def on_start(self):
        super().init(database=True)
        #Creating an Empty Container
        self.ids.container.clear_widgets()

        #Stores all drinks and their data
        count=super().getDataBase().LengthDrinkList()
        records=super().getDataBase().DrinkList()
        records.sort(reverse=True)

        for i in range(count):
            #Retrieving Data
            date=int(records[i][0])
            date=str(datetime.fromtimestamp(date))[:-3]
            alcname=records[i][1]
            duration=str(records[i][2])
            hormax=int(records[i][3])
            hormax=str(datetime.fromtimestamp(hormax))[:-3]
            tauxmax=str(records[i][4])
            #We create a new element in our container/Drink List
            self.ids.container.add_widget(
                TwoLineListItem(text=f"{date}",  secondary_text=f"{alcname}, {duration}=min, tauxmax:{hormax}, tauxmax:{tauxmax}", on_press=lambda x: self.delete(x.text))
                )
    
#Add Consumption Screen
class AddDrink(main.Engine, Screen):
    #User inputs Initialization
    dosebar = ObjectProperty(None)
    alcname= ObjectProperty(None)
    alcvolume= ObjectProperty(None)
    duration=ObjectProperty(None)
    repas=ObjectProperty(None)
    time=ObjectProperty(None)
    bar=False
    alcvolume=None
    volume_dialog=None 
    #Check if DoseBar is pressed
    def bar_click(self, instance, value):
        self.bar=value
    
    def disable_volume(self):
        if self.ids.dosebar.active == True:
            self.ids.alcvolume.disabled = True
                
    def enable_volume(self):
        if self.ids.dosebar.active == False:
            self.ids.alcvolume.disabled = False

    #Initialization of the Duration Slider
    def slide_it(self, *args):
        self.duration.text= str(int(args[1]))
    
    #Initialization of the Meal Consistency Slider
    def slide_it_meal(self, *args):
        self.repas.text= str(int(args[1]))+'%'

    #5 Methods for the Time Picker
    def on_canceltime(self, instance, time):
        self.ids.time_label.text=self.set_txttime()

    def show_time_picker(self):
        time_dialog=MDTimePicker()
        default_time = time.ctime().split()[3]
        default_time = datetime.strptime(default_time, '%H:%M:%S').time()
        time_dialog.set_time(default_time)
        time_dialog.bind(time=self.get_time, on_cancel=self.on_canceltime)
        time_dialog.open()
    
    def get_time(self, instance, time):
        timetxt=str(time)[:-3]
        phr1=timetxt[:2]
        phr2=timetxt[3:]
        timetxt=phr1+'h'+phr2
        self.ids.time_label.text=timetxt
    
    def set_txttime(self):
        time=str(datetime.strptime(str(datetime.now().time())[:8], '%H:%M:%S').time())[:-3]
        phr1=time[:2]
        phr2=time[3:]
        time=phr1+'h'+phr2
        return time

    def getTime(self):
        timetxt=self.ids.time_label.text
        phr1=timetxt[:2]
        phr2=timetxt[3:]
        return phr1, phr2
    
    #6 Methods for the Time Picker
    def show_date_picker(self):
        year, month, day=self.datenow()
        date_dialog = MDDatePicker(year=year, month=month, day=day)
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
        
    def on_cancel(self, instance, value):
        self.ids.date_label.text=self.datetext()
    
    def datenow(self):
        date=str(datetime.now())
        year, month, day=int(date[:4]), int(date[5:7]), int(date[8:10])
        return year, month, day

    def datetext(self):
        date=str(datetime.now())
        year, month, day=int(date[:4]), int(date[5:7]), int(date[8:10])
        phr=str(day)+"/"+str(month)+"/"+str(year)
        return phr

    def on_save(self, instance, value, date_range):
        year=str(value)[:4]
        month=str(value)[5:7]
        day=str(value)[-2:]
        self.ids.date_label.text= str(day)+"/"+str(month)+"/"+str(year)
    
    def getDate(self):
        date=self.ids.date_label.text
        year=str(date[-4:])
        month=str(date[3:5])
        day=str(date[:2])
        return day, month, year

    #Pop-Up Alert if no Drink Volume is informed
    def volume_alert(self):
        if not self.volume_dialog:
            
            self.volume_dialog = MDDialog(
                text="Aucun Volume de boisson n'a été renseigné, veuillez le renseigner ou cocher la case Dose Bar",
                buttons=[
                    MDFlatButton(
                        text="Modifier",
                        on_release = self.volume_alert_close,
                        ),
                ],
            )
        self.volume_dialog.open()
    
    def volume_alert_close(self, obj):
        self.volume_dialog.dismiss()

    def on_press(self):
        
        #Retrieving User Inputs
        alcname=self.alcname.text
        dosebar=self.ids.dosebar.active
        timed=self.getTime()
        date=self.getDate()
        timest=f"{date[0]}-{date[1]}-{date[2]} {timed[0]}:{timed[1]}"
        date=int(time.mktime(time.strptime(str(timest),"%d-%m-%Y %H:%M")))
        duration=self.duration.text
        alcquant=self.alcvolume.text
        repas=self.repas.text    
        if dosebar==False and alcquant=='':
            self.volume_alert()
        else:

            #Retrieving User Data
            super().init(database=True)
            data=super().getDataBase().getDataUpdate()
            if data[2]=='False': valuePermis=False
            else: valuePermis=True
            self.valueUsername, self.valueWeight, self.valueGenre=data[0],int(data[1]), data[3]
            super().init(self.valueUsername, self.valueGenre, self.valueWeight, valuePermis)

            #Check in the super class if all inputs are correct
            if super().getConso().addDrink(alcname, dosebar, date, duration, alcquant, repas, super().getTaux().getTaux(date), super().getUser().getWeight(), super().getUser().getCoeff(), super().getUser().getElim(), super().getUser().getUsername())==True:
                self.manager.current='home'
            #Clear Inputs
            self.alcname.text = ""
            self.ids.dosebar.active=False
            self.alcvolume.text=""

#Add Alcohol Screen
class AddAlcohol(main.Engine, Screen):
    #Initialization of Data Inputs
    newalcname=ObjectProperty(None)
    newconcentration=ObjectProperty(None)
    alcname=""
    concentration=""
    alcohol_dialog=None

    #Alcohol Strength Slider Value Getter
    def slide_it(self, *args):
        self.newconcentration.text= str(float(args[1]))

    def press(self):
        self.alcname=self.newalcname.text
        self.concentration=self.newconcentration.text
        self.submit(self.alcname.lower(), self.concentration)
        self.newalcname.text = ""
        self.newconcentration.text = ""
        self.ids.slider.value=0

    def alcohol_alert(self):
        if not self.alcohol_dialog:
            self.alcohol_dialog = MDDialog(
                text="Nom d'alcool invalide ou deja existant",
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

    def submit(self):
        super().init(database=True)
        
        #Retrieving User Input
        self.alcname=self.newalcname.text
        self.alcname=self.alcname.lower()
        self.concentration=self.newconcentration.text

        #Check if Alcohol already exist or if there are special caracters in alcohol name
        error=super().getDataBase().noSpeCaracters(self.alcname)
        exist=super().getDataBase().AlcExist(self.alcname)
        if error or exist:
            self.alcohol_alert()
            self.newalcname.text=""

        else:
            #add a record
            super().getDataBase().AddAlcohol(self.alcname, self.concentration)
            self.manager.current='alcohols'

            self.newalcname.text = ""
            self.newconcentration.text = ""
            self.ids.slider.value=0
    
#Settings Screen
class SettingPage(main.Engine, Screen):

    #Initialization User Inputs
    username = ObjectProperty(None)
    weight = ObjectProperty(None)
    username_dialog=None
    genre_dialog=None
    checkbox_homme = ObjectProperty(None)
    checkbox_femme = ObjectProperty(None)
    checkbox_permis = ObjectProperty(None)    
        
    #Pop Up Alert if gender is not specified
    def genre_alert(self):
        if not self.genre_dialog:
            
            self.genre_dialog = MDDialog(
                text="Veuillez renseigner votre sexe",
                buttons=[
                    MDFlatButton(
                        text="Modifier",
                        on_release = self.genre_alert_close,
                        ),
                ],
            )
        self.genre_dialog.open()

    def genre_alert_close(self, obj):
        self.genre_dialog.dismiss()

    #Pop Up Alert if username is incorrect
    def username_alert(self):
        if not self.username_dialog:
            
            self.username_dialog = MDDialog(
                text="Nom d'utilisateur invalide ou deja utilise",
                buttons=[
                    MDFlatButton(
                        text="Modifier",
                        on_release = self.username_alert_close,
                        ),
                ],
            )
        self.username_dialog.open()
    
    def username_alert_close(self, obj):
        self.username_dialog.dismiss()


    def update(self):
        #Complete Inputs with User Data
        super().init(database=True)
        data=super().getDataBase().getDataUpdate()
        if data[2]=='False': valuePermis=False
        else: valuePermis=True
        valueUsername, valueWeight, valueGenre=data[0],data[1], data[3]
        self.ids.username.text=valueUsername
        self.ids.slider.value=valueWeight
        self.weight.text=str(valueWeight)

        if valueGenre=="Homme":
            self.ids.checkbox_homme.active= True
            self.ids.checkbox_femme.active= False
            if valuePermis==True:
                self.ids.checkbox_permis.active= True

        elif valueGenre=="Femme":
            self.ids.checkbox_femme.active=True
            self.ids.checkbox_homme.active=False
            print(valuePermis)
            if valuePermis==True:
                self.ids.checkbox_permis.active= True

    def slide_it(self, *args):
        self.weight.text= str(int(args[1]))

    def homme_click(self, instance, value):
        self.homme=value
    
    def femme_click(self, instance, value):
        self.femme=value

    def permis_click(self, instance, value):
        self.permis=value

    def disable_button(self):
        if self.ids.checkbox_homme.active == True:
            self.ids.checkbox_femme.disabled = True
        elif self.ids.checkbox_femme.active == True:
            self.ids.checkbox_homme.disabled = True
    
    def enable_button(self):
        if self.ids.checkbox_femme.active == False:
            self.ids.checkbox_homme.disabled = False
        if self.ids.checkbox_homme.active == False:
            self.ids.checkbox_femme.disabled = False
    
    #Retrieving User Data Changes
    def press(self):        
        username = self.username.text
        weight = self.weight.text
        permis=self.ids.checkbox_permis.active

        if self.ids.checkbox_homme.active == False and self.ids.checkbox_femme.active == False:
            self.genre_alert()
        else:
            if self.ids.checkbox_homme.active == True:
                genre="Homme"
            elif self.ids.checkbox_femme.active == True:
                genre="Femme"
            self.submit(username.lower(), weight, permis, genre)


    #Update User Data in the DataBase
    def submit(self, username, weight, driving, gender):  
        super().init(database=True)

        #Check if there are no special caracters in the input
        error=super().getDataBase().noSpeCaracters(username)
        if error:
            self.username_alert()
            self.ids.username.text=""

        else:
            #check if the new username already exist
            exist=super().getDataBase().UserExist(username)
            active_user=super().getDataBase().getUsernameOnline()
            if exist and active_user!=username:
                self.username_alert()
                self.ids.username.text=""
            else:
                #Update User Data
                super().getDataBase().UpdateUserData(username, weight, driving, gender)
                self.manager.current='home'

    #Delete Account
    def delete(self):
        super().init(database=True)
        super().getDataBase().deleteUser()

#Screens Manager
class WindowManager(ScreenManager):
    pass