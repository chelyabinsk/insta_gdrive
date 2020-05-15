# -*- coding: utf-8 -*-
"""
Created on Fri May 17 19:19:16 2019

@author: c1536127
"""

import textwrap
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter
from PIL import ImageEnhance
import colorsys
import math
from random import randint
from random import uniform
import urllib
import pilgram
import os
import unicodedata
from image_utils import ImageText

class ImageArtist():

    def __init__(self):
        self.path = "/home/seva/Instagram_Etymology2/"
        
    def rgb2hsv(self,rgb):
       return colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])

    def hsv2rgb(self,h,s,v):
        # https://stackoverflow.com/questions/24852345/hsv-to-rgb-color-conversion
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

    def create_image(self,count):
        h = (count*10.0) % 360
        s = 28.0
        v = 90.0

        color = self.hsv2rgb(float(h)/360.0, float(s)/100,float(v)/100)

        color = (int(color[0]),int(color[1]),int(color[2]))
        print("colors: {}, h: {}, s: {}, v: {}, hf: {}".format(color,h,s,v,float(h)))
        img = Image.new("RGB", (1080,1350), color=color)
        draw = ImageDraw.Draw(img)

        # Number of circles to draw
        n_circles = 1000

        for i in range(n_circles):
            h_tmp = randint(h - 40, h + 40)
            s_tmp = randint(10,40)
            alpha = randint(50,90)
            col_tmp = self.hsv2rgb(float(h_tmp)/360.0, float(s_tmp)/100,float(99)/100)
            #print("circle {}, col_tmp : {}, h_tmp : {}, s_tmp : {}".format(i,col_tmp,h_tmp,s_tmp))
            c_col_fill = (int(col_tmp[0]), int(col_tmp[1]), int(col_tmp[2]))

            x_l = randint(-100,1500)
            x_r = randint(x_l+100,x_l+200)

            y_t = randint(-100,1500)
            y_b = randint(y_t+100,y_t+200)

            draw.ellipse((x_l,y_t,x_r,y_b), fill = c_col_fill)
            #print(x_l,y_b,x_r,y_t)
            #draw.point((100, 100), 'red')

        img.save(self.path + "misc/instagram3.jpg")
        #img.save("images/instagram3.jpg")

    #def outputImage(self,word,meaning,definition,imageName,count):
    def outputImage(self,data,imageName,count):
        new = False
        if(len(data) == 3):
            word, meaning, definition = data
        else:
            new = True
            word, meaning, definition, sound, wtype, usage = data
        self.create_image(count)
        w,h = (1080, 1350)
        down_shift = 80  # Number of pixel to shift down
        # Open the starting image
        img = Image.open(self.path + "misc/instagram3.jpg")
        #img = Image.open("images/instagram3.jpg")
        draw = ImageDraw.Draw(img)

        # Initialise the Title word Font-and-Size
        titleFont = ImageFont.truetype(self.path + "fonts/Comfortaa-Regular.ttf", 100)
        titleText = word
        titleW, titleH = draw.textsize(titleText, font=titleFont)
        leftBump = (w - titleW)/2
        # Draw the text in white
        draw.text((leftBump, 40 + down_shift), titleText, (255, 255, 255), font=titleFont)
        # Draw the off-set text in black
        draw.text((leftBump+1, 38 + down_shift), titleText, (0, 0, 0), font=titleFont)
        # Draw lines to the left and right of the text
        # Left line
        draw.line((0, 2 + 40 + down_shift + (titleH/2)) + (leftBump - 20, 2 + 40 + down_shift + (titleH/2) ), fill=0,width=5)
        # Right line
        draw.line((leftBump + titleW + 20, 2 + 40 + down_shift + (titleH/2)) + (w, 2 + 40 + down_shift + (titleH/2) ), fill=0,width=5)

        if(new):
            # Add pronounciation and word type
            #Walkway UltraCondensed.ttf
            #TIMESS__.ttf
            soundsFont = ImageFont.truetype(self.path + "fonts/CharisSILI.ttf",70)
            #soundsFont = ImageFont.truetype("fonts/TIMESS__.ttf",50)
            soundsText = sound + " - " + wtype
            soundsW, soundsH = draw.textsize(soundsText, font=soundsFont)
            draw.text(((w - soundsW)/2,100 + soundsH/4 + titleH),soundsText, (80,80,100),font=soundsFont)

        # Add meaning
        defFont = ImageFont.truetype(self.path + "fonts/Roboto-Regular.ttf",48)
        defText = meaning
        newText = textwrap.wrap(defText,44)
        meaningTextText = ""
        for i in newText:
            meaningTextText = meaningTextText + i + "\n"
        defText = meaningTextText
        del meaningTextText
        defW, defH = draw.textsize(defText, font=defFont)
        defX = 0 + 20
        defY = 100 + defH/4 + titleH + 170
        draw.text((defX, defY),defText, (0,0,0),font=defFont)

        # Draw box around meaning text
        # Draw bottom line
        meaningLineX = 0
        meaningLineY = defY + defH - 20
        draw.line((meaningLineX,meaningLineY) + (w, defY + defH - 20), fill=0,width = 4)
        # Draw line on top
        line1Font = ImageFont.truetype(self.path + "fonts/Roboto-Italic.ttf",30)
        line1Text = "meaning"
        line1W, line1H = draw.textsize(line1Text, font=line1Font)
        draw.text((defX + 20, defY - 30),line1Text, (0,0,0),font=line1Font)
        draw.line((0,defY - 30 + line1H/2) + (defX + 20, defY - 30 + line1H/2), fill=0,width = 4)
        draw.line((defX + 20 + line1W,defY - 30 + line1H/2) + (w, defY - 30 + line1H/2), fill=0,width = 4)

