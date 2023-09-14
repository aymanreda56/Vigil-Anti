import VPhelpers
import os
import re
import sys
import json
import pickle
import time
from exiftool import ExifToolHelper
from random import randint
from argparse import ArgumentParser, Namespace
import glob, pathlib

current_directory = os.path.split(os.path.realpath(__file__))[0]


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


path_to_script_folder = os.path.join(current_directory,'PDFid')


def checkFileType(file_path):
     with ExifToolHelper() as et:
          try:
               metadata = et.get_metadata(file_path)
               
               for i, d in enumerate(metadata):
                    if 'File:FileType' in d.keys():
                         fileTypeDict = d
                         break
               if(re.findall('win', fileTypeDict['File:FileType'], re.IGNORECASE)):
                    return 1
               elif(re.findall('pdf', fileTypeDict['File:FileType'], re.IGNORECASE)):
                    return 2
               else:
                    VPhelpers.printo('', color.BOLD+ color.YELLOW + f"File {file_path} is not a windows PE !!"  + color.END)
                    return 0
          except:
                VPhelpers.printo('', color.BOLD+ color.PURPLE + f"File {file_path} is Corrupt, delete it if you suspect it!"  + color.END)
                return -1


def ScanFile_pdf(file_path, modelPath, quiet, aggressive, verbose, output, no_ascii_art):
    if(not (no_ascii_art or quiet)):
          with open (os.path.join(current_directory, 'models', 'secret.pkl'), 'rb') as f:
               ascii_art = pickle.load(f)

    VPhelpers.printo(output, ascii_art[randint(0, len(ascii_art)-1)])

    if(not quiet):
        VPhelpers.printo(output, "\n\n[+] ================ Checking file Type... ======================\n")

    FileType = checkFileType(file_path=file_path)
    if(FileType == 1):
        VPhelpers.printo(output, f"File is a PE, please use our other tool Vigi_EXE.py")
        return -1
    elif(FileType == 2):
        pass
    elif(FileType == 0):
        VPhelpers.printo(output, f"File is not a PDF !!")
        return -1
    else:
        VPhelpers.printo(output, f"File {file_path} not Parseable")
        return -1
    
    
    VPhelpers.printo(output, f"OK :)")

    if(not quiet):
        VPhelpers.printo(output, "\n\n[+] ================ Extracting Features... ======================\n")

    feature_df = VPhelpers.Extract_Features(file_path=file_path, path_to_script_folder=path_to_script_folder, outfile=output, verbose=verbose)
    if(not(type(feature_df) == int and feature_df == 1)):
        feature_df = VPhelpers.reorder_df(feature_df, [], ready_columns=columns)
        if(not quiet):
            VPhelpers.printo(output, "\n\n[+] ================ Testing on the ML model... ======================\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n")

        Pred = VPhelpers.test_on_file(feature_df, modelPath, outfile=output)


        if (Pred[0] == True):
            if(not quiet):
                VPhelpers.printo(output,color.BOLD+ color.RED + "\n\n[+] ================ MALICIOUS FILE DETECTED ======================\n" + color.END)
            else:
                    VPhelpers.printo(output, 'Malicious')
            return 1

        elif(Pred[0] == False):
            if(not quiet):
                VPhelpers.printo(output, color.BOLD+ color.GREEN + "\n\n[+] ================ File is Safe :) ======================\n"  + color.END)
            else:
                VPhelpers.printo(output, 'Safe')
            return 0
        

def ScanFolder_PDF(folder_in_path, model_path, quiet, aggressive, verbose, outfile, no_ascii_art):
    if(not (no_ascii_art or quiet)):
          with open (os.path.join(current_directory, 'models', 'secret.pkl'), 'rb') as f:
               ascii_art = pickle.load(f)

    VPhelpers.printo(outfile, ascii_art[randint(0, len(ascii_art)-1)])
    folder_path = pathlib.Path(folder_in_path)
    allFile_paths= list(folder_path.glob('*'))
    all_results = {}
    for fp in allFile_paths:
        VPhelpers.printo(outfile, f"\n\nFile: {fp}:")
        result = ScanFile_pdf(file_path=fp, modelPath=model_path, quiet=quiet, aggressive=aggressive, verbose=verbose, output=outfile)
        if(type(result) == list):
            for i in result: VPhelpers.printo(outfile, i) if i != -1 else VPhelpers.printo(outfile, "Cannot be Parsed or scanned")
        else: VPhelpers.printo(outfile, result) if result != -1 else VPhelpers.printo(outfile, "Cannot be Parsed or scanned")
        all_results[fp] = result
    for k, v in all_results.items():
        VPhelpers.printo(outfile, f"---------------------------------------------------------------------------------------------------------\n\n\nFile {k}: \n")
        if(type(result) == list):
            for i in result: VPhelpers.printo(outfile, i) if i != -1 else VPhelpers.printo(outfile, "Cannot be Parsed or scanned")
        else: VPhelpers.printo(outfile, result) if result != -1 else VPhelpers.printo(outfile, "Cannot be Parsed or scanned")