import features
import helpers
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

parser = ArgumentParser()
group = parser.add_mutually_exclusive_group()
group1= parser.add_mutually_exclusive_group()
parser.usage = '''scan a file like this:
python Vigi_PE.py <file_path>'''
parser.add_argument('file_path', help="Specify the file or folder path", type=str)
parser.add_argument('-f', '--folder-scan', help='Folder scan, to recursively scan a passed folder for malwares', action='store_true')
group1.add_argument('-v', '--verbose', help='Display Verbose output', action='store_true')
group1.add_argument('-q', '--quiet', help='Silence all prints', action='store_true')
parser.add_argument('--no-ascii-art', help='Turns off the ascii art from displaying', default=False, action='store_true')
group.add_argument('-m', '--model', help="Specifies the used model, Default = RF", choices=['RF', 'SVM', 'GBT', 'LGB', 'NN1', 'NN2', 'NN3', 'NN4', 'NN5'], default='RF', type=str)
parser.add_argument('-o', '--output', help='Writes output to the specified file', type=str, default='')
group.add_argument('-a', '--aggressive', help='Aggressive scan, Try all the models and display all outputs', default=False, action='store_true')

args: Namespace = parser.parse_args()


if(not args.file_path):
     print(f"Specify the File or folder path please")
     print(f"                   NOOB\nCheck the help menu by 'python Vigi_EXE.py -h'")
     exit()
if(not os.path.exists(args.file_path)):
     print(f"The specified path: {args.file_path} does not exist")
     exit()
if(args.folder_scan and os.path.isfile(args.file_path)):
     print(f"Specify a Folder not a file please, delete the -f argument if you want to scan a single file")
     exit()
if((not args.folder_scan) and os.path.isdir(args.file_path)):
     print(f"The passed path is not a folder, please add the -f argument if you want to scan a folder")
     exit()
# if(args.model != "RF" and args.aggressive):
#      print(f'You cannot use -m and -a together, either specify a single model using -m, or use all models using -a')
#      exit()

outfile = args.output
if(args.output):
     outfile = args.output
     with open(outfile, 'w') as f:
          f.write('Vigi_EXE Logs:\n')

verbose= False
if(args.verbose):
    helpers.printo(outfile, f"\n\nHave a cup of coffee while Vigil-Anti does its thing :)\n\n\n")
    time.sleep(2)
    verbose=True



     


'''
options:
-f --folder=     (input folder, scans the folder recursively)
-v --verbose     (verbose output and progress, default = False)
--no-ascii-art   (turns off the ascii art, default = False)
-m --model       (choose a certain model from [], default = rf)
-o               (write output to file)
-h               (help menu)
-a --aggressive   (aggressive scan, Try all models and display all outputs)
'''







in_file_Path = args.file_path
models_path = os.path.join(os.getcwd(),'models')
if(args.model == 'RF'):
     model_path = os.path.join(models_path, 'rf.pkl')
elif(args.model == 'SVM'):
     model_path = os.path.join(models_path, 'svm.pkl')
elif(args.model == 'GBT'):
     model_path = os.path.join(models_path, 'gbt.pkl')
elif(args.model == 'LGB'):
     model_path = os.path.join(models_path, 'lgb.pkl')
elif(args.model == 'NN1'):
     model_path = os.path.join(models_path, 'NN1.pkl')
elif(args.model == 'NN2'):
     model_path = os.path.join(models_path, 'NN2.pkl')
elif(args.model == 'NN3'):
     model_path = os.path.join(models_path, 'NN3.pkl')
elif(args.model == 'NN4'):
     model_path = os.path.join(models_path, 'NN4.pkl')
elif(args.model == 'NN5'):
     model_path = os.path.join(models_path, 'NN5.pkl')

if(not (args.no_ascii_art or args.quiet)):
    with open (os.path.join(os.getcwd(), 'models', 'secret.pkl'), 'rb') as f:
        ascii_art = pickle.load(f)

    helpers.printo(outfile, ascii_art[randint(0, len(ascii_art)-1)])
    

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






