from kivy.config import Config

Config.set('graphics', 'window_state', 'visible')
Config.set('graphics', 'fullscreen', False)

Config.set('graphics', 'width', 1200)
Config.set('graphics', 'height', 700)
Config.set('graphics', 'position', 'auto')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.videoplayer import VideoPlayer

import keyboard
import cv2

from tkinter import filedialog
from tkinter import *

class VideoShotApp(App):
    def build(self):
        return Builder.load_file("ui.kv")

    def on_start(self, *args):
        self.videoplayer = VideoPlayer(source="", allow_fullscreen=False)
        self.root.ids.mainfloat.add_widget(self.videoplayer)
        keyboard.on_press_key("right", self.rightpressed)
        keyboard.on_press_key("left", self.leftpressed)
        keyboard.on_press_key("space", self.spacepressed)

    def rightpressed(self, *args):
        new_value = (((self.videoplayer.position - 0) / (self.videoplayer.duration - 0)) * (1 - 0) + 0) + 0.0019
        self.videoplayer.seek(new_value, precise=True)

    def leftpressed(self, *args):
        new_value = (((self.videoplayer.position - 0) / (self.videoplayer.duration - 0)) * (1 - 0) + 0) - 0.0019
        self.videoplayer.seek(new_value, precise=True)

    def spacepressed(self, *args):
        if self.videoplayer.state == "stop" or self.videoplayer.state == "pause":
            self.videoplayer.state = "play"

        elif self.videoplayer.state == "play":
            self.videoplayer.state = "pause"

    def getFrame(self, ms):
        self.vidcap.set(cv2.CAP_PROP_POS_MSEC, ms)
        hasFrames, image = self.vidcap.read()
        savewindow = Tk()
        savewindow.geometry("0x0")
        filename = filedialog.asksaveasfilename(title='Save Image As',
                                                filetypes=(('JPEG File', '*.jpg'), ('All Files', '*.*')))
        if filename.endswith(".jpg"):
            filename = filename[:-4]
            
        cv2.imwrite(filename + ".jpg", image)  # Save frame as JPG file
        savewindow.destroy()
        return hasFrames

    def screenshot(self, *args):
        ms = self.videoplayer.position * 1000
        self.getFrame(ms)
        
    def loadvideo(self, *args):
        openwindow = Tk()
        openwindow.geometry("0x0")
        openfilename = filedialog.askopenfilename(title="Choose a Video File",
                                                             filetypes=(("MP4 Files", "*.mp4"), ('All Files', '*.*')))
        self.videoplayer.source = openfilename
        self.video = openfilename
        self.vidcap = cv2.VideoCapture(openfilename)
        openwindow.destroy()


VideoShotApp().run()
