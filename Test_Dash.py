# from kivy.lang import Builder
# from kivy.metrics import dp
# from kivy.properties import StringProperty

# from kivymd.uix.list import OneLineIconListItem
# from kivymd.app import MDApp
# from kivymd.uix.menu import MDDropdownMenu

# KV = '''
# MDScreen

#     MDDropDownItem:
#         id: drop_item
#         pos_hint: {'center_x': .5, 'center_y': .5}
#         text: 'Item 1'
#         on_release: app.menu.open()

# '''

# class Test(MDApp):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.screen = Builder.load_string(KV)
#         menu_items = [
#             {
#                 "viewclass": "OneLineListItem",
#                 "text": f"Item {i}",
#                 "height": dp(56),
#                 "on_release": lambda x=f"Item {i}": self.set_item(x),
#             } for i in range(1,3)
#         ]
#         self.menu = MDDropdownMenu(
#             caller=self.screen.ids.drop_item,
#             items=menu_items,
#             width_mult=4,
#         )
#         self.menu.bind()

#     def set_item(self, text_item):
#         self.screen.ids.drop_item.set_item(text_item)
#         self.menu.dismiss()

#     def build(self):
#         return self.screen


# Test().run()

# from kivy.lang import Builder

# from kivymd.app import MDApp
# from kivymd.uix.list import OneLineListItem

# KV = '''
# ScrollView:

#     MDList:
#         id: container
# '''


# class Test(MDApp):
#     def build(self):
#         return Builder.load_string(KV)

#     def on_start(self):
#         for i in range(5):
#             self.root.ids.container.add_widget(
#                 OneLineListItem(text=f"Single-line item {i}")
#             )

# Test().run()

from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons


KV = '''
<ListItemWithCheckbox>:

    IconLeftWidget:
        icon: root.icon

    RightCheckbox:

MDScreen:
    MDBoxLayout:

        ScrollView:

            MDList:
                id: scroll
'''


class ListItemWithCheckbox(OneLineAvatarIconListItem):
    '''Custom list item.'''

    icon = StringProperty("android")


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    '''Custom right container.'''


class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        icons = list(md_icons.keys())
        for i in range(30):
            self.root.ids.scroll.add_widget(
                ListItemWithCheckbox(text=f"Item {i}", icon=icons[i])
            )


MainApp().run()