def Scan_File(file_path, model_path):
     if(not args.quiet):
          helpers.printo(outfile, "\n\n[+] ================ Checking file Type... ======================\n")

     with ExifToolHelper() as et:
          try:
               metadata = et.get_metadata(file_path)
          except:
               helpers.printo(outfile, f"File {file_path} not Parseable")
               return -1
     for i, d in enumerate(metadata):
          if 'File:FileType' in d.keys():
               fileTypeDict = d
     if(not (re.findall('win', fileTypeDict['File:FileType'], re.IGNORECASE))):
          if(re.findall('pdf', fileTypeDict['File:FileType'], re.IGNORECASE)):
               helpers.printo(outfile, f"File is a PDF, please use our other tool Vigi_PDF.py")
               return -1
          helpers.printo(outfile, f"File is not a windows PE !!")
          return -1
     helpers.printo(outfile, f"OK :)")

     if(not args.quiet):
          helpers.printo(outfile, "\n\n[+] ================ Extracting Features... ======================\n")
     extractor = features.PEFeatureExtractor(print_feature_warning=verbose)
     if(extractor == -1):
          helpers.printo(outfile, "File is not a PE FILE !")
          return -1



     with open (file_path, 'rb') as f:
          PE_file = f.read()



     Raw_features = extractor.raw_features(PE_file)
     if(Raw_features == -1):
          helpers.printo(outfile, "File is not a PE FILE !")
          return -1

     df_features = helpers.Preprocess_Features_into_dataframe(Raw_features, verbose=verbose, outfile=outfile)



     if(not args.quiet):
          helpers.printo(outfile, "\n\n[+] ================ Testing on the ML model... ======================\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n")



     if(not args.aggressive):
          pred = helpers.Inference(df_features, model_path, verbose=verbose, outfile=outfile)
          if (pred == True):
               if(not args.quiet):
                    helpers.printo(outfile, color.BOLD + "\n\n[+] ================ MALICIOUS FILE DETECTED ======================\n" + color.END)
               else:
                    helpers.printo(outfile, 'Malicious')
               return "Malicious"

          elif(pred == False):
               if(not args.quiet):
                    helpers.printo(outfile, color.BOLD + "\n\n[+] ================ File is Safe :) ======================\n"  + color.END)
               else:
                    helpers.printo(outfile, 'Safe')
               return "Safe"

     else:
          models={'rf.pkl': 'Random Forest', 'svm.pkl': 'SVM', 'gbt.pkl': 'Gradient Boosted Trees', 'lgb.pkl': "Light GBM", 'NN1.pkl': "NN1", 'NN2.pkl':"NN2", 'NN3.pkl':"NN3", 'NN4.pkl':"NN4", 'NN5.pkl':"NN5"}
          returned_array=[]
          for mod, name in models.items():
               model_path= os.path.join(models_path, mod)
               pred = helpers.Inference(df_features, model_path, verbose=verbose, outfile=outfile)
               if (pred == True):
                    helpers.printo(outfile, f'Model: {name}               ------>            Malicious')
                    returned_array.append(f'Model: {name}               ------>            Malicious')

               elif(pred == False):
                    helpers.printo(outfile, f'Model: {name}               ------>            Safe')
                    returned_array.append(f'Model: {name}               ------>            Safe')
          return returned_array


if(args.folder_scan):
     folder_path = pathlib.Path(in_file_Path)
     allFile_paths= list(folder_path.glob('*'))
     all_results = {}
     for fp in allFile_paths:
          helpers.printo(outfile, f"\n\nFile: {fp}:")
          result = Scan_File(file_path=fp, model_path=model_path)
          if(type(result) == list):
               for i in result: helpers.printo(outfile, i) if i != -1 else helpers.printo(outfile, "Cannot be Parsed or scanned")
          else: helpers.printo(outfile, result) if result != -1 else helpers.printo(outfile, "Cannot be Parsed or scanned")
          all_results[fp] = result
     for k, v in all_results.items():
          helpers.printo(outfile, f"---------------------------------------------------------------------------------------------------------\n\n\nFile {k}: \n")
          if(type(result) == list):
               for i in result: helpers.printo(outfile, i) if i != -1 else helpers.printo(outfile, "Cannot be Parsed or scanned")
          else: helpers.printo(outfile, result) if result != -1 else helpers.printo(outfile, "Cannot be Parsed or scanned")
else: Scan_File(file_path=in_file_Path, model_path=model_path)