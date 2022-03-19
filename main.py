from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from pyzbar import pyzbar
import cv2
import webbrowser

#Constants
outputtext =''
leb=Label(text=outputtext, size_hint_y=None, height='48dp', font_size='45dp')
found = set() #this will not allow duplicate barcode scans to be stored
togFlag =True
weblink=''
class mainApp(BoxLayout):
    def __init__(self, **kwargs):
        self.orientation = 'vertical'

        self.cam=cv2.VideoCapture(0)
        self.cam.set(3,1200)
        self.cam.set(4, 720)
        self.img=Image()

        self.togbut=ToggleButton(text='Pause', group='camstart',state='down',size_hint_y=None, height='48dp', on_press=self.change_state)
        self.but=Button(text='Stop', size_hint_y=None, height='48dp',on_press=self.stop_stream)
        self.add_widget(self.img)
        self.add_widget(self.togbut)
        self.add_widget(self.but)
        Clock.schedule_interval(self.update,1.0/30)


    def update(self,dt):
        if togFlag:
            ret, frame = self.cam.read()

            if ret:
                buf1=cv2.flip(frame,0)
                buf=buf1.tostring()
                image_texture=Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                image_texture.blit_buffer(buf, colorfmt='bgr',bufferfmt='ubyte')
                self.img.texture=image_texture

                barcodes = pyzbar.decode(frame)
                for barcode in barcodes:
                    (x,y,w,h) = barcode.rect
                    cv2.rectangle(frame,(x,y),(x+w, y+h),(0,0,255),2)
                    barcodeData = barcode.data.decode("utf-8")
                    barcodeType = barcode.type
                    weblink=barcodeData
                    text ="{} ({})".format(barcodeData, barcodeType)
                    cv2.putText(frame, text, (x,y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),2)
                    if barcodeData not in found:
                        outputtext=text
                        leb.text=outputtext
                        found.add(barcodeData)
                        self.change_screen()

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    cv2.destroyAllWindows()
                    exit(0)

    def change_state(self, *args):
        global togFlag
        if togFlag:
            self.togbut.text='Play'
            togFlag=False
        else:
            self.togbut.text = 'Play'
            togFlag = True

    def stop_stream(self, *args):
        self.cam.release()

    def change_screen(self, *args):
        main_app.sm.current='second'

class SecondScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        self.orientation='vertical'
        self.lab1=Label(text='Output: ', size_hint_y=None, height='48dp', font_size="45dp")
        self.but1=Button(text='Open in Web Browser', on_press=self.open_browser, size_hint=None, height='48dp')
        self.add_widget(self.lab1)
        self.add_widget(leb)
        self.add_widget(self.but1)

    def open_browser(self, **kwargs):
        webbrowser.open(weblink)

class TestApp(App):
    def build(self):
        self.sm=ScreenManager()
        self.mainsc=mainApp()
        scrn=Screen(name='main')
        scrn.add_widget(self.mainsc)
        self.sm.add_widget(scrn)

        self.secondsc=SecondScreen()
        scrn=Screen(name='second')
        scrn.add_widget(self.secondsc)
        self.sm.add_widget(scrn)

        return self.sm

if __name__ == '__main__':
    main_app=TestApp()
    main_app.run()
    cv2.destroyAllWindows()