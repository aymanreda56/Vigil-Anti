import os
import sys
import re
from exiftool import ExifToolHelper
sys.path.append('Vigi_EXE')
sys.path.append('Vigi_PDF')
from argparse import ArgumentParser, Namespace
import Vigi_EXE.Vigi_EXE_lib as VE
import Vigi_PDF.Vigi_PDF_lib as VP
import glob, pathlib


current_directory = os.path.split(os.path.realpath(__file__))[0]
parent_directory = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
ExifTool_path = os.path.join(parent_directory, 'exiftool')
os.environ['PATH'] += ';'+ExifTool_path



parser = ArgumentParser()
group = parser.add_mutually_exclusive_group()
group1= parser.add_mutually_exclusive_group()
parser.usage = '''       scan a file like this:
                         python Vigil-Anti.py <file_path>'''
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
     print(f"                   NOOB\nCheck the help menu by 'python Vigil-Anti.py -h'")
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


models_path_exe = os.path.join(current_directory,"Vigi_EXE",'models')
models_path_pdf = os.path.join(current_directory,"Vigi_PDF",'models')
if(args.model == 'RF'):
     model_path_exe = os.path.join(models_path_exe, 'rf.pkl')
     model_path_pdf = os.path.join(models_path_pdf, 'rf.pkl')
elif(args.model == 'SVM'):
     model_path_exe = os.path.join(models_path_exe, 'svm.pkl')
     model_path_pdf = os.path.join(models_path_pdf, 'svm.pkl')
elif(args.model == 'GBT'):
     model_path_exe = os.path.join(models_path_exe, 'gbt.pkl')
     model_path_pdf = os.path.join(models_path_pdf, 'gbt.pkl')
elif(args.model == 'LGB'):
     model_path_exe = os.path.join(models_path_exe, 'lgb.pkl')
     model_path_pdf = os.path.join(models_path_pdf, 'lgb.pkl')
elif(args.model == 'NN1'):
     model_path_exe = os.path.join(models_path_exe, 'NN1.pkl')
elif(args.model == 'NN2'):
     model_path_exe = os.path.join(models_path_exe, 'NN2.pkl')
elif(args.model == 'NN3'):
     model_path_exe = os.path.join(models_path_exe, 'NN3.pkl')
elif(args.model == 'NN4'):
     model_path_exe = os.path.join(models_path_exe, 'NN4.pkl')
elif(args.model == 'NN5'):
     model_path_exe = os.path.join(models_path_exe, 'NN5.pkl')

model_path_pdf = os.path.join(models_path_pdf, 'rf.pkl')

# arguments=[]
# if(args.folder_scan): arguments.append('-f')
# if(args.quiet): arguments.append('-q')
# if(args.aggressive): arguments.append('-a')
# if(args.no_ascii_art): arguments.append('--no-ascii-art')
# if(args.verbose): arguments.append('-v')
# if(args.model and not args.aggressive): arguments+=[f'-m', f'{args.model}']
# if(args.library_use): arguments.append('-l')
# if(args.output): arguments+=[f'-o', f'{args.output}']
# args.library_use= True

def checkFileType(file_path):
     #ee = ExifToolHelper()
     try:
          metadata = ExifToolHelper().get_metadata(file_path)
          
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

def Folder_Scan(folder, modelpath, quiet, aggressive, verb, outfile):
     folder_path = pathlib.Path(folder)
     allFile_paths= list(folder_path.glob('*'))
     all_results = {}
     for fp in allFile_paths:
          FileType = checkFileType(file_path=fp)
          if(FileType == 1):
               result = VE.Scan_File_exe(file_path=fp, model_path=modelpath, quiet=quiet, aggressive=aggressive, verb=verb, outfile=outfile)
               all_results[fp] = result
          elif(FileType == 2):
               print("here")
               result = VP.ScanFile_pdf(file_path=fp, model_path=model_path_pdf, quiet=quiet, aggressive=aggressive, verb=verb, outfile=outfile)
               all_results[fp] = result
     return all_results



if(args.folder_scan):
     #VE.Folder_Scan_exe(folder=args.file_path, modelpath=model_path_exe, quiet=args.quiet, aggressive=args.aggressive, verb=args.verbose, outfile=args.output)
     Folder_Scan(folder= args.file_path, modelpath= args.model, quiet=args.quiet, aggressive=args.aggressive, verb=args.verbose, outfile=args.output)
else:
     fileType = checkFileType(file_path=args.file_path)     
     if(fileType == 1):
          print("here")
          VE.Scan_File_exe(file_path=args.file_path, model_path=model_path_exe, quiet=args.quiet, aggressive=args.aggressive, verb=args.verbose, outfile=args.output)
     elif(fileType == 2):
          print("here")
          VP.ScanFile_pdf(file_path=args.file_path, modelPath=model_path_pdf, quiet=args.quiet, aggressive=args.aggressive, verbose=args.verbose, output=args.output)
     elif(fileType == 0):
          print(f"File is not a windows PE nor PDF, wait for other modules for Vigil-Anti to support it")
     else:
          print(f"File is Corrupt, delete it if you suspect it!")