#        senY = 0
#        senLineY = 0
        senW = 0
        senH = 0
        if(new):
            # Add sentence example
            senFont = ImageFont.truetype(self.path + "fonts/Roboto-Italic.ttf",54)
            senText = usage
            senText = textwrap.wrap(senText,43)
            meaningTextText = ""
            for i in senText:
                meaningTextText = meaningTextText + i + "\n"
            senText = meaningTextText
            del meaningTextText
            senW, senH = draw.textsize(senText, font=senFont)

        # Add etymology
        etyFont = ImageFont.truetype(self.path + "fonts/Roboto-Regular.ttf",48)
        etyText = definition
        newText = textwrap.wrap(etyText,46)
        meaningTextText = ""
        for i in newText:
            meaningTextText = meaningTextText + i + "\n"
        etyText = meaningTextText
        del meaningTextText
        etyW, etyH = draw.textsize(etyText, font=defFont)

        Y = 1350 - meaningLineY  # Total height of the dynamic space
        Y1 = senH  # Height of the Example sentence box
        Y2 = etyH  # Height of the Etymology box
        Ye = 1/3*(Y - Y1 - Y2)  # Height of the spaces between

        # Draw box around meaning text
        # Draw bottom line
        senX = 0 + 20
        sen_t_X = (1080 - senW)/2
        senY = meaningLineY + Ye
        senLineX = 0
        senLineY = senY + senH - 30
        draw.line((senLineX,senLineY) + (w, senLineY), fill=0,width = 4)
        # Add Text
        draw.text((sen_t_X,senY),senText,(0,0,0),font=senFont)
        # Draw line on top
        line2Font = ImageFont.truetype(self.path + "fonts/Roboto-Italic.ttf",30)
        line2Text = "example sentence"
        line2W, line2H = draw.textsize(line2Text, font=line2Font)
        draw.text((senX + 20, senY - 30),line2Text, (0,0,0),font=line2Font)
        draw.line((0,senY - 30 + line2H/2) + (senX + 20, senY - 30 + line2H/2), fill=0,width = 4)
        draw.line((senX + 20 + line2W,senY - 30 + line2H/2) + (w, senY - 30 + line2H/2), fill=0,width = 4)

        #draw.text(((w - defW)/2,100 + defH/4 + titleH + 100),defText, (0,0,0),font=defFont)
        if(new):
            etyX = 0 + 20
            etyY = meaningLineY + Ye + senH + Ye

        else:
            etyX = 0 + 20
            etyY = h/2 + 100

        draw.text((etyX, etyY),etyText, (0,0,0),font=etyFont)
         # Draw box around meaning text
        # Draw bottom line
        etyLineX = 0
        etyLineY = etyY + etyH - 30
        draw.line((etyLineX,etyLineY) + (w, etyLineY), fill=0,width = 4)
        # Draw line on top
        line3Font = ImageFont.truetype(self.path + "fonts/Roboto-Italic.ttf",30)
        line3Text = "etymology"
        line3W, line3H = draw.textsize(line3Text, font=line3Font)
        draw.text((etyX + 20, etyY - 30),line3Text, (0,0,0),font=line3Font)
        draw.line((0,etyY - 30 + line3H/2) + (etyX + 20, etyY - 30 + line3H/2), fill=0,width = 4)
        draw.line((etyX + 20 + line3W,etyY - 30 + line3H/2) + (w, etyY - 30 + line3H/2), fill=0,width = 4)

        # Add my watermark lol
        watermarkFont = ImageFont.truetype(self.path + "fonts/Roboto-Italic.ttf",35)
        draw.text((400, 160 + 35 + down_shift + (titleH/2)),"@daily.etymology", (255,120,255),font=watermarkFont)
        draw.text((400, 160 + 35 + down_shift + (titleH/2)),"@daily.etymology", (0,0,0),font=watermarkFont)
        draw.text((400, 2 + 160 + 35 + down_shift + (titleH/2)),"@daily.etymology", (200,200,255),font=watermarkFont)
        img.save(imageName)
    
    def get_soup(self,url,header):
        from bs4 import BeautifulSoup
        return BeautifulSoup(urllib.request.urlopen(
            urllib.request.Request(url,headers=header)),
            'html.parser')
    
    def download_image(self,query,debug=False):
        import json
        import requests
        import shutil
        
        #query = "nomenclature"
        query = str(unicodedata.normalize('NFKD', query).encode('ascii','ignore'))
        query= query.split()
        query='+'.join(query)
        #url="http://www.bing.com/images/search?q=" + query + "&FORM=HDRSC2"
        url="http://www.bing.com/images/search?q=" + query + "&qft=+filterui:imagesize-large&FORM=HDRSC2"
        
        #add the directory for your image here
        DIR="Pictures"
        header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        soup = self.get_soup(url,header)
        
        ActualImages=[]# contains the link for Large original images, type of  image
        for a in soup.find_all("a",{"class":"iusc"}):
            #print a
            #mad = json.loads(a["mad"])
            #turl = mad["turl"]
            m = json.loads(a["m"])
            murl = m["murl"]
            #print(murl)
        
            #image = Image.open(urllib.request.urlopen(murl))
            try:
                image_name = urllib.parse.urlsplit(murl).path.split("/")[-1]
                r = requests.get(murl,stream=True)
            except:
                continue
            try:
                image = Image.open(r.raw)
                width,height = image.size
                if(width > 1000 and height > 1000 and round(width/float(height),1) >= 0.9 ):
                    #print(width,height,round(width/float(height),1))
                    break
            except:
                pass
        
        r = requests.get(murl)
        if(not debug):
            image_name = "bgimg.jpg"
        with open("Images/{}".format(image_name),"wb") as outfile:
            outfile.write(r.content)
    
    def draw_img1(self,dat,nn=""):
        # Open bgimg.jpg image and create two images of different sizes
        image1 = Image.open("Images/bgimg.jpg").convert("RGBA")
        image = Image.new("RGB",image1.size,"YELLOW")
        image.paste(image1,(0,0),image1)
        image = image.convert("RGB")
        try:
            #image = Image.new("RGBA",image1.size,"WHITE")
            #image = image1.convert("RGBA")
            #image.paste(image1,(0,0),image1)
            #image = image.convert("RGB")
            pass
        except:
            #image = image1
            pass
        image = image.resize((1080,1080),Image.ANTIALIAS)
        
        # Apply filter to the image
        
        # Use one of the filters at random
        self.get_filter()(image).save('Images/pic1.jpg')
        image = Image.open("Images/pic1.jpg")
        image = image.resize((1080,1080),Image.ANTIALIAS)
        image = image.filter(ImageFilter.BLUR)
        image = image.filter(ImageFilter.MinFilter(5))
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(0.5)        
        image = ImageEnhance.Color(image)
        image = image.enhance(1.5)        
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.1)        
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.5)        
        image = image.filter(ImageFilter.BLUR)
        
        # Add text
        draw = ImageDraw.Draw(image)
        
        text = dat["word"]
        fontsize = 1
        
        img_fraction = 0.7
        
        # Pick some title font at random
        font_path = self.pick_font("Title")
        #print(font_path)
        font = ImageFont.truetype(font_path,fontsize)
        while font.getsize(text)[0] < img_fraction*image.size[0]:
            fontsize += 1
            font = ImageFont.truetype(font_path,fontsize)
            font2 = ImageFont.truetype(font_path,fontsize+1)
        # Find average colour
        col = image.resize((1,1)).getpixel((0,0))
        col = self.compliment(col)
        # Center the main word
        draw.text(((image.size[0]-font.getsize(text)[0])/2,
                   (image.size[1]-font.getsize(text)[1])/2),
                  text,(0,0,0),font=font2)
        draw.text(((image.size[0]-font.getsize(text)[0])/2,
                   (image.size[1]-font.getsize(text)[1])/2),
                  text,col,font=font)
        
        topsize = font.getsize(text)
        # Find negative colour for the sound
        text = dat["phonetics"]
        fontsize = 1        
        img_fraction = 0.6
        # Pick some word_type font at random
        font = ImageFont.truetype("fonts/CharisSILI.ttf",fontsize)
        while font.getsize(text)[0] < img_fraction*image.size[0]:
            fontsize += 1
            font = ImageFont.truetype("fonts/CharisSILI.ttf",fontsize)
            font2 = ImageFont.truetype("fonts/CharisSILI.ttf",fontsize+1)
        # Find average colour
        col = image.resize((1,1)).getpixel((0,0))
        col = self.compliment(col)
        col_hsv = self.rgb2hsv(col)
        hue = ((col_hsv[0] + uniform(-45,45)) % 360)/360
        val = (col_hsv[2]+0*uniform(-1,1) % 255)/255
        col = self.hsv2rgb(hue, col_hsv[1], val)
        # Center the main word
        draw.text(((image.size[0]-font.getsize(text)[0])/2,
                   1-font2.getsize(text)[1]/4),text,(0,0,0),font=font2)
        draw.text(((image.size[0]-font.getsize(text)[0])/2,
                   0-font.getsize(text)[1]/4),text,col,font=font)
        
        topsize = font.getsize(text)
        # Find negative colour for the sound
        text = dat["word_type"]
        fontsize = 1        
        img_fraction = 0.3   
        # Pick some text font at random
        font_path = self.pick_font("Text")
        #print(font_path)
        font = ImageFont.truetype(font_path,fontsize)
        while font.getsize(text)[0] < img_fraction*image.size[0]:
            fontsize += 1
            font = ImageFont.truetype(font_path,fontsize)
            font2 = ImageFont.truetype(font_path,fontsize+1)
        # Find average colour
        col = image.resize((1,1)).getpixel((0,0))
        col = self.compliment(col)
        col_hsv = self.rgb2hsv(col)
        hue = ((col_hsv[0] + uniform(-45,45)) % 360)/360
        val = (col_hsv[2]+0*uniform(-1,1) % 255)/255
        col = self.hsv2rgb(hue, col_hsv[1], val)
        # Center the main word
        draw.text(((image.size[0]-font.getsize(text)[0])/2,
                   image.size[1] - font2.getsize(text)[1] - 10),
                  text,(0,0,0),font=font2)
        draw.text(((image.size[0]-font.getsize(text)[0])/2,
                   image.size[1] - font.getsize(text)[1] - 9),
                  text,col,font=font)
        
        image = image.convert("RGB")
        image.save("Images/{}pic1.jpg".format(nn),"JPEG",quality=100,)
    
    
    def draw_img2(self,dat,nn=""):
        # Open bgimg.jpg image resize and crop

        image1 = Image.open("Images/bgimg.jpg").convert("RGBA")
        image = Image.new("RGB",image1.size,"YELLOW")
        image.paste(image1,(0,0),image1)
        image = image.convert("RGB")
        image = image.resize((1140,1140),Image.ANTIALIAS)
        image = image.crop((0,0,1120-30,1120-30))
        
        # Find average colour
        col = image.resize((1,1)).getpixel((0,0))
        col = self.compliment(col)
        col_hsv = self.rgb2hsv(col)
        hue = ((col_hsv[0] + uniform(-45,45)) % 360)/360
        val = (col_hsv[2]+0*uniform(-1,1) % 255)/255
        col = self.hsv2rgb(hue, col_hsv[1], val)
        
        # Add meaning text
                
        # Use one of the filters at random        
        self.get_filter()(image).save('Images/pic2.jpg')
        image = Image.open("Images/pic2.jpg")
        image = image.resize((1080,1080),Image.ANTIALIAS)
        image = image.filter(ImageFilter.BLUR)                        
        #enhancer = ImageEnhance.Sharpness(image)
        #image = enhancer.enhance(0.5)        
        image = ImageEnhance.Color(image)
        image = image.enhance(1.2)        
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.1)        
        #enhancer = ImageEnhance.Sharpness(image)
        #image = enhancer.enhance(1.5)        
        image = image.filter(ImageFilter.BLUR)
                
        image = image.convert("RGB")
        image.save("Images/pic2.jpg","JPEG",quality=100,)
        
        img = ImageText("Images/pic2.jpg")
        text = dat["usage"]
        # Pick some text font at random
        font_path = self.pick_font("Text")

        img.write_text(("center",0),text,font_path,font_size='fill',color=(0,0,0),max_width=800,max_height=200)
        img.write_text(("center",2),text,font_path,font_size='fill',color=(255,255,255),max_width=800,max_height=200)
        #bw,bh,oh = img.write_text_box(('center',0), text, box_width=1000, box_height=200, font_filename=font_path,
        #                   font_size=28, color=(0,0,0))
        #bw,bh,oh = img.write_text_box(('center',2), text, box_width=1000, box_height=200, font_filename=font_path,
        #                   font_size=28, color=(255,255,255))
        
        text = dat["def"] + " " + dat["etym"]
        # Add meaning text
        
        font_path = self.pick_font("Text")
        
        #font_size = img.get_font_size(text,font_path,800,800)
        #print(font_size)
        #img.write_text(('center',200),text,font_path,font_size, col,200,200)
        img.write_text_box((200, 200), text, box_width=800, box_height=800, font_filename=font_path,
                           font_size = 80, color=(0,0,0))
        img.write_text_box((202, 202), text, box_width=800, box_height=800, font_filename=font_path,
                           font_size = 80, color=(255,255,255))
       
        img.save("Images/{}pic2.jpg".format(nn))
    
    def pick_font(self,folder):
        from random import randint
        # Randomly pick a font
        fonts = []
        for file in os.listdir("fonts/{}".format(folder)):
            if(file.endswith(".ttf") or file.endswith(".otf")):
                fonts.append(os.path.join("fonts/{}".format(folder),file))
        return fonts[randint(0,len(fonts)-1)]
        
    def hilo(self,a,b,c):
        if c < b: b, c = c, b
        if b < a: a, b = b, a
        if c < b: b, c = c, b
        return a + c
    
    def compliment(self,col):
        k = self.hilo(col[0],col[1],col[2])
        return tuple(k-u for u in (col[0],col[1],col[2]))
    
    def get_filter(self):
        from random import randint
        # Pick one filter at random
        filters_list = ['aden', 'brooklyn', 'clarendon', 'earlybird', 'gingham', 'hudson', 'kelvin', 'lark', 'lofi', 'maven', 'mayfair', 'nashville', 'perpetua', 'reyes', 'rise', 'slumber', 'stinson', 'toaster', 'valencia', 'walden', 'xpro2']
        return getattr(pilgram,filters_list[randint(0,len(filters_list))-1])
    
    def test_from_data(self):
        import json
        # Open data file
        with open("misc/data.json","r") as f:
            data = json.load(f)
        c = 1
        for word in data[705:750]:
            print(word["word"])
            self.download_image(word["word"])
            self.draw_img1(word,c)
            self.draw_img2(word,c)
            c+=1
            