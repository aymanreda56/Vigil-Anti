import os
import sys
sys.path.append(os.path.split(os.path.realpath(__file__))[0])
import Vigi_EXE_lib as VE
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

parser = ArgumentParser()
group = parser.add_mutually_exclusive_group()
group1= parser.add_mutually_exclusive_group()
parser.usage = '''       scan a file like this:
                         python Vigi_PE.py <file_path>'''
parser.add_argument('file_path', help="Specify the file or folder path", type=str)
parser.add_argument('-f', '--folder-scan', help='Folder scan, to recursively scan a passed folder for malwares', action='store_true')
group1.add_argument('-v', '--verbose', help='Display Verbose output', action='store_true')
group1.add_argument('-q', '--quiet', help='Silence all prints', action='store_true')
parser.add_argument('--no-ascii-art', help='Turns off the ascii art from displaying', default=False, action='store_true')
group.add_argument('-m', '--model', help="Specifies the used model, Default = RF", choices=['RF', 'SVM', 'GBT', 'LGB', 'NN1', 'NN2', 'NN3', 'NN4', 'NN5'], default='RF', type=str)
parser.add_argument('-o', '--output', help='Writes output to the specified file', type=str, default='')
group.add_argument('-a', '--aggressive', help='Aggressive scan, Try all the models and display all outputs', default=False, action='store_true')
parser.add_argument('-l', '--library-use', help='To use this tool inside another tool (ie; import our tool into your code), DONT use this flag if you use our CLI.', default=False, action='store_true')

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

outputfile = args.output
if(args.output):
     outputfile = args.output
     with open(outputfile, 'w') as f:
          f.write('Vigi_EXE Logs:\n')

verbose= False
if(args.verbose):
    helpers.printo(outputfile, f"\n\nHave a cup of coffee while Vigil-Anti does its thing :)\n\n\n")
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
models_path = os.path.join(current_directory,'models')
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

# if(not (args.no_ascii_art or args.quiet)):
#     with open (os.path.join(current_directory, 'models', 'secret.pkl'), 'rb') as f:
#         ascii_art = pickle.load(f)

#     helpers.printo(outputfile, ascii_art[randint(0, len(ascii_art)-1)])
    


if(not args.library_use):
     if(args.folder_scan):
          VE.Folder_Scan_exe(folder=in_file_Path, modelpath=model_path, quiet=args.quiet, aggressive=args.aggressive, verb=verbose, outfile=outputfile, no_ascii_art=args.no_ascii_art)

     else: VE.Scan_File_exe(file_path=in_file_Path, model_path=model_path, quiet=args.quiet, aggressive=args.aggressive, verb=verbose, outfile=outputfile, no_ascii_art=args.no_ascii_art)