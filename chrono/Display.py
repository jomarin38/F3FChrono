#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd4in2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

class Display ():
    def __init__(self, chronoID):
        try:
            self.epd = epd4in2.EPD()
            self.epd.init()
            #self.epd.Clear(0xFF)
            
              
        except:
            print('traceback.format_exc():\n%s',traceback.format_exc())
            exit()
            
            
    def display ():
        try :
            # Drawing on the Horizontal image
            self.Image = Image.new('1', (epd4in2.EPD_WIDTH, epd4in2.EPD_HEIGHT), 255)  # 255: clear the frame
             
            self.draw = ImageDraw.Draw(self.Image)
            self.font24 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf', 32)
            self.draw.rectangle((0, 0, epd4in2.EPD_WIDTH-1, epd4in2.EPD_HEIGHT-1), outline = 0)
            self.draw.text((10, 10), 'F3F CHRONO TEST', font = self.font24, fill = 0)
            textsize = self.draw.textsize ('F3F CHRONO', font = self.font24)
            draw.text((10, textsize[1]+10), '4.2inch e-Paper', font = font24, fill = 0)
            textsize1 = draw.textsize ('4.2inch e-Paper', font = font24)
            draw.text((10, textsize[1]+textsize1[1]+10), 'Last Time : 10.021s', font = font24, fill = 0)
            epd.display(epd.getbuffer(Himage))
            
               
            epd.sleep()
              
            
        except:
            print('traceback.format_exc():\n%s',traceback.format_exc())
            exit()
            

if __name__ == '__main__':
    
