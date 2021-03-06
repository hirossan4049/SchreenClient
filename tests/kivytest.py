import requests
import io

from kivy.core.image import Image as CoreImage
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.core.window import Window
import time
Builder.load_file("teskv.kv")


class MainWidget(Widget):
    def __init__(self,**kwargs):
        super(MainWidget,self).__init__(**kwargs)

class MainWindow(Widget):
    def __init__(self,**kwargs):
        super(MainWindow, self).__init__(**kwargs)



class MainApp(App):
    def __init__(self,**kwargs):
        self.root = super(MainApp,self).__init__(**kwargs)
        self.bytes = b''

        url = "http://192.168.1.12:8050/video_feed"
        self.stream = requests.get(url, stream=True)
        Clock.schedule_interval(self.crap, 1/30)


    def build(self):
        self.root = Factory.MainWindow()
        widget = Widget(id="widget")
        data = io.BytesIO(open("sample.jpg", "rb").read())
        im = CoreImage.load(data, ext='jpg')
        texture = im.texture
        with widget.canvas:
            Rectangle(texture=texture, size=(300, 200))
        # self.root.add_widget(widget)
        # return Factory.MainWindow()

    # TODO:謎.
    # TODO:メモリもぐもぐ
    def crap(self,*args):
        while True:
            self.bytes += self.stream.raw.read(2048)
            a = self.bytes.find(b'\xff\xd8')
            b = self.bytes.find(b'\xff\xd9')
            if a!=-1 and b!=-1:
                jpg = self.bytes[a:b+2]
                self.bytes = self.bytes[b+2:]
                self.draw_jpg(jpg)
                print(len(self.bytes))
                break


    def draw_jpg(self,imbytes):
        im = CoreImage.load(io.BytesIO(imbytes), ext='jpg')
        texture = im.texture
        # with self.root.ids.widget.canvas:
        with self.root.canvas:
            Rectangle(texture=texture, size=Window.size)



if __name__ == '__main__':
    MainApp().run()
