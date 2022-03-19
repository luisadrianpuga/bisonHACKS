#
#TEAM 13
#AllergiScan APP
#Luis Puga, Praise Idowu, RainbowMan
#

from kivy.uix.checkbox import CheckBox
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from pyzbar import pyzbar

import cv2

# Resize the window
from kivy.core.window import Window
Window.size = (350, 600)

# Constants
outputtext=''
sample = Label(text='Eggs, Milk, & Nuts',size_hint_y=None,height='48dp',font_size='45dp')
barCode=Label(text=outputtext,size_hint_y=None,height='48dp',font_size='23dp')
found = set()       
togglflag=True
allFlag = False

class MainScreen(BoxLayout):
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.orientation='vertical'   
        
        self.cam=cv2.VideoCapture(0)    
        self.cam.set(3,1280)        
        self.cam.set(4,720)
        self.img=Image()        
        self.lab3=Label(text='AllergiScan ',size_hint_y=None,height='48dp',font_size='45dp')
        self.lab4=Label(text='Scan an item below',size_hint_y=None,height='48dp',font_size='27dp')
        self.add_widget(self.lab3)
        self.add_widget(self.lab4)
        self.add_widget(self.img)
        self.but2=Button(text='Settings',on_press=self.change_settings,size_hint_y=None,height='48dp')
        self.add_widget(self.but2)
     
        Clock.schedule_interval(self.update,1.0/30)    
        
                
    # update frame of OpenCV camera
    def update(self,dt):
        if togglflag:
            ret, frame = self.cam.read()    
            
            if ret:
                buf1=cv2.flip(frame,0)      
                buf=buf1.tostring()
                image_texture=Texture.create(size=(frame.shape[1],frame.shape[0]),colorfmt='bgr')
                image_texture.blit_buffer(buf,colorfmt='bgr',bufferfmt='ubyte')
                self.img.texture=image_texture  
                
                barcodes = pyzbar.decode(frame)  # detect barcode from image
                for barcode in barcodes:
                    (x, y, w, h) = barcode.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    barcodeData = barcode.data.decode("utf-8")
                    barcodeType = barcode.type
                    text = "{} ({})".format(barcodeData, barcodeType)
                    cv2.putText(frame, text, (x, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    if barcodeData not in found: 
                        outputtext=text
                        print('Scanned: ', outputtext)
                        #Hot Tamale
                        accepted_Tamale = {'0070970471230 (EAN13)'}
                        if outputtext in accepted_Tamale:
                            print('Hot Tamales')
                            outputtext='No Matching Allergens'
                            barCode.text=outputtext 
                            print(outputtext)        
                          
                            self.change_screen()
                        
                        #Nerds
                        accepted_Nerds = {'0079200558338 (EAN13)'}
                        if outputtext in accepted_Nerds:
                            outputtext='WARNING: MAY CONTAIN EGGS'
                            barCode.text=outputtext 
                            print(outputtext)        
                            
                            self.change_screen()
                        
                        #Skittles
                        accepted_Skittles = {'0022000011893 (EAN13)'}
                        if outputtext in accepted_Skittles:
                            outputtext='No Matching Allergens'
                            barCode.text=outputtext 
                            print(outputtext)        
                            
                            self.change_screen()
                            
                        #DORITOS
                        accepted_DORITOS = {'0028400090896 (EAN13)'}
                        if outputtext in accepted_DORITOS:
                            outputtext='WARNING: CONTAINS MILK'
                            barCode.text=outputtext 
                            print(outputtext)        
                           
                            self.change_screen()
                        
                            
                            
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    cv2.destroyAllWindows()
                    exit(0)
        
    # change state of toggle button
    def change_state(self,*args):
        global togglflag
        if togglflag:
            self.togbut.text='Play'
            togglflag=False
        else:
            self.togbut.text='Pause'
            togglflag=True
            
            
    def stop_stream(self,*args):
        self.cam.release() 
        
    def change_screen(self,*args):
        main_app.sm.current='second'  
          
    def change_settings(self,*args):
        main_app.sm.current='third'  #settings menu
        
         
class SecondScreen(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.orientation='vertical'
        self.lab1=Label(text='Result: ',size_hint_y=None,height='48dp',font_size='45dp')
        self.lab4=Label(text='Contains: ',size_hint_y=None,height='15dp',font_size='15dp')
        self.but1=Button(text='Scan Another Item',on_press=self.change_screen,size_hint_y=None,height='48dp')
        
        if allFlag == True:
            self.add_widget(self.lab1)
            self.add_widget(barCode)
            self.add_widget(self.lab4)
            self.add_widget(sample)
            allFlag == False
            self.add_widget(self.but1)
        else:   
            self.add_widget(self.lab1)
            self.add_widget(barCode)
            self.add_widget(self.but1)   
        
    def change_screen(self,*args):
        main_app.sm.current='main' #Return the user to the mainscreen
        #reset the constants
        outputtext=''
        barCode=Label(text='',size_hint_y=None,height='48dp',font_size='45dp')

class settingMenu(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.orientation='vertical'
        self.lab9=Label(text='My Settings: ',size_hint_y=None,height='48dp',font_size='45dp')
        self.add_widget(self.lab9)
        self.but5=Button(text='Go Home',on_press=self.change_screen1,size_hint_y=None,height='48dp')
        self.add_widget(self.but5)
          
        
    def change_screen1(self,*args):
        main_app.sm.current='main' #Return the user to the mainscreen
        #reset the constants
        outputtext=''
        barCode=Label(text='',size_hint_y=None,height='48dp',font_size='45dp')


    
        
                   
class TestApp(App):
    def build(self):
        self.sm=ScreenManager()     
        self.mainsc=MainScreen()
        scrn=Screen(name='main')
        scrn.add_widget(self.mainsc)
        self.sm.add_widget(scrn)
        
        self.secondsc=SecondScreen()
        scrn=Screen(name='second')
        scrn.add_widget(self.secondsc)
        self.sm.add_widget(scrn)
        
        self.thirdsc=settingMenu()
        scrn=Screen(name='third')
        scrn.add_widget(self.thirdsc)
        self.sm.add_widget(scrn)
        return self.sm

if __name__ == '__main__':
    main_app=TestApp()
    main_app.run()
    cv2.destroyAllWindows()        
