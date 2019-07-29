#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd4in2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

try:
    epd = epd4in2.EPD()
    epd.init()
    #epd.Clear(0xFF)
    
    # Drawing on the Horizontal image
    Himage = Image.new('1', (epd4in2.EPD_WIDTH, epd4in2.EPD_HEIGHT), 255)  # 255: clear the frame
     
    # Horizontal
    print("Drawing")
    draw = ImageDraw.Draw(Himage)
    #font24 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 24)
    font24 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf', 32)
    draw.rectangle((0, 0, epd4in2.EPD_WIDTH-1, epd4in2.EPD_HEIGHT-1), outline = 0)
    draw.text((10, 10), 'F3F CHRONO TEST', font = font24, fill = 0)
    textsize = draw.textsize ('F3F CHRONO', font = font24)
    print (textsize)
    draw.text((10, textsize[1]+10), '4.2inch e-Paper', font = font24, fill = 0)
    textsize1 = draw.textsize ('4.2inch e-Paper', font = font24)
    draw.text((10, textsize[1]+textsize1[1]+10), 'Last Time : 10.021s', font = font24, fill = 0)
    epd.display(epd.getbuffer(Himage))
    
       
    epd.sleep()
        
except:
    print('traceback.format_exc():\n%s',traceback.format_exc())
    exit()

