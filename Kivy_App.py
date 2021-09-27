from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.picker import MDTimePicker
from kivymd.uix.menu import MDDropdownMenu
from datetime import datetime
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

Window.size = (800,480)

class ListItemWithCheckbox(OneLineAvatarIconListItem):
    icon = StringProperty("delete")

class Content(BoxLayout):
    pass

class Example(MDApp):
    dialog = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("MainScreen.kv"))
        screen_manager.add_widget(Builder.load_file("LoginScreen.kv"))
        self.selected_pond = "1"
        self.username = "smart aquapak"
        self.password = "fish1234"
        self.RedStatus = 0
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"Pond {i}",
                "height": dp(56),
                "on_release": lambda x=f"Pond {i}": self.set_item(x),
            } for i in range(1,3)
        ]
        self.menu = MDDropdownMenu(
            caller=screen_manager.get_screen("MainScreen").ids.pond_selection,
            items=menu_items,
            width_mult=4,
        )
        self.menu.bind()
        self.feedingList = []


    def set_item(self, text_item):
        screen_manager.get_screen("MainScreen").ids.pond_selection.set_item(text_item)
        self.selected_pond = text_item.split(" ")[1]
        self.menu.dismiss()

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

    def log_in(self):
        if self.root.get_screen("LoginScreen").ids.user.text == self.username and self.root.get_screen("LoginScreen").ids.password.text == self.password:
           name = self.root.get_screen("LoginScreen").ids.user.text
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
    
    def add_to_list(self):
        time_dict = {"00":"twelve","01":"one","02":"two","03":"three","04":"four","05":"five","06":"six",
                    "07":"seven","08":"eight","09":"nine","10":"ten","11":"eleven","12":"twelve","13":"one",
                    "14":"two","15":"three","16":"four","17":"five","18":"six","19":"seven","20":"eight",
                    "21":"nine","22":"ten","23":"eleven"}
        time = self.root.get_screen("MainScreen").ids.feeding_time_label.text
        self.root.get_screen("MainScreen").ids.feeding_time_list.add_widget(ListItemWithCheckbox(text=time,icon=f"clock-time-{time_dict[time[0:2]]}-outline"))
        self.feedingList.append(time)

    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()

    def update_time(self, *args):
        now = datetime.now()
        dt_string = now.strftime("%b-%d-%Y %H:%M:%S").split(" ")
        self.date = dt_string[0]
        self.time = dt_string[1]
        self.root.get_screen("MainScreen").ids.date_label.text = dt_string[0]
        self.root.get_screen("MainScreen").ids.time_label.text = dt_string[1]
    
    def remove_widget(self,widget):
        self.root.get_screen("MainScreen").ids.feeding_time_list.remove_widget(widget)
        self.feedingList.remove(widget.text)
        print(self.feedingList)
        
    
    def update(self, *args):
        arduino = self.arduino
        data = str(arduino.readline(arduino.inWaiting()).decode()).split(";")
        try:
            data = data[int(self.selected_pond)-1].split(",")
            self.root.get_screen("MainScreen").ids.do_label.text = data[0]
            self.root.get_screen("MainScreen").ids.temp_label.text = data[1]
            self.root.get_screen("MainScreen").ids.pH_label.text = data[2]
            self.root.get_screen("MainScreen").ids.water_level_label.text = data[3]
            self.root.get_screen("MainScreen").ids.turbidity_label.text = data[4]
            salinityLevel = (float(data[5].replace("\r\n",""))**1.0878)*466.5
            self.root.get_screen("MainScreen").ids.conductivity_label.text = str(salinityLevel)
            if len(data) == 6:
                if float(data[0]) < 4 and self.RedStatus == 0:
                    arduino.write(b"R")
                    self.RedStatus = 1
                    CurrentDate = self.date
                    CurrentTime = self.time
                    self.root.get_screen("MainScreen").ids.history_list.add_widget(TwoLineListItem(text="Red LED Turned On",secondary_text=f"At {CurrentTime} on {CurrentDate}"))
                if float(data[0]) > 3 and self.RedStatus == 1 :
                    arduino.write(b"r")
                    self.RedStatus = 0
                    CurrentDate = self.date
                    CurrentTime = self.time
                    self.root.get_screen("MainScreen").ids.history_list.add_widget(TwoLineListItem(text="Red LED Turned Off",secondary_text=f"At {CurrentTime} on {CurrentDate}"))
                    
        except:
            pass

    def change_login_details_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color,on_release=self.close_dialog
                    ),
                    MDFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color,on_release=self.change_login_details
                    ),
                ],
            )
        self.dialog.open()
    
    def close_dialog(self,obj):
        self.dialog.dismiss()
   
    def change_login_details(self,obj):
        if self.dialog.content_cls.ids.old_password.text == self.password:
            if self.dialog.content_cls.ids.new_password.text == self.dialog.content_cls.ids.confirm_password.text:
                self.username = self.dialog.content_cls.ids.new_username.text
                self.password = self.dialog.content_cls.ids.new_password.text
                toast("Login Credentials Changed")
                self.dialog.dismiss()
                self.dialog.content_cls.ids.old_password.text = ""
                self.dialog.content_cls.ids.new_username.text = ""
                self.dialog.content_cls.ids.new_password.text = ""
                self.dialog.content_cls.ids.confirm_password.text = ""
            else:
                self.dialog.content_cls.ids.confirm_password.text = ""
                toast("Re-enter Confirmatory Password")
        else:
            self.dialog.content_cls.ids.old_password.text = ""
            toast("Invalid Old Password")

    def on_switch_active(self, instance, value):
        if value:
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

Example().run()