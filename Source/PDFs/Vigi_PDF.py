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

current_directory = os.path.split(os.path.realpath(__file__))[0]


parser = ArgumentParser()
group1= parser.add_mutually_exclusive_group()
parser.usage = '''scan a file like this:
python Vigi_PDF.py <file_path>'''
parser.add_argument('file_path', help="Specify the file or folder path", type=str)
parser.add_argument('-f', '--folder-scan', help='Folder scan, to recursively scan a passed folder for PDF malwares', action='store_true')
group1.add_argument('-v', '--verbose', help='Display Verbose output', action='store_true')
group1.add_argument('-q', '--quiet', help='Silence all prints', action='store_true')
parser.add_argument('--no-ascii-art', help='Turns off the ascii art from displaying', default=False, action='store_true')
parser.add_argument('-o', '--output', help='Writes output to the specified file', type=str, default='')

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






in_file_Path = args.file_path


if(not (args.no_ascii_art or args.quiet)):
    with open (os.path.join(current_directory, 'models', 'secret.pkl'), 'rb') as f:
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





columns = ['pages', 'obj', 'endobj', 'stream', 'endstream', 'xref', 'trailer', 'startxref', 'encrypt', 'ObjStm', 'JS', 'Javascript', 'AA', 'OpenAction', 'Acroform', 'JBIG2Decode', 'RichMedia', 'launch', 'EmbeddedFile', 'XFA', 'Colors', 'header_regex_boolean', 'PDF_Version']


path_to_script_folder = os.path.join(current_directory,'PDFid')
model_path = os.path.join(current_directory, 'models', 'rf.pkl')


def ScanFile(file_path):

    if(not args.quiet):
        helpers.printo(outfile, "\n\n[+] ================ Checking file Type... ======================\n")

    with ExifToolHelper() as et:
        try:
            metadata = et.get_metadata(file_path)
            for i, d in enumerate(metadata):
                if 'File:FileType' in d.keys():
                    fileTypeDict = d
            if(not (re.findall('pdf', fileTypeDict['File:FileType'], re.IGNORECASE))):
                if(re.findall('win', fileTypeDict['File:FileType'], re.IGNORECASE)):
                    helpers.printo(outfile, f"File is a PE, please use our other tool Vigi_EXE.py")
                    return -1
                helpers.printo(outfile, f"File is not a PDF !!")
                return -1
        except:
            helpers.printo(outfile, f"File {file_path} not Parseable")
            return -1
    
    helpers.printo(outfile, f"OK :)")




    if(not args.quiet):
        helpers.printo(outfile, "\n\n[+] ================ Extracting Features... ======================\n")

    feature_df = helpers.Extract_Features(file_path, path_to_script_folder, outfile=outfile, verbose=verbose)
    if(not(type(feature_df) == int and feature_df == 1)):
        feature_df = helpers.reorder_df(feature_df, [], ready_columns=columns)
        if(not args.quiet):
            helpers.printo(outfile, "\n\n[+] ================ Testing on the ML model... ======================\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n\t\t\t\t||\n")

        Pred = helpers.test_on_file(feature_df, model_path, outfile=outfile)


        if (Pred[0] == True):
            if(not args.quiet):
                helpers.printo(outfile,color.BOLD + "\n\n[+] ================ MALICIOUS FILE DETECTED ======================\n" + color.END)
            else:
                    helpers.printo(outfile, 'Malicious')
            return "Malicious"

        elif(Pred[0] == False):
            if(not args.quiet):
                helpers.printo(outfile, color.BOLD + "\n\n[+] ================ File is Safe :) ======================\n"  + color.END)
            else:
                helpers.printo(outfile, 'Safe')
            return "Safe"
        



if(args.folder_scan):
     folder_path = pathlib.Path(in_file_Path)
     allFile_paths= list(folder_path.glob('*'))
     all_results = {}
     for fp in allFile_paths:
          helpers.printo(outfile, f"\n\nFile: {fp}:")
          result = ScanFile(file_path=fp)
          if(type(result) == list):
               for i in result: helpers.printo(outfile, i) if i != -1 else helpers.printo(outfile, "Cannot be Parsed or scanned")
          else: helpers.printo(outfile, result) if result != -1 else helpers.printo(outfile, "Cannot be Parsed or scanned")
          all_results[fp] = result
     for k, v in all_results.items():
          helpers.printo(outfile, f"---------------------------------------------------------------------------------------------------------\n\n\nFile {k}: \n")
          if(type(result) == list):
               for i in result: helpers.printo(outfile, i) if i != -1 else helpers.printo(outfile, "Cannot be Parsed or scanned")
          else: helpers.printo(outfile, result) if result != -1 else helpers.printo(outfile, "Cannot be Parsed or scanned")
else: ScanFile(file_path=in_file_Path)
