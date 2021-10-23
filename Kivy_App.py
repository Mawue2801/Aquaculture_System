from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.picker import MDTimePicker
from kivymd.uix.menu import MDDropdownMenu
import datetime
import time
import serial
import serial.tools.list_ports
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.toast import toast
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import TwoLineListItem
from bs4 import BeautifulSoup
import requests
import threading

Window.size = (800,480)

class ListItemWithCheckbox(OneLineAvatarIconListItem):
    icon = StringProperty("delete")

class ListItemWithCheckbox2(OneLineAvatarIconListItem):
    icon = StringProperty("delete")

class CredentialsContent(BoxLayout):
    pass


class MainApp(MDApp):
    dialog1 = None
    dialog2 = None
    dialog3 = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("LoginScreen.kv"))
        screen_manager.add_widget(Builder.load_file("SystemSettingsScreen.kv"))
        screen_manager.add_widget(Builder.load_file("MainScreen.kv"))
        self.selected_pond = "Pond 1"
        self.securityQuestion = ""
        self.securityAnswer = ""
        self.selected_species_2 = "Nile Tilapia"
        self.selected_species = "Nile Tilapia"
        self.username = "smart aquapak"
        self.password = "fish1234"
        self.setSystem = False
        self.approveSpeciesChange = False
        self.num_of_ponds = 0
        self.RedStatus = 0
        self.pondDict = {}
        self.feedingList = []
        self.useMeteorologicalData = False
        self.start_date = datetime.date.today()

        self.TilapiaFeeding = {
                            1:[0.11,0,40,0.8,4],
                            2:[0.18,0.14,40,1,4],
                            4:[0.26,0.29,40,1,4],
                            8:[0.42,0.57,40,2,4],
                            12:[0.55,0.57,40,2,4],
                            17:[0.73,0.7,35,3,3],
                            24:[0.96,1.0,35,3,3],
                            32:[1.16,1.2,35,3,3],
                            43:[1.45,1.5,35,3,3],
                            55:[1.70,1.7,35,3,3],
                            68:[1.97,1.9,35,3,3],
                            83:[2.28,2.2,35,3,3],
                            100:[2.60,2.4,35,3,3],
                            118:[2.84,2.6,35,3,3],
                            137:[3.14,2.6,35,3,2],
                            155:[3.58,2.7,32,"5 mix",2],
                            174:[3.84,2.7,32,"5 mix",2],
                            195:[4.28,2.9,32,"5 mix",2],
                            215:[4.51,2.9,32,5,2],
                            236:[4.72,3.0,32,5,2],
                            257:[5.14,3.0,32,5,2],
                            278:[5.42,3.0,32,5,2],
                            299:[5.68,3.0,32,5,2],
                            320:[5.92,3.0,32,5,2],
                            341:[6.14,3.0,32,5,2],
                            363:[6.53,3.1,32,5,2],
                            384:[6.53,3.1,32,5,2],
                            407:[6.92,3.2,32,5,2],
                            430:[7.09,3.2,32,5,2],
                            451:[7.21,3.3,32,5,2]
                            }
        self.CatfishFeeding = {
                            10:[0.5,0.5,36,3,4],
                            14:[0.7,0.6,36,3,4],
                            23:[1.0,1.2,36,3,4],
                            33:[1.3,1.4,36,3,4],
                            45:[1.7,1.7,36,3,3],
                            59:[2.1,2.0,36,3,3],
                            77:[2.6,2.6,36,3,2],
                            97:[2.9,2.8,32,3,2],
                            122:[3.7,3.7,32,3,2],
                            150:[4.1,4.0,32,3,2],
                            182:[4.6,4.6,32,5,2],
                            217:[5.2,4.9,32,5,2],
                            252:[6.0,5.0,32,5,2],
                            288:[5.8,5.1,32,5,2],
                            323:[5.8,5.1,32,5,2],
                            359:[6.5,5.1,32,5,2],
                            395:[7.1,5.1,32,5,1],
                            430:[6.5,5.1,32,5,1],
                            466:[7.0,5.1,32,5,1],
                            502:[7.5,5.1,32,5,1],
                            537:[7.5,5.1,32,5,1],
                            573:[8.0,5.1,32,5,1],
                            609:[7.9,5.1,32,5,1],
                            645:[8.4,5.1,32,5,1],
                            680:[8.2,5.1,32,5,1],
                            716:[8.6,5.1,32,5,1],
                            752:[9.0,5.1,32,5,1],
                            787:[8.7,5.1,32,5,1],
                            823:[9.1,5.1,32,5,1],
                            859:[9.4,5.1,32,5,1],
                            894:[9.8,5.1,32,5,1],
                            930:[9.3,5.1,32,5,1],
                            966:[9.7,5.1,32,5,1],
                            1002:[10.0,5.1,32,5,1],
                            1037:[10.4,5.1,32,5,1],
                            1073:[10.7,5.1,32,5,1],
        }
        
        species = ["Nile Tilapia", "Catfish", "Shrimp", "Prawn"]
        species_menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": species[i],
                "height": dp(56),
                "on_release": lambda x=species[i]: self.set_species_item(x),
            } for i in range(4)
        ]
        self.species_menu = MDDropdownMenu(
            caller=screen_manager.get_screen("MainScreen").ids.species_selection,
            items=species_menu_items,
            width_mult=4,
        )
        self.species_menu.bind()

        # Species Menu for System Settings Page
        species_menu_items_2 = [
            {
                "viewclass": "OneLineListItem",
                "text": species[i],
                "height": dp(56),
                "on_release": lambda x=species[i]: self.set_species_item_2(x),
            } for i in range(4)
        ]
        self.species_menu_2 = MDDropdownMenu(
            caller=screen_manager.get_screen("SystemSettingsScreen").ids.species_selection,
            items=species_menu_items_2,
            width_mult=4,
        )
        self.species_menu_2.bind()

    def set_pond_item(self, text_item):
        screen_manager.get_screen("MainScreen").ids.pond_selection.set_item(text_item)
        #self.selected_pond = text_item.split(" ")[1]
        self.selected_pond = text_item
        self.pond_menu.dismiss()
        self.selected_species = self.pondDict[text_item][0]
        self.root.get_screen("MainScreen").ids.fish_count.text = self.pondDict[text_item][1]
        screen_manager.get_screen("MainScreen").ids.species_selection.set_item(self.pondDict[text_item][0])
        self.root.get_screen("MainScreen").ids.feeding_time_list.clear_widgets()
        if len(self.pondDict[text_item][2]) != 0:
            for time in self.pondDict[text_item][2]:
                self.root.get_screen("MainScreen").ids.feeding_time_list.add_widget(ListItemWithCheckbox(text=time,icon=f"clock-time-{self.time_dict[time[0:2]]}-outline"))
        self.root.get_screen("MainScreen").ids.minDO.text = self.pondDict[text_item][3][0]
        self.root.get_screen("MainScreen").ids.maxDO.text = self.pondDict[text_item][3][1]
        self.root.get_screen("MainScreen").ids.minTemp.text = self.pondDict[text_item][3][2]
        self.root.get_screen("MainScreen").ids.maxTemp.text = self.pondDict[text_item][3][3]
        self.root.get_screen("MainScreen").ids.minpH.text = self.pondDict[text_item][3][4]
        self.root.get_screen("MainScreen").ids.maxpH.text = self.pondDict[text_item][3][5]
        self.root.get_screen("MainScreen").ids.minSalinity.text = self.pondDict[text_item][3][6]
        self.root.get_screen("MainScreen").ids.maxSalinity.text = self.pondDict[text_item][3][7]

    def set_species_item(self, text_item):
        screen_manager.get_screen("MainScreen").ids.species_selection.set_item(text_item)
        self.pondDict[self.selected_pond][0] = text_item
        self.selected_species = text_item
        self.reset_default()
        self.species_menu.dismiss()
        self.species_change_alert()

    def set_species_item_2(self, text_item):
        screen_manager.get_screen("SystemSettingsScreen").ids.species_selection.set_item(text_item)
        self.selected_species_2 = text_item
        self.species_menu_2.dismiss()
    
    def species_change_alert(self):
        if not self.dialog3:
            self.dialog3 = MDDialog(
                text="Species for Selected Pond Changed",
                buttons=[
                    MDFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color,on_release=self.close_dialog3
                    ),
                ],
            )
        self.dialog3.open()

    def close_dialog3(self,obj):
        self.dialog3.dismiss()
    
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        try:
            ports = serial.tools.list_ports.comports()
            for i in ports:
                i = str(i)
                if 'Arduino' in i:
                    commPort = i.split(' ')[0]
                if commPort != 'None':
                    self.arduino = serial.Serial(commPort,baudrate = 9600, timeout=1)
                    print('Connected to ' + commPort)
        except:
            print('Connection Issue!')
        Clock.schedule_interval(self.update, 1)
        Clock.schedule_interval(self.update_time, 1)
        return screen_manager

    def set_system(self):
        self.num_of_ponds = len(self.pondDict)
        pond_menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"Pond {i}",
                "height": dp(56),
                "on_release": lambda x=f"Pond {i}": self.set_pond_item(x),
            } for i in range(1,self.num_of_ponds+1)
        ]
        self.pond_menu = MDDropdownMenu(
            caller=screen_manager.get_screen("MainScreen").ids.pond_selection,
            items=pond_menu_items,
            width_mult=4,
        )
        self.pond_menu.bind()

        screen_manager.current = "MainScreen"
        name = self.username 
        toast(f"Welcome {name}")
        self.selected_species = self.pondDict["Pond 1"][0]
        self.root.get_screen("MainScreen").ids.fish_count.text = self.pondDict["Pond 1"][1]
        screen_manager.get_screen("MainScreen").ids.species_selection.set_item(self.pondDict["Pond 1"][0])

        self.root.get_screen("MainScreen").ids.minDO.text = self.pondDict["Pond 1"][3][0]
        self.root.get_screen("MainScreen").ids.maxDO.text = self.pondDict["Pond 1"][3][1]
        self.root.get_screen("MainScreen").ids.minTemp.text = self.pondDict["Pond 1"][3][2]
        self.root.get_screen("MainScreen").ids.maxTemp.text = self.pondDict["Pond 1"][3][3]
        self.root.get_screen("MainScreen").ids.minpH.text = self.pondDict["Pond 1"][3][4]
        self.root.get_screen("MainScreen").ids.maxpH.text = self.pondDict["Pond 1"][3][5]
        self.root.get_screen("MainScreen").ids.minSalinity.text = self.pondDict["Pond 1"][3][6]
        self.root.get_screen("MainScreen").ids.maxSalinity.text = self.pondDict["Pond 1"][3][7]

        self.setSystem = True

    def log_in(self):
        if self.root.get_screen("LoginScreen").ids.user.text == self.username and self.root.get_screen("LoginScreen").ids.password.text == self.password:
           if self.setSystem == False:
               screen_manager.current = "SystemSettingsScreen" 
               self.root.get_screen("LoginScreen").ids.user.text = ""
               self.root.get_screen("LoginScreen").ids.password.text = ""
           else:
                name = self.username
                toast(f"Welcome {name}")
                screen_manager.current = "MainScreen" 
                self.root.get_screen("LoginScreen").ids.user.text = ""
                self.root.get_screen("LoginScreen").ids.password.text = ""
        else:                           
            toast("Invalid Username or Password")
            
    def log_out(self):
        screen_manager.current = "LoginScreen"
    
    def get_time(self,instance,time):
        self.root.get_screen("MainScreen").ids.feeding_time_label.text = str(time)
    
    def add_to_ponds_dict(self):
        self.num_of_ponds += 1
        name = "Pond " + str(self.num_of_ponds)
        species = self.selected_species_2
        count = self.root.get_screen("SystemSettingsScreen").ids.fish_count.text

        if species == "Catfish":
            species += "       "
        elif species == "Shrimp":
            species += "       "
        elif species == "Prawn":
            species += "         "

        if len(count) == 1:
            self.root.get_screen("SystemSettingsScreen").ids.pond_identities_list.add_widget(ListItemWithCheckbox2(text=f"{name}                    {species}                   {count}"))
        elif len(count) == 2:
            self.root.get_screen("SystemSettingsScreen").ids.pond_identities_list.add_widget(ListItemWithCheckbox2(text=f"{name}                    {species}                   {count}"))
        elif len(count) == 3:
            self.root.get_screen("SystemSettingsScreen").ids.pond_identities_list.add_widget(ListItemWithCheckbox2(text=f"{name}                    {species}                   {count}"))
        elif len(count) == 4:
            self.root.get_screen("SystemSettingsScreen").ids.pond_identities_list.add_widget(ListItemWithCheckbox2(text=f"{name}                    {species}                   {count}"))
        

        if self.selected_species_2 == "Nile Tilapia":
            self.pondDict[name] = [self.selected_species_2,count,[],["4","8","12","42","7.5","8.5","0","0.5"],[]]
        elif self.selected_species_2 == "Catfish":
            self.pondDict[name] = [self.selected_species_2,count,[],["4","8","9","37","7.5","8.5","0","0.5"],[]]
        elif self.selected_species_2 == "Shrimp":
            self.pondDict[name] = [self.selected_species_2,count,[],["4","8","14","40","7.5","8.5","0","0.5"],[]]
        elif self.selected_species_2 == "Prawn":
            self.pondDict[name] = [self.selected_species_2,count,[],["4","8","14","36","7.5","8.5","0","0.5"],[]]


    def add_to_feeding_list(self):
        self.time_dict = {"00":"twelve","01":"one","02":"two","03":"three","04":"four","05":"five","06":"six",
                    "07":"seven","08":"eight","09":"nine","10":"ten","11":"eleven","12":"twelve","13":"one",
                    "14":"two","15":"three","16":"four","17":"five","18":"six","19":"seven","20":"eight",
                    "21":"nine","22":"ten","23":"eleven"}
        time = self.root.get_screen("MainScreen").ids.feeding_time_label.text
        if time not in self.pondDict[self.selected_pond][2]:
            self.root.get_screen("MainScreen").ids.feeding_time_list.add_widget(ListItemWithCheckbox(text=time,icon=f"clock-time-{self.time_dict[time[0:2]]}-outline"))
            self.pondDict[self.selected_pond][2].append(time)
        else:
            toast("Selected time is already in the list")

    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()
    
    def save_fish_count(self,text):
        self.pondDict[self.selected_pond][1] = self.root.get_screen("MainScreen").ids.fish_count.text

    def save_minDO(self,text):
        self.pondDict[self.selected_pond][3][0] = self.root.get_screen("MainScreen").ids.minDO.text

    def save_maxDO(self,text):
        self.pondDict[self.selected_pond][3][1] = self.root.get_screen("MainScreen").ids.maxDO.text

    def save_minTemp(self,text):
        self.pondDict[self.selected_pond][3][2] = self.root.get_screen("MainScreen").ids.minTemp.text

    def save_maxTemp(self,text):
        self.pondDict[self.selected_pond][3][3] = self.root.get_screen("MainScreen").ids.maxTemp.text
    
    def save_minpH(self,text):
        self.pondDict[self.selected_pond][3][4] = self.root.get_screen("MainScreen").ids.minpH.text

    def save_maxpH(self,text):
        self.pondDict[self.selected_pond][3][5] = self.root.get_screen("MainScreen").ids.maxpH.text

    def save_minSalinity(self,text):
        self.pondDict[self.selected_pond][3][6] = self.root.get_screen("MainScreen").ids.minSalinity.text

    def save_maxSalinity(self,text):
        self.pondDict[self.selected_pond][3][7] = self.root.get_screen("MainScreen").ids.maxSalinity.text

    def update_time(self, *args):
        self.today = datetime.date.today()
        self.date = self.today.strftime("%b-%d-%Y")
        t = time.localtime()
        self.current_time = time.strftime("%H:%M:%S",t)
        self.root.get_screen("MainScreen").ids.date_label.text = str(self.date)
        self.root.get_screen("MainScreen").ids.time_label.text = str(self.current_time)

        self.current_week = int((self.today-self.start_date).days/7) + 1
        self.root.get_screen("MainScreen").ids.week_label.text = "Week " + str(self.current_week)

        weight = self.root.get_screen("MainScreen").ids.fish_weight.text
        
        if self.setSystem == True:
            for name in list(self.pondDict.keys()):
                if self.current_time in self.pondDict[name][2]:
                    print(f"Feeder Turned on for {name}")

            if self.useMeteorologicalData == True:
                if str(self.current_time)[3:] == "00:00":
                    threading.Thread(target = self.fetch_meteorological_data).start()

            if weight == "":
                weight=0
            weight = int(weight)

            if self.selected_species == "Nile Tilapia":
                FeedingDict = self.TilapiaFeeding
            elif self.selected_species == "Catfish":
                FeedingDict = self.CatfishFeeding

            FeedingDictKeys = list(FeedingDict.keys())

            if weight in FeedingDictKeys:
                print(FeedingDict[weight][0])
            elif weight == 0:
                pass
            else:
                FeedingDictKeys.append(weight)
                FeedingDictKeys.sort()
                Approximation = FeedingDictKeys[FeedingDictKeys.index(weight) - 1]
                print(FeedingDict[Approximation][0])

    def remove_widget(self,widget):
        self.root.get_screen("MainScreen").ids.feeding_time_list.remove_widget(widget)
        self.pondDict[self.selected_pond][2].remove(widget.text)
        
    def remove_widget_2(self,widget):
        name = widget.text.split(" ")[0]
        name = name + " " + widget.text.split(" ")[1]
        self.root.get_screen("SystemSettingsScreen").ids.pond_identities_list.remove_widget(widget)
        del self.pondDict[name]
        print(self.pondDict)
    
    def update(self, *args):
        if self.setSystem == True:
            try:
                arduino = self.arduino
                data = str(arduino.readline(arduino.inWaiting()).decode()).split("-")
                pondIdentity = "Pond " + data[0]
                sensorValues = data[1].split(",")
                self.pondDict[pondIdentity][4] = sensorValues
                print(sensorValues)
                if len(self.pondDict[self.selected_pond][4]) == 2:
            #         self.root.get_screen("MainScreen").ids.do_label.text = data[0]
                    self.root.get_screen("MainScreen").ids.temp_label.text = self.pondDict[self.selected_pond][4][0]
                    self.root.get_screen("MainScreen").ids.pH_label.text = self.pondDict[self.selected_pond][4][1].replace("\r\n","")
                    arduino.write(b"A1")
            #         self.root.get_screen("MainScreen").ids.water_level_label.text = data[3]
            #         self.root.get_screen("MainScreen").ids.turbidity_label.text = data[4]
            #         salinityLevel = (float(data[5].replace("\r\n",""))**1.0878)*466.5
            #         self.root.get_screen("MainScreen").ids.salinity_label.text = str(salinityLevel)
            #         if len(data) == 6:
            #             if float(data[0]) < 4 and self.RedStatus == 0:
            #                 arduino.write(b"R")
            #                 self.RedStatus = 1
            #                 CurrentDate = self.date
            #                 CurrentTime = self.time
            #                 self.root.get_screen("MainScreen").ids.history_list.add_widget(TwoLineListItem(text="Red LED Turned On",secondary_text=f"At {CurrentTime} on {CurrentDate}"))
            #             if float(data[0]) > 3 and self.RedStatus == 1 :
            #                 arduino.write(b"r")
            #                 self.RedStatus = 0
            #                 CurrentDate = self.date
            #                 CurrentTime = self.time
            #                 self.root.get_screen("MainScreen").ids.history_list.add_widget(TwoLineListItem(text="Red LED Turned Off",secondary_text=f"At {CurrentTime} on {CurrentDate}"))     
            except:
                pass

    def change_login_details_dialog(self):
        if not self.dialog2:
            self.dialog2 = MDDialog(
                type="custom",
                content_cls=CredentialsContent(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color,on_release=self.close_dialog2
                    ),
                    MDFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color,on_release=self.change_login_details
                    ),
                ],
            )
        self.dialog2.open()
   
    def change_login_details(self,obj):
        if self.dialog2.content_cls.ids.old_password.text == self.password:
            if self.dialog2.content_cls.ids.new_password.text == self.dialog2.content_cls.ids.confirm_password.text:
                self.username = self.dialog2.content_cls.ids.new_username.text
                self.password = self.dialog2.content_cls.ids.new_password.text
                toast("Login Credentials Changed")
                self.dialog2.dismiss()
                self.dialog2.content_cls.ids.old_password.text = ""
                self.dialog2.content_cls.ids.new_username.text = ""
                self.dialog2.content_cls.ids.new_password.text = ""
                self.dialog2.content_cls.ids.confirm_password.text = ""
            else:
                self.dialog2.content_cls.ids.confirm_password.text = ""
                toast("Re-enter Confirmatory Password")
        else:
            self.dialog2.content_cls.ids.old_password.text = ""
            toast("Invalid Old Password")


    def close_dialog2(self,obj):
        self.dialog2.dismiss()

    def on_switch_active(self, instance, value):
        if value:
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

    def reset_default(self):
        self.root.get_screen("MainScreen").ids.minDO.text = "4"
        self.pondDict[self.selected_pond][3][0] = "4"
        self.root.get_screen("MainScreen").ids.maxDO.text = "8"
        self.pondDict[self.selected_pond][3][1] = "8"
        self.root.get_screen("MainScreen").ids.minpH.text = "7.5"
        self.pondDict[self.selected_pond][3][4] = "7.5"
        self.root.get_screen("MainScreen").ids.maxpH.text = "8.5"
        self.pondDict[self.selected_pond][3][5] = "8.5"
        self.root.get_screen("MainScreen").ids.minSalinity.text = "0"
        self.pondDict[self.selected_pond][3][6] = "0"
        self.root.get_screen("MainScreen").ids.maxSalinity.text = "0.5"
        self.pondDict[self.selected_pond][3][7] = "0.5"
        
        if self.selected_species == "Nile Tilapia":
            self.root.get_screen("MainScreen").ids.minTemp.text = "12"
            self.root.get_screen("MainScreen").ids.maxTemp.text = "42"
            self.pondDict[self.selected_pond][3][2] = "12"
            self.pondDict[self.selected_pond][3][3] = "42"
        elif self.selected_species == "Catfish":
            self.root.get_screen("MainScreen").ids.minTemp.text = "9"
            self.root.get_screen("MainScreen").ids.maxTemp.text = "37"
            self.pondDict[self.selected_pond][3][2] = "9"
            self.pondDict[self.selected_pond][3][3] = "37"
        elif self.selected_species == "Shrimp":
            self.root.get_screen("MainScreen").ids.minTemp.text = "14"
            self.root.get_screen("MainScreen").ids.maxTemp.text = "40"
            self.pondDict[self.selected_pond][3][2] = "14"
            self.pondDict[self.selected_pond][3][3] = "40"
        elif self.selected_species == "Prawn":
            self.root.get_screen("MainScreen").ids.minTemp.text = "14"
            self.root.get_screen("MainScreen").ids.maxTemp.text = "36"
            self.pondDict[self.selected_pond][3][2] = "14"
            self.pondDict[self.selected_pond][3][3] = "36"

    def use_meteorological_data(self, instance, value):
        if value:
            self.useMeteorologicalData = True
            #threading.Thread(target = self.fetch_meteorological_data).start()
        else:
            self.useMeteorologicalData = False

    def fetch_meteorological_data(self, *args):
        html_text = requests.get("https://weather.com/weather/hourbyhour/l/Accra+Greater+Accra+Ghana?canonicalCityId=6ea38a5575bc43b7f51f1fd1416e23b944035f76b5e7f817354e76191c79a389").text
        soup = BeautifulSoup(html_text,'lxml')
        hours = soup.findAll('h2',class_="DetailsSummary--daypartName--2FBp2")
        temps = soup.findAll('span', class_="DetailsSummary--tempValue--1K4ka")
        precipitationPercentages = soup.findAll('div',class_="DetailsSummary--precip--1ecIJ")
        winds = soup.findAll('span', class_="Wind--windWrapper--3aqXJ undefined")
        precipitationPercentage = precipitationPercentages[0].text
        precipitationPercentage = precipitationPercentage.replace("Rain","")
        wind = winds[0].text
        wind = wind.split(" ")
        wind = wind[0] + " " + wind[1] + wind[2]
        self.root.get_screen("MainScreen").ids.meteorologicalTime.text = hours[0].text
        self.root.get_screen("MainScreen").ids.meteorologicalTemp.text = temps[0].text
        self.root.get_screen("MainScreen").ids.meteorologicalPrecipitation.text = precipitationPercentage
        self.root.get_screen("MainScreen").ids.meteorologicalWind.text = wind
        print(hours[0].text,temps[0].text,precipitationPercentages[0].text,winds[0].text)
        

MainApp().run()