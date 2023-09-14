import os
import sys
sys.path.append(os.path.split(os.path.realpath(__file__))[0])
import features
import helpers
import re
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



def Scan_File_exe(file_path, model_path, quiet, aggressive, verb, outfile, no_ascii_art):
     if(not (no_ascii_art or quiet)):
          with open (os.path.join(current_directory, 'models', 'secret.pkl'), 'rb') as f:
               ascii_art = pickle.load(f)

     helpers.printo(outfile, ascii_art[randint(0, len(ascii_art)-1)])
     if(not quiet):
          helpers.printo(outfile, "\n\n[+] ================ Checking file Type... ======================\n")

     fileType = checkFileType(file_path=file_path)
     if(fileType == 1):
          pass
     elif(fileType == 2):
          helpers.printo(outfile, f"File is a PDF, please use our other tool Vigi_PDF.py")
          return -1
     elif(fileType == 0):
          helpers.printo(outfile, color.YELLOW+ color.BOLD +f"File {file_path} is not a windows PE !!"+ color.END)
          return -1
     else:
          helpers.printo(outfile, color.PURPLE+ color.BOLD +f"File {file_path} is Corrupt, delete it if you suspect it!"+ color.END)
          return -1
     
     helpers.printo(outfile, f"OK :)")

     if(not quiet):
          helpers.printo(outfile, "\n\n[+] ================ Extracting Features... ======================\n")
     extractor = features.PEFeatureExtractor(print_feature_warning=verb)
     if(extractor == -1):
          helpers.printo(outfile, "File is not a PE FILE !")
          return -1


     try:
          with open (file_path, 'rb') as f:
               PE_file = f.read()
     except Exception as e:
          helpers.printo(outfile, f"File {file_path} Cannot be opened {str(e)}")
          return -1

     
     Raw_features = extractor.raw_features(PE_file)
     if(Raw_features == -1):
          helpers.printo(outfile, "File is not a PE FILE !")
          return -1

     df_features = helpers.Preprocess_Features_into_dataframe(Raw_features, verbose=verb, outfile=outfile)



     if(not quiet):
          helpers.printo(outfile, "\n\n[+] ================ Testing on the ML model... ======================\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n")



     if(not aggressive):
          pred = helpers.Inference(df_features, model_path, verbose=verb, outfile=outfile)
          if (pred == True):
               if(not quiet):
                    helpers.printo(outfile, color.RED+ color.BOLD + "\n\n[+] ================ MALICIOUS FILE DETECTED ======================\n" + color.END)
               else:
                    helpers.printo(outfile, 'Malicious')
               return 1

          elif(pred == False):
               if(not quiet):
                    helpers.printo(outfile, color.GREEN+ color.BOLD + "\n\n[+] ================ File is Safe :) ======================\n"  + color.END)
               else:
                    helpers.printo(outfile, 'Safe')
               return 0

     else:
          models={'rf.pkl': 'Random Forest', 'svm.pkl': 'SVM', 'gbt.pkl': 'Gradient Boosted Trees', 'lgb.pkl': "Light GBM", 'NN1.pkl': "NN1", 'NN2.pkl':"NN2", 'NN3.pkl':"NN3", 'NN4.pkl':"NN4", 'NN5.pkl':"NN5"}
          returned_array=[]
          models_path = os.path.join(current_directory, 'models')
          for mod, name in models.items():
               model_path= os.path.join(models_path, mod)
               pred = helpers.Inference(df_features, model_path, verbose=verb, outfile=outfile)
               if (pred == True):
                    helpers.printo(outfile, f'Model: {name}               ------>            Malicious')
                    returned_array.append((f'Model: {name}               ------>            Malicious', (name, 1)))

               elif(pred == False):
                    helpers.printo(outfile, f'Model: {name}               ------>            Safe')
                    returned_array.append((f'Model: {name}               ------>            Safe', (name, 0)))
          return returned_array




def Folder_Scan_exe(folder, modelpath, quiet, aggressive, verb, outfile, no_ascii_art):
     if(not (no_ascii_art or quiet)):
          with open (os.path.join(current_directory, 'models', 'secret.pkl'), 'rb') as f:
               ascii_art = pickle.load(f)

     helpers.printo(outfile, ascii_art[randint(0, len(ascii_art)-1)])
     folder_path = pathlib.Path(folder)
     allFile_paths= list(folder_path.glob('*'))
     all_results = {}
     for fp in allFile_paths:
          helpers.printo(outfile, f"\n\nFile: {fp}:")
          result = Scan_File_exe(file_path=fp, model_path=modelpath, quiet=quiet, aggressive=aggressive, verb=verb, outfile=outfile)
          if(type(result) == list):
               for i in result: helpers.printo(outfile, i[0]) if i != -1 else helpers.printo(outfile, "Cannot be Parsed or scanned")
          else: helpers.printo(outfile, result) if result != -1 else helpers.printo(outfile, "Cannot be Parsed or scanned")
          all_results[fp] = result
     for k, v in all_results.items():
          helpers.printo(outfile, f"---------------------------------------------------------------------------------------------------------\n\n\nFile {k}: \n")
          if(type(result) == list):
               for i in result: helpers.printo(outfile, i[0]) if i != -1 else helpers.printo(outfile, "Cannot be Parsed or scanned")
          else: helpers.printo(outfile, result) if result != -1 else helpers.printo(outfile, "Cannot be Parsed or scanned")
     return all_results


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
                    return 0
          except:
               return -1

