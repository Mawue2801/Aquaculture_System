from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window

Window.size = (800,480)

KV = '''
#:import KivyLexer kivy.extras.highlight.KivyLexer
#:import HotReloadViewer kivymd.utils.hot_reload_viewer.HotReloadViewer

BoxLayout:
    HotReloadViewer:
        path: app.path_to_kv_file
        errors: True
        errors_text_colour: 1,1,0,1
        errors_background_colour: app.theme_cls.bg_dark
'''

class MainApp(MDApp):
    path_to_kv_file = "GraphScreen.kv"
    def build(self):
        return Builder.load_string(KV)

MainApp().run()