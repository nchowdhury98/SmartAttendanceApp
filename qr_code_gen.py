from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy_garden.qrcode import QRCodeWidget

class MyWidget(Widget):
    parent=Widget()
    x="abc"
    parent.add_widget(QRCodeWidget(data="Kivy Rocks"))
root=Builder.load_string('''


#:import QRCodeWidget kivy_garden.qrcode

BoxLayout:
    orientation: 'vertical'
    QRCodeWidget:
        id: qr
        data: root.x
        ''')
class GeneratorApp(App):
    def build(self):

        return root


if __name__ == "__main__":
    GeneratorApp().run()