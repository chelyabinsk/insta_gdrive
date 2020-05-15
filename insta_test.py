#!/usr/bin/python3.6
#-*-coding: utf-8-*-
from datetime import datetime as d
import json
import datetime
from ImageArtist import ImageArtist
from service_google import GDrive

from datetime import date 
  
def numOfDays(date1, date2): 
    return (date2-date1).days 


def main():
    G = GDrive()
    G.clean_folder()
    G.download_files()
    # Read the file of words
    with open('misc/data.json', 'r') as f:
        data = json.load(f)
    
    date1 = date(2020, 5, 15) 
    date2 = datetime.date.today() 
    i = 702 + numOfDays(date1, date2)

    # Call the Drawer class with the text
    drawer = ImageArtist()
    
    print("Downloading image")
    drawer.download_image(data[i]["word"])
    print("Drawing stuff")
    drawer.draw_img1(data[i])
    drawer.draw_img2(data[i])
    
    print("Cleaning folder")
    G.clean_folder()
    print("Uploading images")
    G.upload_files(["Images/pic1.jpg","Images/pic2.jpg"])
    print("Done")


if __name__ == "__main__":
    main()
