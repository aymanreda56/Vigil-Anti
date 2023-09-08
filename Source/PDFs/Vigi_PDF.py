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

with open("secret.pkl", 'rb') as f:
    Ascii_ARTS = pickle.load(f)
magic_number = random.randint(0, len(Ascii_ARTS))



columns = ['pages', 'obj', 'endobj', 'stream', 'endstream', 'xref', 'trailer', 'startxref', 'encrypt', 'ObjStm', 'JS', 'Javascript', 'AA', 'OpenAction', 'Acroform', 'JBIG2Decode', 'RichMedia', 'launch', 'EmbeddedFile', 'XFA', 'Colors', 'header_regex_boolean', 'PDF_Version']


file_path = sys.argv[1]
path_to_script_folder = sys.argv[2]
model_path = sys.argv[3]


print(Ascii_ARTS[magic_number])


print("\n\n[+] ================ Extracting Features... ======================\n")
feature_df = Extract_Features(file_path, path_to_script_folder)
feature_df = reorder_df(feature_df, [], ready_columns=columns)

print("\n\n[+] ================ Testing on the ML model... ======================\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n")

Pred = test_on_file(feature_df, model_path)

if (Pred[0] == True):
    print("\n\n[+] ================ MALICIOUS FILE DETECTED ======================\n")

elif(Pred[0] == False):
    print("\n\n[+] ================ File is Safe :) ======================\n")