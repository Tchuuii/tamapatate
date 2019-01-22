import RPi.GPIO as GPIO

import time,random

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

A_pin = 10
B_pin = 12
C_pin = 16
GPIO.setmode(GPIO.BCM)

GPIO.setup(A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(C_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

mlevel = 0 #main level

def button1_callback(channel):
    global mlevel
    print("Button 1 was pushed!")
    if mlevel<=10:
        mlevel+=1
    else:
        mlevel=0

def button2_callback(channel):
    global mlevel
    print("Button 2 was pushed!")
    if mlevel==1:
        print("menu1")
    elif mlevel==2:
        print("menu2")
    elif mlevel==3:
        print("menu3")

def button3_callback(channel):
    global mlevel
    print("Button 3 was pushed!")
    mlevel=0


class Tamagotchi:
    def __init__(self,name):
        self.name=name
        self.miam=4
        self.joy=4
        self.poo=2
        self.weight=2

    def manger(self):
        self.miam+=1
        self.weight+=1

    def clean(self):
        self.poo=2

    def play(self):
        self.joy+=2
        self.weight-=3

    def snack(self):
        self.joy+=2
        self.weight+=5


if __name__ == '__main__':
    # Initialize library.
    disp.begin()

    # Clear display.
    disp.clear()
    disp.display()
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    font = ImageFont.load_default()
    tamapatate = Tamagotchi("patate")

    #------------BUTTONS SETTING ---------------

    GPIO.add_event_detect(A_pin,GPIO.RISING,callback=button1_callback) # Setup event on pin 10 rising edge
    GPIO.add_event_detect(B_pin,GPIO.RISING,callback=button2_callback) # Setup event on pin 12 rising edge
    GPIO.add_event_detect(C_pin,GPIO.RISING,callback=button3_callback) # Setup event on pin 16 rising edge


    alert = False
    print('Press Ctrl+C to exit')
    draw.text((2, 2),    'Hello',  font=font, fill=255)
    draw.text((2, 22), 'tamapatate', font=font, fill=255)
    # Display image.
    disp.image(image)
    disp.display()
    try:
        while(True):

            statMiam=random.randint(0,100)
            statJoy=random.randint(0,100)
            statPoo=random.randint(0,100)

            if(statMiam>=98) and (tamapatate.miam>0):
                tamapatate.miam-=1
            if(statJoy>=98) and (tamapatate.joy>0):
                tamapatate.joy-=1
            if(statPoo>=97) and (tamapatate.poo>0):
                tamapatate.poo-=1
                print('pop')
                draw.text((2, 42), 'popo', font=font, fill=255)
                disp.image(image)
                disp.display()

            if((tamapatate.miam==0) or (tamapatate.joy==0) or (tamapatate.poo<2)) and alert==False:
                alert=True
                print('ALERT')

            time.sleep(0.2)
    except KeyboardInterrupt:
        GPIO.cleanup()
        time.sleep(1)
        raise
