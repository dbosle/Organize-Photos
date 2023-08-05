#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: dbosle
# Date: 13.05.2021
# Organize Photos v1.0

import sys # for arguments
import os # for directory operations
import exifread 
from datetime import datetime
from os import path
import shutil
import random
from tkinter import Tk, filedialog


filetypes = [".jpg", ".jpeg", ".png", ".jfif", ".tiff", ".tif"]
mediaFileTypes = [".mp4", ".mov", ".avi", ".3gp", ".m4a"]


def processImage(imageFile, name, extension, filepath):
    mintimestamp = getMinCreationTime(filepath)
    targetfolder = createdir(mintimestamp)
    
    dt_object = datetime.fromtimestamp(mintimestamp)
    filename = str(dt_object.day) + setmonth(dt_object.month) + str(dt_object.year) + "-" + name + extension # file name
    
    targetfilepath = os.path.join(targetfolder, getfilename(os.path.join(targetfolder, filename), mintimestamp, name, extension)) # get new file path
    
    shutil.copyfile(filepath, targetfilepath) # copy file


def processVideo(imageFile, name, extension, filepath):
    mintimestamp = getMinCreationDateFromMedia(filepath)
    targetfolder = createdir(mintimestamp)
    
    dt_object = datetime.fromtimestamp(mintimestamp)
    filename = str(dt_object.day) + setmonth(dt_object.month) + str(dt_object.year) + "-" + name + extension # file name
    
    targetfilepath = os.path.join(targetfolder, getfilename(os.path.join(targetfolder, filename), mintimestamp, name, extension)) # get new file path
    
    shutil.copyfile(filepath, targetfilepath) # copy file   
        

def getfilename(targetfilepath, mintimestamp, name, extension):
    if(path.exists(targetfilepath)):
        dt_object = datetime.fromtimestamp(mintimestamp)
        newfilename = str(dt_object.day) + setmonth(dt_object.month) + str(dt_object.year) + "-" + name + "-" + str(random.randint(1,100)) + extension # new file name
        return getfilename(newfilename, mintimestamp, name, extension)
    else:
        return targetfilepath


def getMinCreationTime(imageFile):
    image = open(imageFile, 'rb')
    exifData = exifread.process_file(image, details=False)
    exifdt = exifdto = datetime.now()

    try:
        if (exifData.get('DateTime') is not None):
            exifdt = datetime.strptime(str(exifData.get('DateTime')), "%Y:%m:%d %H:%M:%S")
        if (exifData.get('EXIF DateTimeOriginal') is not None):
            exifdto = datetime.strptime(str(exifData.get('EXIF DateTimeOriginal')), "%Y:%m:%d %H:%M:%S")
    except: 
        i = False #For Debugging
        
    imgmt = os.path.getmtime(imageFile) # değiştirme timestamp
    imgct = os.path.getctime(imageFile) # oluşturma timestamp
    exifdt = datetime.timestamp(exifdt)
    exifdto = datetime.timestamp(exifdto)

    stamps = [imgmt, imgct, exifdt, exifdto]
    stamps.sort()
    return min(stamps)


def getMinCreationDateFromMedia(imageFile):
    imgmt = os.path.getmtime(imageFile) # değiştirme timestamp
    imgct = os.path.getctime(imageFile) # oluşturma timestamp
    stamps = [imgmt, imgct]
    stamps.sort()
    return min(stamps)

   
def setmonth(no):
    switcher = {
        1: "Ocak",
        2: "Şubat",
        3: "Mart",
        4: "Nisan",
        5: "Mayıs",
        6: "Haziran",
        7: "Temmuz",
        8: "Ağustos",
        9: "Eylül",
        10: "Ekim",
        11: "Kasım",
        12: "Aralık"
    }
    return switcher.get(no, "Invalid month") 
    
    
def createdir(timestamp):
    dt_object = datetime.fromtimestamp(timestamp)
    targetFolder = os.path.join(target, str(dt_object.year)) # year directory path
    monthfolder = str(dt_object.month) + "-" + setmonth(dt_object.month) + "-" + str(dt_object.year) #month folder directory path
    targetFolder = os.path.join(targetFolder, monthfolder) # target directory path

    # Create folders if not exist
    if(not path.exists(targetFolder)):
        os.makedirs(targetFolder, exist_ok=False)


    return targetFolder
    
    
def walkdir(directory):
    for root, subdirs, files in os.walk(directory):
        for imageFile in files:
            filepath = os.path.join(root, imageFile)
            name, extension = os.path.splitext(imageFile)
            if (extension.lower() in filetypes):
                processImage(imageFile, name, extension, filepath)
            elif (extension.lower() in mediaFileTypes):
                processVideo(imageFile, name, extension, filepath)
                
    
def usage():
    print("\nUsage: ")
    print(" ", __file__," <source_path> <target_path>\n\n")
    exit()
    
    
if __name__ == "__main__":
    if (len(sys.argv) != 3 ):
        usage()

 
    source = sys.argv[1] #source dir
    target = sys.argv[2] #target dir
    walkdir(source_dir)
