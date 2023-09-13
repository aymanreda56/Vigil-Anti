import os
import re
import sys
sys.path.append('Vigi_EXE')
sys.path.append('Vigi_PDF')
import json
import pickle
import time
from exiftool import ExifToolHelper
from argparse import ArgumentParser, Namespace
import Vigi_EXE.Vigi_EXE_lib as VE
from subprocess import run, STDOUT
import glob, pathlib





import customtkinter as ctk

global file_path, folder_path

file_path, folder_path = False, False

def getFilePath():
    global file_path
    file_path = ctk.filedialog.askopenfilename()
    if(file_path):
        print(file_path)

def getFolderPath():
    global folder_path
    folder_path = ctk.filedialog.askdirectory()
    if(folder_path):
        print(folder_path)


def scanFile(file_path):
    



root = ctk.CTk()

scan_file_button = ctk.CTkButton(root, text='Scan a File!', command=getFilePath)
scan_file_button.pack()
scan_folder_button = ctk.CTkButton(root, text='Scan a Folder!', command=getFolderPath)
scan_folder_button.pack()







root.mainloop()