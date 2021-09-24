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
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem

Window.size = (800,480)

KV = """
#:import toast kivymd.toast.toast
MDScreen:
    BoxLayout:
        orientation: 'vertical'

        MDBottomNavigation:

            MDBottomNavigationItem:
                name: 'screen 1'
                text: "Sensor Values"
                icon: 'monitor-dashboard'

                MDLabel:
                    text: "Pond of Focus:"
                    font_style: "Subtitle1"
                    pos_hint: {"center_x": 0.575, "center_y": 0.9}

                MDDropDownItem:
                    id: pond_selection
                    pos_hint: {'center_x': 0.275, 'center_y': 0.9}
                    text: 'Pond 1'
                    on_release: app.menu.open()

                MDCard:
                    orientation: "vertical"
                    padding: "8dp"
                    size_hint: 0.25 , 0.25
                    pos_hint: {"center_x": 0.2, "center_y": 0.6}

                    MDLabel:
                        text: "Dissolved Oxygen"
                        theme_text_color: "Secondary"
                        text_color: (0,0,1,1)
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDSeparator:
                        height: "1dp"

                    BoxLayout:
                        orientation:"horizontal"

                        MDLabel:
                            text: ""

                        MDLabel:
                            id: do_label
                            text: "00.00"
                            font_style: "H4"
                
                MDCard:
                    orientation: "vertical"
                    padding: "8dp"
                    size_hint: 0.25 , 0.25
                    pos_hint: {"center_x": 0.5, "center_y": 0.6}


                    MDLabel:
                        text: "Temperature"
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDSeparator:
                        height: "1dp"

                    BoxLayout:
                        orientation:"horizontal"

                        MDLabel:
                            text: ""

                        MDLabel:
                            id: temp_label
                            text: "00.00"
                            font_style: "H4"

                MDCard:
                    orientation: "vertical"
                    padding: "8dp"
                    size_hint: 0.25 , 0.25
                    pos_hint: {"center_x": 0.8, "center_y": 0.6}


                    MDLabel:
                        text: "pH"
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDSeparator:
                        height: "1dp"

                    BoxLayout:
                        orientation:"horizontal"

                        MDLabel:
                            text: ""

                        MDLabel:
                            id: pH_label
                            text: "00.00"
                            font_style: "H4"

                MDCard:
                    orientation: "vertical"
                    padding: "8dp"
                    size_hint: 0.25 , 0.25
                    pos_hint: {"center_x": 0.2, "center_y": 0.3}


                    MDLabel:
                        text: "Water Level"
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDSeparator:
                        height: "1dp"

                    BoxLayout:
                        orientation:"horizontal"

                        MDLabel:
                            text: ""

                        MDLabel:
                            id: water_level_label
                            text: "00.00"
                            font_style: "H4"

                MDCard:
                    orientation: "vertical"
                    padding: "8dp"
                    size_hint: 0.25 , 0.25
                    pos_hint: {"center_x": 0.5, "center_y": 0.3}


                    MDLabel:
                        text: "Turbidity"
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDSeparator:
                        height: "1dp"

                    BoxLayout:
                        orientation:"horizontal"

                        MDLabel:
                            text: ""

                        MDLabel:
                            id: turbidity_label
                            text: "00.00"
                            font_style: "H4"

                MDCard:
                    orientation: "vertical"
                    padding: "8dp"
                    size_hint: 0.25 , 0.25
                    pos_hint: {"center_x": 0.8, "center_y": 0.3}


                    MDLabel:
                        text: "Electrical Conductivity"
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDSeparator:
                        height: "1dp"

                    BoxLayout:
                        orientation:"horizontal"

                        MDLabel:
                            text: ""

                        MDLabel:
                            id: conductivity_label
                            text: "00.00"
                            font_style: "H4"

            MDBottomNavigationItem:
                name: 'screen 2'
                text: "Feeding"
                icon: 'grain'

                MDCard:
                    orientation: "vertical"
                    padding: "5dp"
                    size_hint: 0.95 , 0.2
                    pos_hint: {"center_x": 0.5, "center_y": 0.875}

                    BoxLayout:
                        orientation:"horizontal"
                        padding:"10dp"

                        MDLabel:
                            id: week_label
                            text: "Week 1"
                            font_style: "H4"
                
                        MDLabel:
                            text: ""
                            font_style: "H1"
                        
                        MDLabel:
                            text: ""
                            font_style: "H1"

                        MDLabel:
                            text: ""
                            font_style: "H1"
                        
                        MDLabel:
                            text: ""
                            font_style: "H1"

                        BoxLayout:
                            orientation:"vertical"
                        
                            MDLabel:
                                id: time_label
                                text: ""
                                font_style: "H5"

                            MDLabel:
                                id: date_label
                                text: ""
                                font_style: "Subtitle1"
                                theme_text_color: "Secondary"

                FloatLayout:

                    MDRectangleFlatButton:
                        text: "Add Feeding Time"
                        pos_hint: {'center_x': .5, 'center_y': .4}
                        on_release: app.show_time_picker()

                    MDLabel:
                        id: feeding_time_label
                        text: "Feeding"
                        halign: 'center'


            MDBottomNavigationItem:
                name: 'screen 3'
                text: "History"
                icon: 'history'

                # MDLabel:
                #     text: "History"
                #     halign: 'center'

                ScrollView:

                    MDList:
                        id: container


            MDBottomNavigationItem:
                name: 'screen 4'
                text: "Settings"
                icon: 'cog'

                MDLabel:
                    text: "Settings"
                    halign: 'center'
"""

class Example(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        self.screen = Builder.load_string(KV)
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"Pond {i}",
                "height": dp(56),
                "on_release": lambda x=f"Pond {i}": self.set_item(x),
            } for i in range(1,3)
        ]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.pond_selection,
            items=menu_items,
            width_mult=4,
        )
        self.menu.bind()

    def set_item(self, text_item):
        self.screen.ids.pond_selection.set_item(text_item)
        self.menu.dismiss()

    def build(self):
        #self.theme_cls.theme_style = "Dark"
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
        # Clock.schedule_interval(self.update, 1)
        Clock.schedule_interval(self.update_time, 1)
        return self.screen

    def get_time(self,instance,time):
        self.root.ids.feeding_time_label.text = str(time)

    def on_cancel(self,instance,time):
        self.root.ids.feeding_time_label.text = "Cancelled"
    
    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(on_cancel=self.on_cancel,time=self.get_time)
        time_dialog.open()

    def update_time(self, *args):
        now = datetime.now()
        dt_string = now.strftime("%b-%d-%Y %H:%M:%S").split(" ")
        self.root.ids.date_label.text = dt_string[0]
        self.root.ids.time_label.text = dt_string[1]
        #self.root.ids.container.add_widget(OneLineListItem(text=f"Time change {dt_string[1]}"))
    
    # def update(self, *args):
    #     arduino = self.arduino
    #     data = str(arduino.read(arduino.inWaiting()).decode()).split(",")
    #     self.root.ids.do_label.text = data[0]
    #     print(data[0])

Example().run()

    
