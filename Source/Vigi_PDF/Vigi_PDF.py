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
import Vigi_PDF_lib as VP

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
parser.add_argument('-a', '--aggressive',help='Aggressive scan, Try all the models and display all outputs', default=False, action='store_true')
parser.add_argument('-m', '--model', help="Specifies the used model, Default = RF", choices=['RF', 'SVM', 'GBT', 'LGB', 'NN1', 'NN2', 'NN3', 'NN4', 'NN5'], default='RF', type=str)

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


def main():
    if(args.folder_scan):
        VP.ScanFolder_PDF(folder_in_path=args.file_path, model_path=model_path, quiet=args.quiet, aggressive=args.aggressive, verbose=args.verbose, outfile=args.output)
    else: VP.ScanFile_pdf(file_path=args.file_path, modelPath=model_path, quiet=args.quiet, aggressive=args.aggressive, verbose=args.verbose, output=args.output)

if __name__ == '__main__':
     main()
