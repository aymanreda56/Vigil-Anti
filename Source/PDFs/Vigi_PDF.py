from helpers import *
import os
import re
import pandas as pd
import numpy as np
from subprocess import run
import sys
import pickle
from colorama import Fore
import random

with open(os.path.join(os.getcwd(),'models',"secret.pkl"), 'rb') as f:
    Ascii_ARTS = pickle.load(f)
magic_number = random.randint(0, len(Ascii_ARTS)-1)

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


columns = ['pages', 'obj', 'endobj', 'stream', 'endstream', 'xref', 'trailer', 'startxref', 'encrypt', 'ObjStm', 'JS', 'Javascript', 'AA', 'OpenAction', 'Acroform', 'JBIG2Decode', 'RichMedia', 'launch', 'EmbeddedFile', 'XFA', 'Colors', 'header_regex_boolean', 'PDF_Version']


file_path = sys.argv[1]
path_to_script_folder = os.path.join(os.getcwd(),'PDFid')
model_path = sys.argv[2]


print(Ascii_ARTS[magic_number])


print("\n\n[+] ================ Extracting Features... ======================\n")
feature_df = Extract_Features(file_path, path_to_script_folder)
if(not(type(feature_df) == int and feature_df == 1)):
    feature_df = reorder_df(feature_df, [], ready_columns=columns)

    print("\n\n[+] ================ Testing on the ML model... ======================\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n")

    Pred = test_on_file(feature_df, model_path)




    

    if (Pred[0] == True):
        print(color.BOLD + "\n\n[+] ================ MALICIOUS FILE DETECTED ======================\n" + color.END)

    elif(Pred[0] == False):
        print(color.BOLD + "\n\n[+] ================ File is Safe :) ======================\n"  + color.END)