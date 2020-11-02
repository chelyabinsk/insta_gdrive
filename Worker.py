#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main file.

Select a word and pre-process data
Draw Image
Upload to GDrive
Send message
"""

from word import Word_picker
from ImageArtist import ImageArtist
from service_google import GDrive
from os import getenv, environ
from InstagramAPI import InstagramAPI
from randomEmoji import random_emoji

class insta_bot():
    def __init__(self,username,password):
        self.api = InstagramAPI(username,password)

        if(self.api.login()):
            self.api.getSelfUserFeed()
        else:
            print("Can't login!")
    
    def write_message(self,data,emoji):
        msg = """{} ({} - {})\n
Means: {}\n
Sentence: {}\n
Etymology: {}\n
Emoji of the day: {} ({})\n
Unicode: {}
""".format(data['word'].capitalize(),
                   data['phonetics'],
                   data['word_type'],
                   data['def'],
                   data['usage'].capitalize(),
                   data['etym'],
                   emoji[0],
                   emoji[2],
                   emoji[1]
                   )
        return msg
    
    def write_status(self,data,emoji,status):
        txt = """Today's word is {0} along side the ({2}) {1} emoji.\n
The word {0} means {3}. Its etymology is, {4}\n
You can use it in a sentence like, {5}\n
{6}\n
status: {7}
        """.format(data['word'],
                  emoji[0],
                  emoji[2],
                  data['def'],
                  data['etym'],
                  data['usage'],
                  ' '.join(data['hashtags']),
                  status
        )
        return txt

def main():
    G = GDrive()
    
    WP = Word_picker()
    WP.get_word()
    word = WP.page_data
    status = WP.status
    
    # Login into my account
    bot = insta_bot(getenv('INSTA_ACC'),getenv('INSTA_PASS'))
    emoji_data = random_emoji()
    txt = bot.write_message(word,emoji_data)
    debug_txt = bot.write_status(word,emoji_data,status)
    
    recv_ids = eval(getenv('INSTA_IDS'))
        
    drawer = ImageArtist()
    print("Downloading image")
    drawer.download_image(word["word"])
    print('Drawing stuff')
    drawer.draw_img1(word)
    drawer.draw_img2(word)
    print('Sending messages')
    for c,recv in enumerate(recv_ids):
        if c == 0:
            bot.api.direct_message(debug_txt,recv['uid'])
        else:
            bot.api.direct_message(txt,recv['uid'])
    print('Cleaning folder')
    G.clean_folder()
    print("Uploading images")
    G.upload_files(["Images/pic1.jpg","Images/pic2.jpg"])
    print("Done")

main()