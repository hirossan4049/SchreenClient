import requests
import io
import cv2
import numpy
from PIL import Image

from kivy.core.image import Image as CoreImage
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.graphics.texture import Texture

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
        super(MainApp,self).__init__(**kwargs)
        self.bytes = b''
        self.texture = Texture.create(size=Window.size)
        url = "http://192.168.1.12:8050/video_feed"
        self.stream = requests.get(url, stream=True)
        self.fps_check_num = 0
        Clock.schedule_interval(self.crap, 1/60)
        # Clock.schedule_once(self.check_fps)


    def build(self):
        self.root = Factory.MainWindow()
        self.canvas = self.root.canvas


        # self.root.add_widget(self.texture)
        # widget = Widget(id="widget")
        # data = io.BytesIO(open("sample.jpg", "rb").read())
        # im = CoreImage.load(data, ext='jpg')
        # texture = im.texture
        # with widget.canvas:
        #     Rectangle(texture=texture, size=(300, 200))


    # TODO:謎.
    # TODO:メモリもぐもぐ
    def crap(self,*args):
        while True:
            self.bytes += self.stream.raw.read(20480)
            a = self.bytes.find(b'\xff\xd8')
            b = self.bytes.find(b'\xff\xd9')
            if a!=-1 and b!=-1:
                self.fps_check_num += 1
                jpg = self.bytes[a:b+2]
                self.bytes = self.bytes[b+2:]
                self.draw_jpg(jpg)
                # print(len(self.bytes))
                break


    def draw_jpg(self,imbytes):
        imiob = io.BytesIO(imbytes)
        img_pil = Image.open(imiob)

        im = CoreImage.load(io.BytesIO(imbytes), ext='jpg')
        # texture = im.texture
        # self.texture.blit_buffer(img_pil.tobytes())

        # with self.root.canvas as a: # 描画
        # TODO: よくわからん。
        self.canvas.clear()
        self.canvas.add(Rectangle(texture = im.texture , size=Window.size))
        # with self.root.ids.widget.canvas:
        # with self.root.canvas:
        #     Rectangle(texture=texture, size=Window.size)

    def check_fps(self,*args):
        self.fps_check_num = 0
        time.sleep(10)
        print(self.fps_check_num)


if __name__ == '__main__':
    MainApp().run()
